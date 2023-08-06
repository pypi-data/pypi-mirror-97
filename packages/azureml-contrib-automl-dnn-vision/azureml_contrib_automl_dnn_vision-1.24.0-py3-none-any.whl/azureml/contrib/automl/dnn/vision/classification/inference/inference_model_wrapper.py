# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Class containing model wrapper object and other metadata."""

import pickle
import torch

from azureml.contrib.automl.dnn.vision.common.utils import _get_default_device
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionSystemException
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger


logger = get_logger(__name__)


class InferenceModelWrapper:
    """Class containing model wrapper object and other metadata."""

    @staticmethod
    def load_serialized_inference_model_wrapper(model_wrapper_pkl_file=None, device=None):
        """Load inference model wrapper from serialized files.

        :param model_wrapper_pkl_file: path to pickled inference model wrapper
        :type model_wrapper_pkl_file: str
        :param device: device on which to load the model
        :type device: str
        :return: inference model wrapper object
        :rtype: inference.InferenceModelWrapper
        """
        with open(model_wrapper_pkl_file, 'rb') as fp:
            inference_model_wrapper = pickle.load(fp)

        if device is None:
            device = _get_default_device()

        return inference_model_wrapper.to_device(device)

    def __init__(self, model_wrapper=None, labels=None, device=None):
        """
        :param model_wrapper: model wrapper object
        :type model_wrapper: azureml.dnn.vision.models.base_model_wrapper.BaseModelWrapper
        :param labels: list of string labels
        :type labels: list[str]
        :param device: device for the torch model
        :type device: str
        """

        self._model_wrapper = model_wrapper
        self._model_wrapper.optimizer = None
        self._model_wrapper.lr_scheduler = None
        self._labels = labels

        if device is None:
            device = _get_default_device()
        self._device = device

        self.to_device(device)

    def _get_tensor(self, images=None):
        """
        :param images: list of PIL Image objects
        :type images: list[PIL.Image]
        :return: tensor for image batch
        :rtype: torch.Tensor
        """
        return torch.stack([self._model_wrapper._resize_and_crop(x) for x in images], dim=0)

    @property
    def model_wrapper(self):
        """Model wrapper object."""
        return self._model_wrapper

    @property
    def labels(self):
        """List of string labels."""
        return self._labels

    def featurize(self, images):
        """Featurize images.

        :param images: list of PIL Image objects
        :type images: list[PIL.Image]
        :return: featurized images num_images x feature_size
        :rtype: torch.Tensor
        """
        features = self._model_wrapper._featurizer(self._get_tensor(images).to(self._device)).squeeze()
        # if there was just a single image, we wouldve got rid of the leading 1 dimension
        if len(features.shape) == 1:
            features = features.unsqueeze(0)

        return features

    def predict(self, images):
        """
        :param images: list of PIL Image objects
        :type images: list[PIL.Image]
        :return: label predictions - integer for multiclass, one hot encoding for multilabel
        :rtype: typing.Union[int, torch.Tensor]
        """
        outputs = self.model_wrapper._get_model_output(self._get_tensor(images).to(self._device))
        return self.model_wrapper.predict_from_outputs(outputs)

    def predict_proba(self, images):
        """
        :param images: list of PIL Image objects
        :type images: list[PIL.Image]
        :return: label probabilities - probabilities for every class
        :rtype: torch.Tensor
        """
        outputs = self.model_wrapper._get_model_output(self._get_tensor(images).to(self._device))
        return self.model_wrapper.predict_probs_from_outputs(outputs)

    def to_device(self, device=None):
        """Copy inference wrapper models to the device.

        :param device: 'cpu' or the gpu device eg. 'cuda:0'.
        :type device: str
        """
        if device is None:
            msg = 'Cannot transfer inference model wrapper a None device'
            logger.error(msg)
            raise AutoMLVisionSystemException(msg, has_pii=False)

        self.model_wrapper.model.to(device)
        self.model_wrapper.featurizer.to(device)
        # save which device the model is at
        self._device = device
        return self
