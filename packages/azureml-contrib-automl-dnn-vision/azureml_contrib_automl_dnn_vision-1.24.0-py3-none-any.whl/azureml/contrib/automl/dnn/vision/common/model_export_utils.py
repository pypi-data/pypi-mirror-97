# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper Utils for model deployment."""
import os
import json
import logging
import pkg_resources
import tempfile
import torch

from azureml.core.run import _OfflineRun
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.core.inference import inference

from azureml.train.automl.runtime._azureautomlruncontext import AzureAutoMLRunContext

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals
from azureml.contrib.automl.dnn.vision.classification.inference import InferenceModelWrapper
from azureml.contrib.automl.dnn.vision.object_detection.common.object_detection_utils import _load_model_wrapper

logger = logging.getLogger(__name__)


def prepare_model_export(run, model_wrapper, model_weights, output_dir,
                         task_type, model_settings={}, is_yolo=False):
    """Save model and weights to artifacts, generate score script and
        conda environment yml, and save run properties needed for model export

    :param run: The current azureml run object
    :type run: azureml.core.run
    :param model_wrapper: Model wrapper or model
    :type model_wrapper: typing.Union[object_detection.models.CommonObjectDetectionModelWrapper,
                         object_detection_yolo.models.Model,
                         classification.models.BaseModelWrapper]
    :param model_weights: Saved pytorch dict with model weights
    :type model_weights: Pytorch state dict
    :param output_dir: Name of dir to save model files.
    :type output_dir: str
    :param task_type: Task type used in training.
    :type task_type: str
    :param model_settings: Settings for the model
    :type model_settings: dict
    :param is_yolo: True if experiment is object detection yolo
    :type is_yolo: bool
    """
    automl_run_context = AzureAutoMLRunContext(run)

    model_weights_path = os.path.join(output_dir, ArtifactLiterals.MODEL_FILE_NAME)
    model_wrapper_path = os.path.join(output_dir, ArtifactLiterals.MODEL_WRAPPER_PKL)

    models_to_upload = {model_weights_path: model_weights,
                        model_wrapper_path: model_wrapper}
    strs_to_save = {}

    # Save conda environment file into artifacts
    try:
        strs_to_save[constants.CONDA_ENV_FILE_PATH] = _create_conda_env_file_content(run)
    except Exception as e:
        logger.warning("Failed to create conda environment file.")
        logging_utilities.log_traceback(e, logger)

    # Save scoring file into artifacts
    try:
        scoring_file_str = _get_scoring_file(task_type=task_type,
                                             model_settings=model_settings,
                                             is_yolo=is_yolo)
        strs_to_save[constants.SCORING_FILE_PATH] = scoring_file_str
    except Exception as e:
        logger.warning("Failed to create score inference file.")
        logging_utilities.log_traceback(e, logger)

    # Upload files to artifact store
    automl_run_context.batch_save_artifacts(os.getcwd(), strs_to_save, models_to_upload)

    # Get model artifacts file paths
    scoring_data_loc = automl_run_context._get_artifact_id(constants.SCORING_FILE_PATH)
    conda_env_data_loc = automl_run_context._get_artifact_id(constants.CONDA_ENV_FILE_PATH)
    model_artifacts_file = automl_run_context._get_artifact_id(model_wrapper_path)
    model_data_dir = os.path.dirname(model_artifacts_file)

    # Add paths to run properties for model deployment
    properties_to_add = {
        inference.AutoMLInferenceArtifactIDs.ScoringDataLocation: scoring_data_loc,
        inference.AutoMLInferenceArtifactIDs.CondaEnvDataLocation: conda_env_data_loc,
        inference.AutoMLInferenceArtifactIDs.ModelDataLocation: model_data_dir
    }
    run.add_properties(properties_to_add)


def _create_conda_env_file_content(run):
    """
    Return conda/pip dependencies for the current run.

    If there are any changes to the conda environment file, the version of the conda environment
    file should be updated in the vendor.

    :param run: The current azureml run object
    :type run: azureml.core.run
    :return: Conda dependencies as string
    :rtype: str
    """
    env = run.get_environment()
    conda_deps = env.python.conda_dependencies

    # Add necessary extra package dependencies
    for conda_package in inference.AutoMLVisionCondaPackagesList:
        conda_deps.add_conda_package(conda_package)

    # Add pytorch channel to download pytorch and torchvision
    conda_deps.add_channel('pytorch')

    # Renames environment to 'project environment' instead
    # using the default generated name
    conda_deps._conda_dependencies['name'] = 'project_environment'
    return conda_deps.serialize_to_string()


def _get_scoring_file(task_type, model_settings={}, is_yolo=False):
    """
    Return scoring file to be used at the inference time.

    If there are any changes to the scoring file, the version of the scoring file should
    be updated in the vendor.

    :param task_type: Task type used in training
    :type task_type: str
    :param model_settings: Settings for the model
    :type model_settings: dict
    :param is_yolo: True if experiment is object detection yolo
    :type is_yolo: bool
    :return: Scoring python file as a string
    :rtype: str
    """
    scoring_file_path = pkg_resources.resource_filename(
        inference.PACKAGE_NAME, os.path.join('inference', 'score_images.txt'))

    # Ensure correct path is used to import _score_with_model in the script
    score_path = 'object_detection_yolo.writers' if is_yolo else 'object_detection.writers'
    if task_type in constants.Tasks.ALL_IMAGE_CLASSIFICATION:
        score_path = 'classification.inference'

    with open(scoring_file_path, 'r') as scoring_file_ptr:
        content = scoring_file_ptr.read()
        content = content.replace('<<artifacts_dir>>', ArtifactLiterals.OUTPUT_DIR)
        content = content.replace('<<task_type>>', task_type)
        content = content.replace('<<score_path>>', score_path)
        content = content.replace('<<model_settings>>', json.dumps(model_settings))

    return content


def load_model(task_type, model_artifacts_path, **model_settings):
    """Load model for model deployment

    :param task_type: Task type used in training.
    :type task_type: str
    :param model_artifacts_path: Path to the artifacts in model
    :type model_artifacts_path: str
    :param model_settings: Settings for the model
    :type model_settings: dict
    :return: Loaded model wrapper
    :rtype: typing.Union[object_detection.models.CommonObjectDetectionModelWrapper,
                         object_detection_yolo.models.Model,
                         classification.models.BaseModelWrapper]
    """
    model_pkl_path = os.path.join(model_artifacts_path, ArtifactLiterals.MODEL_WRAPPER_PKL)

    if task_type in constants.Tasks.ALL_IMAGE_CLASSIFICATION:
        return InferenceModelWrapper.load_serialized_inference_model_wrapper(model_pkl_path)
    else:
        model_weights_path = os.path.join(model_artifacts_path, ArtifactLiterals.MODEL_FILE_NAME)
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        return _load_model_wrapper(model_weights_path, model_pkl_path,
                                   device=device, **model_settings)


def run_inference(model, request_body, score_with_model):
    """ Run inferencing for deployed models

    :param model: Model to use for inferencing
    :type model: typing.Union[object_detection.models.CommonObjectDetectionModelWrapper,
                              object_detection_yolo.models.Model,
                              classification.models.BaseModelWrapper]
    :param request_body: Data of image to score
    :type request_body: str
    :param score_with_model: method to be called for scoring
    :type score_with_model: Callable
    :return: Output of inferencing
    :rtype: str
    """
    with tempfile.NamedTemporaryFile() as output_filename_fp, \
        tempfile.NamedTemporaryFile(mode="w") as image_list_file_fp, \
            tempfile.NamedTemporaryFile() as image_file_fp:

        image_file_fp.write(request_body)
        image_file_fp.flush()

        image_list_file_fp.write(image_file_fp.name)
        image_list_file_fp.flush()

        root_dir = ""
        device = utils._get_default_device()
        score_with_model(model,
                         run=_OfflineRun(),
                         target_path=None,
                         output_file=output_filename_fp.name,
                         root_dir=root_dir,
                         image_list_file=image_list_file_fp.name,
                         device=device,
                         num_workers=0)
        output_filename_fp.flush()
        return output_filename_fp.read()
