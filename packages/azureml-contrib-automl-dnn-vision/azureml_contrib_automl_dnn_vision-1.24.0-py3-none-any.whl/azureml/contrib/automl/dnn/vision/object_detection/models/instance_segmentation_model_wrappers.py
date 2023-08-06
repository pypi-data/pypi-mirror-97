# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper function to build instance segmentation wrappers."""
import time

import torch
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
from torchvision.ops._register_onnx_ops import _onnx_opset_version

from .object_detection_model_wrappers import FasterRCNNResnet50FPNWrapper
from .object_detection_model_wrappers import ObjectDetectionModelFactory
from ..common.constants import ModelNames, MaskRCNNLiterals, MaskRCNNParameters
from ..common.object_detection_utils import convert_box_score_thresh_to_float_tensor
from ...common.constants import ArtifactLiterals, PretrainedModelNames
from ...common.pretrained_model_utilities import PretrainedModelFactory
from ...common.logging_utils import get_logger

logger = get_logger(__name__)


class MaskRCNNResnet50FPNWrapper(FasterRCNNResnet50FPNWrapper):
    """Model wrapper for Mask RCNN with Resnet50 FPN backbone."""

    def _create_model(self, number_of_classes, specs=None, **kwargs):
        if specs is None:
            specs = {}

        kwargs = convert_box_score_thresh_to_float_tensor(**kwargs)
        model = PretrainedModelFactory.maskrcnn_resnet50_fpn(pretrained=True, **kwargs)

        if number_of_classes is not None:
            input_features_box = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(input_features_box,
                                                              number_of_classes)

            input_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
            hidden_layer = specs.get(MaskRCNNLiterals.MASK_PREDICTOR_HIDDEN_DIM,
                                     MaskRCNNParameters.DEFAULT_MASK_PREDICTOR_HIDDEN_DIM)
            model.roi_heads.mask_predictor = MaskRCNNPredictor(input_features_mask,
                                                               hidden_layer,
                                                               number_of_classes)

        return model

    def export_onnx_model(self, file_path=ArtifactLiterals.ONNX_MODEL_FILE_NAME, device=None, enable_norm=False):
        """
        Export the pytorch model to onnx model file.

        :param file_path: file path to save the exported onnx model.
        :type file_path: str
        :param device: device where model should be run (usually 'cpu' or 'cuda:0' if it is the first gpu)
        :type device: str
        :param enable_norm: enable normalization when exporting onnx
        :type enable_norm: bool
        """
        # TODO: support/verify batch inferencing
        # p0 (torchvision==0.7.0): device='cuda:0' is NOT working -- Device mismatch error from detection/rpn.py
        onnx_export_start = time.time()

        class ModelNormalizerWrapper(torch.nn.Module):
            def __init__(self, model):
                super(ModelNormalizerWrapper, self).__init__()
                self.model = model

            def forward(self, x):
                norm_x = self.normalize(x)
                output = self.model(norm_x)
                return output

            def normalize(self, imgs):
                new_imgs = imgs.clone()
                new_imgs /= 255
                return new_imgs

        dummy_input = torch.randn(1, 3, 600, 800).to(device='cpu')
        if self._distributed:
            new_model = self._model.module
        else:
            new_model = self._model

        new_model.to(device='cpu')
        new_model.eval()
        if enable_norm:
            dummy_input *= 255.
            new_model = ModelNormalizerWrapper(new_model)
        torch.onnx.export(new_model,
                          dummy_input,
                          file_path,
                          opset_version=_onnx_opset_version,
                          input_names=['input'],
                          output_names=['boxes', 'labels', 'scores', 'masks'],
                          dynamic_axes={'input': {0: 'batch', 1: 'channel', 2: 'height', 3: 'width'},
                                        'boxes': {0: 'prediction'},
                                        'labels': {0: 'prediction'},
                                        'scores': {0: 'prediction'},
                                        'masks': {0: 'prediction',
                                                  2: 'height',
                                                  3: 'width'}})
        onnx_export_time = time.time() - onnx_export_start
        logger.info('ONNX ({}) export time {:.4f} with enable_onnx_normalization ({})'
                    .format(file_path, onnx_export_time, enable_norm))


class InstanceSegmentationModelFactory(ObjectDetectionModelFactory):
    """Factory function to create mask rcnn models."""

    def __init__(self):
        """Init method."""
        super().__init__()

        self._models_dict = {
            ModelNames.MASK_RCNN_RESNET50_FPN: MaskRCNNResnet50FPNWrapper
        }
        self._pre_trained_model_names_dict = {
            ModelNames.MASK_RCNN_RESNET50_FPN: PretrainedModelNames.MASKRCNN_RESNET50_FPN_COCO
        }
        self._default_model = ModelNames.MASK_RCNN_RESNET50_FPN
