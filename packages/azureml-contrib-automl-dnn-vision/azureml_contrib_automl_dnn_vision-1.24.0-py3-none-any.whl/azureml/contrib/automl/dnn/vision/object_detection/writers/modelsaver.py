# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions to help save a trained model."""

import os
import json
import logging

from azureml.train.automl import constants

from azureml.contrib.automl.dnn.vision.common.model_export_utils import prepare_model_export
from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionValidationException

logger = logging.getLogger(__name__)

TASK_TYPE_PLACEHOLDER = "%%TASK_TYPE%%"


def write_model(run, model_wrapper, labels, output_dir,
                device=None, score_script_dir=None,
                enable_onnx_norm=False,
                task_type=constants.Tasks.IMAGE_OBJECT_DETECTION,
                model_settings=None, is_yolo=False):
    """Save a model to Artifacts

    :param run: The current azureml run object
    :type run: azureml.core.run
    :param model_wrapper: Model wrapper or model
    :type model_wrapper: typing.Union[CommonObjectDetectionModelWrapper, Model]
    :param labels: list of classes
    :type labels: list
    :param output_dir: Name of dir to save model files. If it does not exist, it will be created.
    :type output_dir: String
    :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
    :type device: str
    :param score_script_dir: directory of score_script to be copied (defaults to current dir if None)
    :type score_script_dir: str
    :param enable_onnx_norm: enable normalization when exporting onnx
    :type enable_onnx_norm: bool
    :param task_type: Task type used in training.
    :type task_type: str
    :param model_settings: Settings for the model
    :type model_settings: dict
    :param is_yolo: True if experiement is object detection yolo
    :type is_yolo: bool
    """
    os.makedirs(output_dir, exist_ok=True)

    # Export and save the torch onnx model.
    onnx_file_path = os.path.join(output_dir, ArtifactLiterals.ONNX_MODEL_FILE_NAME)
    model_wrapper.export_onnx_model(file_path=onnx_file_path, device=device, enable_norm=enable_onnx_norm)

    # Explicitly Save the labels to a json file.
    if labels is None:
        raise AutoMLVisionValidationException('No labels were found in dataset wrapper', has_pii=False)
    label_file_path = os.path.join(output_dir, ArtifactLiterals.LABEL_FILE_NAME)
    with open(label_file_path, 'w') as f:
        json.dump(labels, f)

    # Save PyTorch model weights
    model_weights = model_wrapper.get_state_dict()

    # Save pickle file
    model_wrapper.model = None
    model_wrapper.device = None
    model_wrapper.distributed = False

    # Save score script with appropriate task_type.
    if score_script_dir is None:
        score_script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(score_script_dir, ArtifactLiterals.SCORE_SCRIPT)) as source_file:
        with open(os.path.join(output_dir, ArtifactLiterals.SCORE_SCRIPT), "w") as output_file:
            output_file.write(source_file.read().replace(TASK_TYPE_PLACEHOLDER, task_type))

    # Upload outputs
    folder_name = os.path.basename(output_dir)
    if run is not None:
        run.upload_folder(name=folder_name, path=output_dir)

    prepare_model_export(run=run, model_wrapper=model_wrapper,
                         model_weights=model_weights,
                         output_dir=output_dir,
                         task_type=task_type,
                         model_settings=model_settings,
                         is_yolo=is_yolo)
