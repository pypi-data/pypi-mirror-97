# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Base model factory class to be used by object detection and classification"""
from azureml.automl.core.shared.exceptions import ClientException

from .pretrained_model_utilities import PretrainedModelFactory


class BaseModelFactory:
    """Base class defining interface to be used by object detection and classification model factories"""

    def __init__(self):
        """Init method."""
        self._models_dict = {}
        self._pre_trained_model_names_dict = {}
        self._default_model = None

    def download_model_weights(self, model_name=None):
        """ Download model weights to a predefined location for a model.
        These weights will be later used to setup model wrapper.

        :param model_name: string name of the model if specified or None if not specified
        :type model_name: str or NoneType
        :return: model_name: String name of the chosen model
        :rtype: model_name: str
        """
        if model_name is None:
            model_name = self._default_model

        if model_name not in self._pre_trained_model_names_dict:
            raise ClientException('Unsupported model_name: {}'.format(model_name), has_pii=False)

        PretrainedModelFactory.download_pretrained_model_weights(
            self._pre_trained_model_names_dict[model_name], progress=True)
        return model_name

    def model_supported(self, model_name):
        """ Check if model is supported by the ModelFactory.

        :param model_name: string name of the model
        :type model_name: str
        :return: True if model is supported, None otherwise
        :rtype: bool
        """
        return model_name in self._models_dict
