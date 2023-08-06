# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common utilities for object detection and object detection yolo."""
import json
import os
import pickle
import time
import torch

from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals, SettingsLiterals
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.common.utils import _read_image, _distill_run_from_experiment
from azureml.contrib.automl.dnn.vision.object_detection.common import boundingbox

from .constants import FasterRCNNLiterals, PredictionLiterals, TrainingLiterals, ValidationMetricType
from .masktools import convert_mask_to_polygon
from ..data.datasets import AmlDatasetObjectDetectionWrapper
from ..eval import cocotools
from ..eval.utils import prepare_bounding_boxes_for_eval
from ..eval.vocmap import VocMap
from ...common.average_meter import AverageMeter
from ...common.exceptions import AutoMLVisionSystemException
from ...common.system_meter import SystemMeter

logger = get_logger(__name__)


def _load_model_wrapper(torch_model_file, model_wrapper_pkl, device, **model_settings):
    with open(model_wrapper_pkl, 'rb') as fp:
        model_wrapper = pickle.load(fp)

    map_location = torch.device(device)
    model_weights = torch.load(torch_model_file, map_location=map_location)
    model_wrapper.restore_model(model_weights, **model_settings)

    return model_wrapper


def _fetch_model_from_artifacts(run_id, experiment_name=None, device=None, **model_settings):
    logger.info("Start fetching model from artifacts")
    run = _distill_run_from_experiment(run_id, experiment_name)

    run.download_file(os.path.join(ArtifactLiterals.OUTPUT_DIR, ArtifactLiterals.MODEL_FILE_NAME),
                      ArtifactLiterals.MODEL_FILE_NAME)
    run.download_file(os.path.join(ArtifactLiterals.OUTPUT_DIR, ArtifactLiterals.MODEL_WRAPPER_PKL),
                      ArtifactLiterals.MODEL_WRAPPER_PKL)
    logger.info("Finished downloading files from artifacts")

    return _load_model_wrapper(ArtifactLiterals.MODEL_FILE_NAME, ArtifactLiterals.MODEL_WRAPPER_PKL,
                               device=device, **model_settings)


def _get_box_dims(image_shape, box):
    box_keys = ['topX', 'topY', 'bottomX', 'bottomY']
    height, width = image_shape[0], image_shape[1]

    box_dims = dict(zip(box_keys, [coordinate.item() for coordinate in box]))

    box_dims['topX'] = box_dims['topX'] * 1.0 / width
    box_dims['bottomX'] = box_dims['bottomX'] * 1.0 / width
    box_dims['topY'] = box_dims['topY'] * 1.0 / height
    box_dims['bottomY'] = box_dims['bottomY'] * 1.0 / height

    return box_dims


def _get_bounding_boxes(label, image_shape, classes):
    bounding_boxes = []

    if 'masks' not in label:
        masks = [None] * len(label['boxes'])
    else:
        masks = label['masks']

    for box, label_index, score, mask in zip(label['boxes'], label['labels'], label['scores'], masks):
        box_dims = _get_box_dims(image_shape, box)

        box_record = {PredictionLiterals.BOX: box_dims,
                      PredictionLiterals.LABEL: classes[label_index],
                      PredictionLiterals.SCORE: score.item()}

        if mask is not None:
            mask = convert_mask_to_polygon(mask)
            box_record['polygon'] = mask

        bounding_boxes.append(box_record)

    return bounding_boxes


def _write_prediction_file_line(fw, filename, label, image_shape, classes):
    bounding_boxes = _get_bounding_boxes(label, image_shape, classes)

    annotation = {PredictionLiterals.FILENAME: filename,
                  PredictionLiterals.BOXES: bounding_boxes}

    fw.write('{}\n'.format(json.dumps(annotation)))


def _write_dataset_file_line(fw, filename, label, image_shape, classes):
    labels = []
    scores = []

    if 'masks' not in label:
        masks = [None] * len(label['boxes'])
    else:
        masks = label['masks']

    for box, label_index, score, mask in zip(label['boxes'], label['labels'], label['scores'], masks):
        label_record = _get_box_dims(image_shape, box)
        label_record[PredictionLiterals.LABEL] = classes[label_index]

        if mask is not None:
            mask = convert_mask_to_polygon(mask)
            label_record['polygon'] = mask

        labels.append(label_record)
        scores.append(score.item())

    AmlLabeledDatasetHelper.write_dataset_file_line(
        fw,
        filename,
        scores,
        labels)


def _parse_bounding_boxes(output_file, validation_dataset, val_index_map):
    logger.info("Start parsing predictions.")
    prediction_lines = 0
    bounding_boxes = []
    with open(output_file) as od:
        for prediction_line in od:
            prediction_lines += 1
            prediction_dict = json.loads(prediction_line)

            filename = validation_dataset._labeled_dataset_helper.get_image_full_path(prediction_lines - 1)
            # Ensure we deal with the same files in validation dataset as output file
            assert prediction_dict[PredictionLiterals.FILENAME] in filename

            image = _read_image(ignore_data_errors=True, image_url=filename)
            if image is None:
                logger.info("Skip invalid image {}.".format(image))
                continue

            height = image.height
            width = image.width

            image_boxes = boundingbox.ImageBoxes(filename, val_index_map)
            boxes = []
            labels = []
            scores = []
            for box in prediction_dict[PredictionLiterals.BOXES]:
                box_coordinates = [box['box']["topX"] * width, box['box']["topY"] * height,
                                   box['box']["bottomX"] * width, box['box']["bottomY"] * height]
                boxes.append(box_coordinates)
                labels.append(validation_dataset.label_to_index_map(box[PredictionLiterals.LABEL]))
                scores.append(box[PredictionLiterals.SCORE])
            image_boxes.add_boxes(torch.tensor(boxes), torch.tensor(labels), torch.tensor(scores))
            bounding_boxes.append(image_boxes)

    logger.info("End parsing {} predictions.".format(prediction_lines))
    return prepare_bounding_boxes_for_eval(bounding_boxes)


def compute_metrics(eval_bounding_boxes, val_metric_type,
                    val_coco_index, val_vocmap, val_index_map, label_metrics,
                    coco_metric_time, voc_metric_time,
                    master_process, run, add_to_run_properties=False):
    """Compute metrics from validation bounding boxes.

    :param eval_bounding_boxes: Bounding boxes list
    :type eval_bounding_boxes: List
    :param val_metric_type: Validation metric evaluation type.
    :type val_metric_type: ValidationMetricType.
    :param val_coco_index: Cocoindex created from validation data
    :type val_coco_index: Pycocotool Cocoindex object
    :param val_vocmap: VocMap created from validation data
    :type val_vocmap: VocMap object
    :param val_index_map: Map from class indices to class names
    :type val_index_map: List of strings
    :param label_metrics: Dictionary to store per label metrics across epochs
    :type label_metrics: Dict
    :param coco_metric_time: Meter to record coco computation time
    :type coco_metric_time: AverageMeter
    :param voc_metric_time: Meter to record vocmap computation time
    :type voc_metric_time: AverageMeter
    :param master_process: Master process or not
    :type master_process: bool
    :param run: azureml run object
    :type run: azureml.core.run.Run
    :param add_to_run_properties: Whether to add metrics like precision, recall to run properties.
    :type add_to_run_properties: bool
    :return: mAP score
    :rtype: float
    """

    if val_metric_type in ValidationMetricType.ALL_COCO and val_coco_index is None:
        raise AutoMLVisionSystemException("val_metric_type is {}. But, val_coco_index is None. "
                                          "Cannot compute metrics.".format(val_metric_type), has_pii=False)

    if val_metric_type in ValidationMetricType.ALL_VOC and val_vocmap is None:
        raise AutoMLVisionSystemException("val_metric_type is {}. But, val_vocmap is None. "
                                          "Cannot compute metrics.".format(val_metric_type), has_pii=False)

    map_score = 0.0

    task = "bbox"
    if eval_bounding_boxes and "segmentation" in eval_bounding_boxes[0]:
        task = "segm"

    if val_metric_type in ValidationMetricType.ALL_COCO:
        coco_metric_start = time.time()
        coco_score = cocotools.score_from_index(val_coco_index, eval_bounding_boxes, task)
        coco_metric_time.update(time.time() - coco_metric_start)
        logger.info("Coco Time {coco_time.value:.4f} ({coco_time.avg:.4f})".format(coco_time=coco_metric_time))
        map_score = coco_score[1]  # mAP at IoU 0.5

    if val_metric_type in ValidationMetricType.ALL_VOC:
        voc_metric_start = time.time()
        vocmap_result = val_vocmap.compute(eval_bounding_boxes, task)
        voc_metric_time.update(time.time() - voc_metric_start)

        vocmap_score = vocmap_result[VocMap.MAP]
        precision = vocmap_result[VocMap.PRECISION]
        recall = vocmap_result[VocMap.RECALL]

        logger.info("Voc map result: {}".format(vocmap_result))
        logger.info("Voc map score: {}".format(round(vocmap_score, 3)))
        logger.info("Precision: {}".format(round(precision, 3)))
        logger.info("Recall: {}".format(round(recall, 3)))
        logger.info("Voc Time {voc_time.value:.4f} ({voc_time.avg:.4f})".format(voc_time=voc_metric_time))

        if master_process and run is not None:
            run.log(VocMap.PRECISION, round(precision, 3))
            run.log(VocMap.RECALL, round(recall, 3))
            if add_to_run_properties:
                properties = {
                    VocMap.PRECISION: precision,
                    VocMap.RECALL: recall
                }
                run.add_properties(properties)

        if label_metrics is not None:
            for label, label_metric in vocmap_result[VocMap.LABEL_METRICS].items():
                label_name = val_index_map[label]
                if label_name not in label_metrics:
                    label_metrics[label_name] = {}
                for metric_name in [VocMap.PRECISION, VocMap.RECALL, VocMap.AVERAGE_PRECISION]:
                    if metric_name not in label_metrics[label_name]:
                        label_metrics[label_name][metric_name] = []
                    label_metrics[label_name][metric_name].append(round(label_metric[metric_name].item(), 3))

        map_score = vocmap_score  # Overwrites coco_score when val_metric_type is COCO_VOC.

    return map_score


def _evaluate_results(score_run, val_vocmap, eval_bounding_boxes, val_index_map):
    voc_metric_time = AverageMeter()
    map_score = compute_metrics(eval_bounding_boxes, val_metric_type=ValidationMetricType.VOC,
                                val_coco_index=None, val_vocmap=val_vocmap,
                                val_index_map=val_index_map, label_metrics=None,
                                coco_metric_time=AverageMeter(), voc_metric_time=voc_metric_time,
                                master_process=True, run=score_run, add_to_run_properties=True)
    score_run.log(VocMap.MAP, round(map_score, 3))
    properties_to_add = {
        VocMap.MAP: map_score
    }
    score_run.add_properties(properties_to_add)


def _validate_score_run(input_dataset_id, workspace, output_file, score_run):
    logger.info("Begin validating scoring run")
    if input_dataset_id is None:
        logger.warning("No input dataset specified, skipping validation.")
        return

    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    logger.info("Initializing validation dataset.")
    try:
        validation_dataset = AmlDatasetObjectDetectionWrapper(dataset_id=input_dataset_id,
                                                              is_train=False,
                                                              ignore_data_errors=True,
                                                              workspace=workspace,
                                                              download_files=False)
    except KeyError:
        logger.warning("Dataset does not contain ground truth, skipping validation.")
        return
    logger.info("End initializing validation dataset.")

    val_vocmap = VocMap(validation_dataset)
    val_index_map = validation_dataset.classes

    # Parse the predictions
    eval_bounding_boxes = _parse_bounding_boxes(output_file, validation_dataset, val_index_map)
    # Compare the results
    _evaluate_results(score_run, val_vocmap, eval_bounding_boxes, val_index_map)


def score_validation_data(run, model_settings, settings, device, score_with_model):
    """ Runs validations on the best model to give predictions output

    :param azureml_run: azureml run object
    :type azureml_run: azureml.core.run
    :param model_settings: dictionary containing model settings
    :type model_settings: dict
    :param settings: dictionary containing settings
    :type settings: dict
    :param device: device to use for inferencing
    :type device: str
    :param score_with_model: method to be called for scoring
    :type score_with_model: Callable
    """
    logger.info("Beginning validation for the best model")

    val_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)
    ignore_data_errors = settings.get(SettingsLiterals.IGNORE_DATA_ERRORS, True)

    # Get image_list_file with path
    root_dir = settings.get(SettingsLiterals.IMAGE_FOLDER, None)
    val_labels_file = settings.get(SettingsLiterals.VALIDATION_LABELS_FILE, None)
    if val_labels_file is not None:
        val_labels_file = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], val_labels_file)
        root_dir = os.path.join(settings[SettingsLiterals.DATA_FOLDER], root_dir)

    if val_labels_file is None and val_dataset_id is None:
        logger.warning("No validation dataset or validation file was given, skipping scoring run.")
        return

    # Get target path
    target_path = settings.get(SettingsLiterals.OUTPUT_DATASET_TARGET_PATH, None)
    if target_path is None:
        target_path = AmlLabeledDatasetHelper.get_default_target_path()

    batch_size = settings[TrainingLiterals.VALIDATION_BATCH_SIZE]
    output_file = settings.get(SettingsLiterals.VALIDATION_OUTPUT_FILE, None)
    num_workers = settings[SettingsLiterals.NUM_WORKERS]
    validate_scoring = settings[SettingsLiterals.VALIDATE_SCORING]
    log_scoring_file_info = settings.get(SettingsLiterals.LOG_SCORING_FILE_INFO, False)

    model = _fetch_model_from_artifacts(run_id=run.id, device=device, **model_settings)

    logger.info("[start scoring for validation data: batch_size: {}]".format(batch_size))

    score_with_model(model, run, target_path=target_path,
                     output_file=output_file, root_dir=root_dir,
                     image_list_file=val_labels_file, batch_size=batch_size,
                     ignore_data_errors=ignore_data_errors,
                     input_dataset_id=val_dataset_id,
                     num_workers=num_workers,
                     device=device,
                     validate_score=validate_scoring,
                     log_output_file_info=log_scoring_file_info)


def convert_box_score_thresh_to_float_tensor(**kwargs):
    """If box_score_thresh is present in kwargs, convert it to float32 tensor.

    Inference with onnx model obtained from FasterRCNN model fails in torch 1.7.1 as box_score_thresh
    is interpreted as float64 and float64 is not supported in one of the nodes(Greater).
    Passing it as a torch tensor with float32 type fixes the issue.

    :param kwargs: Optional keyword arguments
    :type kwargs: dict
    :return: modified keyword arguments
    :rtype: dict
    """
    if FasterRCNNLiterals.BOX_SCORE_THRESH in kwargs:
        box_score_thresh = kwargs.get(FasterRCNNLiterals.BOX_SCORE_THRESH)
        kwargs[FasterRCNNLiterals.BOX_SCORE_THRESH] = torch.tensor(box_score_thresh, dtype=torch.float)
    return kwargs
