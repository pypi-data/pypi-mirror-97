# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions to write the model at the end of training."""

import os
import shutil
import json
import logging

from azureml.train.automl import constants

from azureml.contrib.automl.dnn.vision.common.model_export_utils import prepare_model_export
from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionValidationException
from azureml.contrib.automl.dnn.vision.classification.inference import InferenceModelWrapper

logger = logging.getLogger(__name__)


def write_model(run, model_wrapper, labels=None, output_dir=None,
                device=None, enable_onnx_norm=False,
                task_type=constants.Tasks.IMAGE_CLASSIFICATION):
    """Save a model to Artifacts.

    :param run: The current azureml run object
    :type run: azureml.core.run
    :param model_wrapper: Wrapper that contains model
    :type model_wrapper: azureml.contrib.automl.dnn.vision
    :param labels: list of classes
    :type labels: list
    :param output_dir: path to output directory
    :type output_dir: str
    :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
    :type device: str
    :param enable_onnx_norm: enable normalization when exporting onnx
    :type enable_onnx_norm: bool
    :return: inference model wrapper object
    :param task_type: Task type used in training
    :type task_type: str
    :rtype: inference.InferenceModelWrapper
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

    if model_wrapper.distributed:
        model_wrapper.model = model_wrapper.model.module
        model_wrapper.distributed = False

    # always save on cpu so we can restore both on CPU and GPU
    inference_model_wrapper = InferenceModelWrapper(model_wrapper, labels=labels, device='cpu')
    # Remove device info
    inference_model_wrapper._device = None

    # Save score and featurize script
    dirname = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(dirname, ArtifactLiterals.SCORE_SCRIPT),
                os.path.join(output_dir, ArtifactLiterals.SCORE_SCRIPT))
    shutil.copy(os.path.join(dirname, ArtifactLiterals.FEATURIZE_SCRIPT),
                os.path.join(output_dir, ArtifactLiterals.FEATURIZE_SCRIPT))

    folder_name = os.path.basename(output_dir)
    run.upload_folder(name=folder_name, path=output_dir)

    prepare_model_export(run=run, model_wrapper=inference_model_wrapper,
                         model_weights=model_weights,
                         output_dir=output_dir,
                         task_type=task_type)

    return inference_model_wrapper
