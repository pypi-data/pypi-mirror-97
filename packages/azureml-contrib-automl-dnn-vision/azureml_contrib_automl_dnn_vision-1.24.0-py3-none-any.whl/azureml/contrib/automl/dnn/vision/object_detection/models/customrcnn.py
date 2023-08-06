# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Model wrappers to build customized Faster RCNN Models."""

import torchvision

from .base_model_wrapper import BaseObjectDetectionModelWrapper
from ..common.constants import RCNNSpecifications, RCNNBackbones
from ..common.object_detection_utils import convert_box_score_thresh_to_float_tensor
from ...common.pretrained_model_utilities import PretrainedModelFactory
from azureml.automl.core.shared.exceptions import ClientException


class CustomRCNNSpecifications:
    """Class that contains all specifications necessary to define
    faster rcnn model."""

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional keyword arguments to define model specifications currently supported:
            -backbone: (string) Key that maps to custom backbone
        :type kwargs: dict
        """

        self._backbone = None

        if "backbone" in kwargs:
            self._backbone = kwargs["backbone"]
        else:
            self._backbone = RCNNSpecifications.DEFAULT_BACKBONE

    @property
    def backbone(self):
        """Get backbone name

        :return: Backbone name
        :rtype: String
        """
        return self._backbone


class CustomRCNNWrapper(BaseObjectDetectionModelWrapper):
    """Model wrapper for custom Faster RCNN Models."""

    _backbone_map = {RCNNBackbones.RESNET_18_FPN_BACKBONE: 'resnet18'}

    def __init__(self, number_of_classes, specifications, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param specifications: Model specifications
        :type specifications: CustomRCNNSpecifications
        :param kwargs: Keyword arguments
        :type kwargs: dict
        """

        model = self._create_model(number_of_classes, specifications, **kwargs)

        super().__init__(model=model, number_of_classes=number_of_classes, specs=specifications)

    def _create_model(self, num_classes, specifications, **kwargs):

        if 'fpn' in specifications.backbone:
            backbone = self._make_backbone(specifications.backbone)
        else:
            backbone = self._make_backbone_no_fpn(specifications.backbone)

        kwargs = convert_box_score_thresh_to_float_tensor(**kwargs)
        model = torchvision.models.detection.faster_rcnn.FasterRCNN(backbone=backbone,
                                                                    num_classes=num_classes, **kwargs)
        return model

    def _make_backbone(self, backbone):

        if backbone in RCNNSpecifications.RESNET_FPN_BACKBONES:
            torch_backbone_name = self._backbone_map[backbone]
            model_backbone = PretrainedModelFactory.resnet_fpn_backbone(
                torch_backbone_name, pretrained=True)
        else:
            raise ClientException('{} not supported'.format(backbone))\
                .with_generic_msg("backbone not supported.")

        return model_backbone

    def _make_backbone_no_fpn(self, backbone):

        if backbone in RCNNSpecifications.CNN_BACKBONES:
            model_backbone = PretrainedModelFactory.mobilenet_v2(pretrained=True).features
            model_backbone.out_channels = 1280
        else:
            raise ClientException('{} not supported'.format(backbone))\
                .with_generic_msg("backbone not supported.")

        return model_backbone
