# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Scoring functions that can load a serialized model and predict."""

import os
import json
import time
import torch

from azureml.core.run import Run, _OfflineRun
from azureml.contrib.dataset.labeled_dataset import _LabeledDatasetFactory

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.constants import (
    ArtifactLiterals, ScoringLiterals, SettingsLiterals
)
from azureml.contrib.automl.dnn.vision.common.dataloaders import RobustDataLoader
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.common.prediction_dataset import PredictionDataset
from azureml.contrib.automl.dnn.vision.classification.common.constants import (
    PredictionLiterals, scoring_settings_defaults, featurization_settings_defaults
)

from azureml.contrib.automl.dnn.vision.common.average_meter import AverageMeter
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.system_meter import SystemMeter
from . import InferenceModelWrapper

logger = get_logger(__name__)


def _get_labels_as_array(num_to_labels):
    num_labels = max(num_to_labels.keys()) + 1
    labels = [0] * num_labels
    for i in range(num_labels):
        labels[i] = num_to_labels[i]

    return labels


def load_model_from_artifacts(run_id, experiment_name=None, artifacts_dir=None):
    """
    :param run_id: run id of the run that produced the model
    :type run_id: str
    :param experiment_name: name of experiment that contained the run id
    :type experiment_name: str
    :param artifacts_dir: artifacts directory
    :type artifacts_dir: str
    :return: InferenceModelWrapper object
    :rtype: inference.InferenceModelWrapper
    """
    logger.info("Start fetching model from artifacts")
    if artifacts_dir is None:
        artifacts_dir = ArtifactLiterals.OUTPUT_DIR

    run = utils._distill_run_from_experiment(run_id, experiment_name)

    run.download_file(os.path.join(artifacts_dir, ArtifactLiterals.MODEL_WRAPPER_PKL),
                      output_file_path=ArtifactLiterals.MODEL_WRAPPER_PKL)
    logger.info("Finished downloading files from artifacts")

    return InferenceModelWrapper.load_serialized_inference_model_wrapper(ArtifactLiterals.MODEL_WRAPPER_PKL)


def _write_prediction_file_line(fw, filename, prob, inference_labels):
    fw.write(
        json.dumps(
            {
                PredictionLiterals.FILENAME: filename,
                PredictionLiterals.PROBS: prob.cpu().numpy().tolist(),
                PredictionLiterals.LABELS: inference_labels
            }
        )
    )
    fw.write('\n')


def _write_dataset_file_line(fw, file_name, prob, inference_labels):
    AmlLabeledDatasetHelper.write_dataset_file_line(
        fw,
        file_name,
        prob.cpu().numpy().tolist(),
        inference_labels)


def _featurize_batch(model_wrapper, filenames, batch, output_file):
    features = model_wrapper.featurizer(batch).squeeze()
    # make sure we don't squeeze the batch dimension
    if len(features.shape) == 1:
        features = features.unsqueeze(0)
    features = features.cpu().numpy()
    num_lines = 0
    for filename, feat in zip(filenames, features):
        num_lines += 1
        output_file.write(
            json.dumps(
                {
                    PredictionLiterals.FILENAME: filename,
                    PredictionLiterals.FEATURE_VECTOR: feat.tolist(),
                }
            )
        )
        output_file.write('\n')
    return num_lines


def _score_batch(model_wrapper, filenames, batch, output_file,
                 labeled_dataset_file, inference_labels):
    outputs = model_wrapper.model(batch)
    probs = model_wrapper.predict_probs_from_outputs(outputs)
    num_lines = 0
    for filename, prob in zip(filenames, probs):
        num_lines += 1
        _write_prediction_file_line(output_file, filename, prob, inference_labels)
        _write_dataset_file_line(labeled_dataset_file, filename,
                                 prob, inference_labels)
    return num_lines


def _perform_inference(dataloader, device, model_wrapper, output_file,
                       start_time, labeled_dataset_file=None,
                       inference_labels=None, run_featurization=False,
                       log_output_file_info=False):
    """ Performs inference on the given model_wrapper

    :param dataloader: dataloader for inferencing
    :type dataloader: torch.utils.data.dataloader.Dataloader
    :param device: device on which to load the batches
    :type device: str
    :param model_wrapper: model wrapper object
    :type model_wrapper: classification.models.base_model_wrapper.BaseModelWrapper
    :param output_file: opened file to write predictions
    :type output_file: _io.TextIOWrapper
    :param start_time: inferencing start time
    :type start_time: float
    :param labeled_dataset_file: opened file to write dataset lines
    :type labeled_dataset_file: _io.TextIOWrapper
    :param inference_labels: list of string labels
    :type inference_labels: list[str]
    :param run_featurization: flag on whether to score or featurize
    :type run_featurization: bool
    :param log_output_file_info: flag on whether to log output file debug info
    :type log_output_file_info: bool
    """
    batch_time = AverageMeter()
    end = time.time()
    system_meter = SystemMeter()

    # count number of lines written to feature output
    output_num_lines = 0
    with open(output_file, 'w') as fw:
        with torch.no_grad():
            for i, (filenames, batch) in enumerate(utils._data_exception_safe_iterator(iter(dataloader))):
                batch = batch.to(device)

                if run_featurization:
                    batch_num_lines = _featurize_batch(model_wrapper, filenames=filenames,
                                                       batch=batch, output_file=fw)
                else:
                    batch_num_lines = _score_batch(model_wrapper, filenames=filenames,
                                                   batch=batch, output_file=fw,
                                                   labeled_dataset_file=labeled_dataset_file,
                                                   inference_labels=inference_labels)
                output_num_lines += batch_num_lines

                batch_time.update(time.time() - end)
                end = time.time()
                if i % 100 == 0 or i == len(dataloader) - 1:
                    mesg = "Epoch: [{0}/{1}]\t" "Time {batch_time.value:.4f}" \
                        " ({batch_time.avg:.4f})\t".format(i, len(dataloader), batch_time=batch_time)
                    mesg += system_meter.get_gpu_stats()
                    logger.info(mesg)
                    system_meter.log_system_stats(True)

    # measure total inference time
    total_inference_time = time.time() - start_time
    if run_featurization:
        logger.info("Number of lines written to featurization output file: {}".format(output_num_lines))
        utils.log_end_featurizing_stats(total_inference_time, batch_time, system_meter)
    else:
        logger.info("Number of lines written to prediction file: {}".format(output_num_lines))
        utils.log_end_scoring_stats(total_inference_time, batch_time, system_meter)

    if log_output_file_info:
        output_type = "featurization" if run_featurization else "scoring"
        logger.info("{} output file closed status: {}".format(output_type, fw.closed))
        with open(output_file, "r") as fw:
            # count number of lines actually written to the output files
            logger.info("Number of lines read from {} output file: {}".format(output_type, len(fw.readlines())))


def _score_with_model(inference_model_wrapper, run, target_path, device,
                      output_file=None, root_dir=None, image_list_file=None,
                      batch_size=80, ignore_data_errors=True,
                      labeled_dataset_factory=_LabeledDatasetFactory,
                      labeled_dataset_file=None,
                      input_dataset_id=None, always_create_dataset=False,
                      num_workers=None,
                      output_featurization=False,
                      featurization_output_file=None, log_output_file_info=False):
    if output_file is None:
        os.makedirs(ScoringLiterals.DEFAULT_OUTPUT_DIR, exist_ok=True)
        output_file = os.path.join(ScoringLiterals.DEFAULT_OUTPUT_DIR,
                                   ScoringLiterals.PREDICTION_FILE_NAME)
    if labeled_dataset_file is None:
        os.makedirs(ScoringLiterals.DEFAULT_OUTPUT_DIR, exist_ok=True)
        labeled_dataset_file = os.path.join(ScoringLiterals.DEFAULT_OUTPUT_DIR,
                                            ScoringLiterals.LABELED_DATASET_FILE_NAME)

    ws = None if isinstance(run, _OfflineRun) else run.experiment.workspace

    model_wrapper = inference_model_wrapper.model_wrapper
    model_wrapper.model.eval()
    model_wrapper.model = model_wrapper.model.to(device)

    score_start = time.time()
    logger.info("Building the prediction dataset")
    dataset = PredictionDataset(root_dir=root_dir,
                                image_list_file=image_list_file,
                                transforms=model_wrapper.transforms,
                                ignore_data_errors=ignore_data_errors,
                                input_dataset_id=input_dataset_id, ws=ws)
    dataloader = RobustDataLoader(dataset,
                                  batch_size=batch_size,
                                  drop_last=False,
                                  num_workers=num_workers)

    with open(labeled_dataset_file, "w") as ldsf:
        inference_labels = inference_model_wrapper.labels
        logger.info("Starting the inference")
        _perform_inference(dataloader=dataloader, device=device,
                           model_wrapper=model_wrapper,
                           output_file=output_file,
                           start_time=score_start,
                           labeled_dataset_file=ldsf,
                           inference_labels=inference_labels,
                           log_output_file_info=log_output_file_info)

    if log_output_file_info:
        logger.info("Labeled dataset file closed status: {}".format(ldsf.closed))
        with open(labeled_dataset_file, "r") as ldsf:
            logger.info("Number of lines read from labeled dataset file: {}".format(len(ldsf.readlines())))

    if always_create_dataset or input_dataset_id is not None:
        datastore = ws.get_default_datastore()
        AmlLabeledDatasetHelper.create(run, datastore, labeled_dataset_file, target_path,
                                       "ImageClassification", labeled_dataset_factory)

    # run featurizations after scoring
    if output_featurization:
        featurize_start = time.time()
        logger.info("[start featurization: batch_size: {}]".format(batch_size))
        model_wrapper.featurizer.eval()
        model_wrapper.model = model_wrapper.featurizer.to(device)
        if featurization_output_file is None:
            os.makedirs(ScoringLiterals.DEFAULT_OUTPUT_DIR, exist_ok=True)
            featurization_output_file = os.path.join(ScoringLiterals.DEFAULT_OUTPUT_DIR,
                                                     ScoringLiterals.FEATURE_FILE_NAME)
        logger.info("Starting the featurization")
        _perform_inference(dataloader=dataloader, device=device,
                           model_wrapper=model_wrapper,
                           output_file=featurization_output_file,
                           start_time=featurize_start,
                           run_featurization=True,
                           log_output_file_info=log_output_file_info)


def _featurize_with_model(inference_model_wrapper, run, device,
                          output_file=None, root_dir=None, image_list_file=None,
                          batch_size=80, ignore_data_errors=True,
                          num_workers=None, input_dataset_id=None,
                          log_output_file_info=False):
    if output_file is None:
        os.makedirs(ScoringLiterals.DEFAULT_OUTPUT_DIR, exist_ok=True)
        output_file = os.path.join(ScoringLiterals.DEFAULT_OUTPUT_DIR,
                                   ScoringLiterals.FEATURE_FILE_NAME)

    ws = None if isinstance(run, _OfflineRun) else run.experiment.workspace

    model_wrapper = inference_model_wrapper.model_wrapper
    model_wrapper.featurizer.eval()

    model_wrapper.model = model_wrapper.featurizer.to(device)

    featurize_start = time.time()
    logger.info("Building the prediction dataset")
    dataset = PredictionDataset(root_dir=root_dir,
                                image_list_file=image_list_file,
                                transforms=model_wrapper.transforms,
                                ignore_data_errors=ignore_data_errors,
                                input_dataset_id=input_dataset_id, ws=ws)
    dataloader = RobustDataLoader(dataset,
                                  batch_size=batch_size,
                                  drop_last=False,
                                  num_workers=num_workers)

    logger.info("Starting the featurization")
    _perform_inference(dataloader=dataloader, device=device,
                       model_wrapper=model_wrapper,
                       output_file=output_file,
                       start_time=featurize_start,
                       run_featurization=True,
                       log_output_file_info=log_output_file_info)


def featurize(run_id, device, experiment_name=None, output_file=None,
              root_dir=None, image_list_file=None, batch_size=80,
              ignore_data_errors=True, input_dataset_id=None, log_output_file_info=False):
    """Generate predictions from input files.

    :param run_id: azureml run id
    :type run_id: str
    :param device: device to be used for inferencing
    :type device: str
    :param experiment_name: name of experiment
    :type experiment_name: str
    :param output_file: path to output file
    :type output_file: str
    :param root_dir: prefix to be added to the paths contained in image_list_file
    :type root_dir: str
    :param image_list_file: path to file containing list of images
    :type image_list_file: str
    :param batch_size: batch size for prediction
    :type batch_size: int
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
    :type input_dataset_id: str
    :param log_output_file_info: flag on whether to log output file debug info
    :type log_output_file_info: bool
    """
    logger.info("[start featurization: batch_size: {}]".format(batch_size))
    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    inference_model_wrapper = load_model_from_artifacts(run_id, experiment_name=experiment_name)
    run = Run.get_context()

    num_workers = featurization_settings_defaults[SettingsLiterals.NUM_WORKERS]

    _featurize_with_model(inference_model_wrapper, run, device,
                          output_file=output_file, root_dir=root_dir,
                          image_list_file=image_list_file, batch_size=batch_size,
                          ignore_data_errors=ignore_data_errors,
                          input_dataset_id=input_dataset_id,
                          num_workers=num_workers,
                          log_output_file_info=log_output_file_info)


def score(run_id, device, experiment_name=None, output_file=None,
          root_dir=None, image_list_file=None, batch_size=80,
          ignore_data_errors=True, output_dataset_target_path=None,
          input_dataset_id=None, output_featurization=False,
          featurization_output_file=None, log_output_file_info=False):
    """Generate predictions from input files.

    :param run_id: azureml run id
    :type run_id: str
    :param device: device to be used for inferencing
    :type device: str
    :param experiment_name: name of experiment
    :type experiment_name: str
    :param output_file: path to output file
    :type output_file: str
    :param root_dir: prefix to be added to the paths contained in image_list_file
    :type root_dir: str
    :param image_list_file: path to file containing list of images
    :type image_list_file: str
    :param batch_size: batch size for prediction
    :type batch_size: int
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dataset_target_path: path on Datastore for the output dataset files.
    :type output_dataset_target_path: str
    :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
    :type input_dataset_id: str
    :param output_featurization: boolean flag on whether to run featurizations after scoring
    :type output_featurization: bool
    :param featurization_output_file: path to featurization output file
    :type featurization_output_file: str
    :param log_output_file_info: flag on whether to log output file debug info
    :type log_output_file_info: bool
    """
    logger.info("[start inference: batch_size: {}]".format(batch_size))
    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    inference_model_wrapper = load_model_from_artifacts(run_id, experiment_name=experiment_name)
    logger.info("Model restored successfully")
    run = Run.get_context()

    if output_dataset_target_path is None:
        output_dataset_target_path = AmlLabeledDatasetHelper.get_default_target_path()

    num_workers = scoring_settings_defaults[SettingsLiterals.NUM_WORKERS]

    _score_with_model(inference_model_wrapper, run,
                      output_dataset_target_path,
                      device=device, output_file=output_file,
                      root_dir=root_dir,
                      image_list_file=image_list_file,
                      batch_size=batch_size,
                      ignore_data_errors=ignore_data_errors,
                      input_dataset_id=input_dataset_id,
                      num_workers=num_workers,
                      output_featurization=output_featurization,
                      featurization_output_file=featurization_output_file,
                      log_output_file_info=log_output_file_info)
