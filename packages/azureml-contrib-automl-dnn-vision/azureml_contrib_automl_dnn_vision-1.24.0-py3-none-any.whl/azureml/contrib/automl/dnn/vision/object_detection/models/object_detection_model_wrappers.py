# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper functions to build model wrappers."""
import torch
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.transform import GeneralizedRCNNTransform
from torchvision.transforms import functional

from .base_model_wrapper import BaseObjectDetectionModelWrapper
from .customrcnn import CustomRCNNWrapper, CustomRCNNSpecifications
from ..common.constants import ModelNames, RCNNBackbones
from ..common.object_detection_utils import convert_box_score_thresh_to_float_tensor
from ...common.base_model_factory import BaseModelFactory
from ...common.constants import PretrainedModelNames
from ...common.pretrained_model_utilities import PretrainedModelFactory
from ...common.logging_utils import get_logger

logger = get_logger(__name__)


class CallableGeneralizedRCNNTransform:
    """Wrapper that exposes transforms extracted from GeneralizedRCNNTransform
    to be used when loading data on cpu."""
    def __init__(self, model):
        """Init method.

        :param model: a FasterRCNN model
        """
        self._gen_rcnn_transform = GeneralizedRCNNTransform(min_size=model.transform.min_size,
                                                            max_size=model.transform.max_size,
                                                            image_mean=model.transform.image_mean,
                                                            image_std=model.transform.image_std)

    @staticmethod
    def identity_batch(images):
        """A NOP batch method.

        :param images: images to batch
        :return: same images
        """
        return images

    def inference_transform(self, image):
        """Apply the transform from the model on a single image at inference time.

        :param image: the image to prepare for inference
        :type image: PIL Image
        :return: transformed image
        :rtype: Tensor
        """
        self._gen_rcnn_transform.training = False
        # No need for batching here, as this function is called for each image
        self._gen_rcnn_transform.batch_images = self.identity_batch
        image_tensor = functional.to_tensor(image)
        new_image, _ = self._gen_rcnn_transform(torch.unsqueeze(image_tensor, 0))  # transform expects a batch

        # remove the batch dimension
        return new_image.tensors[0]

    def train_validation_transform(self, is_train, image, boxes, masks=None):
        """Exposes model specific transformations.

        :param is_train: True if the transformations are for training, False otherwise.
        :param image: image tensor, 3 dimensions
        :param boxes: boxes tensor
        :param mask: tensors of masks (unnecessary)
        :return: a tuple with new image, boxes, height and width, and optionally new masks
        """

        self._gen_rcnn_transform.training = is_train
        # No need for batching here, as this function is called for each image
        self._gen_rcnn_transform.batch_images = self.identity_batch

        targets = {"boxes": boxes}

        if masks is not None:
            targets['masks'] = masks

        new_image, new_targets = self._gen_rcnn_transform(torch.unsqueeze(image, 0),  # transform expects a batch
                                                          [targets])
        # remove the batch dimension
        new_image = new_image.tensors[0]
        # the first element of the list contains the boxes for the image,
        # as the batch only has one entry

        new_boxes = new_targets[0]["boxes"]
        new_masks = new_targets[0].get("masks", None)

        new_height = new_image.shape[1]
        new_width = new_image.shape[2]

        return new_image, new_boxes, new_height, new_width, new_masks


class FasterRCNNResnet50FPNWrapper(BaseObjectDetectionModelWrapper):
    """Model wrapper for Faster RCNN with Resnet50 FPN backbone."""

    def __init__(self, number_of_classes=None, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param kwargs: Optional keyword arguments to define model specifications
        :type kwargs: dict
        """

        model = self._create_model(number_of_classes, **kwargs)
        super().__init__(model=model, number_of_classes=number_of_classes)

    def _create_model(self, number_of_classes, specs=None, load_pretrained_model_dict=True, **kwargs):
        kwargs = convert_box_score_thresh_to_float_tensor(**kwargs)
        model = PretrainedModelFactory.fasterrcnn_resnet50_fpn(pretrained=True,
                                                               load_pretrained_model_dict=load_pretrained_model_dict,
                                                               **kwargs)

        if number_of_classes is not None:
            input_features = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(input_features,
                                                              number_of_classes)

        return model

    def restore_model(self, model_dict=None, **kwargs):
        """Restores a saved model state.

        :param model_dict (optional): Saved pytorch dict with model weights
        :type model_dict: Pytorch state dict
        """
        # Only load the model_dict when creating model if one is not given
        load_pretrained_model_dict = model_dict is None

        self._model = self._create_model(number_of_classes=self._number_of_classes, specs=self._specs,
                                         load_pretrained_model_dict=load_pretrained_model_dict,
                                         **kwargs)

        if not load_pretrained_model_dict:
            self.load_state_dict(model_dict)

    def get_inference_transform(self):
        """Get the transformation function to use at inference time."""
        return CallableGeneralizedRCNNTransform(self.model).inference_transform

    def get_train_validation_transform(self):
        """Get the transformation function to use at training and validation time."""
        return CallableGeneralizedRCNNTransform(self.model).train_validation_transform

    def disable_model_transform(self):
        """Disable resize and normalize from the model."""

        self.model.transform.resize = self.identity_resize
        self.model.transform.normalize = self.identity_normalize

    @staticmethod
    def identity_normalize(image):
        """A NOP normalization method.

        :param image: image to normalize
        :return: same image
        """
        return image

    @staticmethod
    def identity_resize(image, target_index):
        """A NOP resize method.

        :param image: image to resize.
        :param target_index: target index to resize.
        :return: tuple with same image and target_index.
        """
        return image, target_index


class FasterRCNNResnet18FPNWrapper(CustomRCNNWrapper):
    """Model wrapper for Faster RCNN with Resnet 18 FPN backbone."""

    _specifications = CustomRCNNSpecifications(
        backbone=RCNNBackbones.RESNET_18_FPN_BACKBONE)

    def __init__(self, number_of_classes, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param kwargs: Optional keyword arguments to define model specifications
        :type kwargs: dict
        """

        super().__init__(number_of_classes, self._specifications, **kwargs)


class FasterRCNNMobilenetV2Wrapper(CustomRCNNWrapper):
    """Model wrapper for Faster RCNN with MobileNet v2 w/o FPN backbone."""

    _specifications = CustomRCNNSpecifications(
        backbone=RCNNBackbones.MOBILENET_V2_BACKBONE)

    def __init__(self, number_of_classes, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param kwargs: Optional keyword arguments to define model specifications
        :type kwargs: dict
        """

        super().__init__(number_of_classes, self._specifications, **kwargs)


class ObjectDetectionModelFactory(BaseModelFactory):
    """Factory function to create models."""

    def __init__(self):
        """Init method."""
        super().__init__()

        self._models_dict = {
            ModelNames.FASTER_RCNN_RESNET50_FPN: FasterRCNNResnet50FPNWrapper,
            ModelNames.FASTER_RCNN_RESNET18_FPN: FasterRCNNResnet18FPNWrapper,
            # init fails for MobileNetv2
            # ModelNames.FASTER_RCNN_MOBILENETV2: FasterRCNNMobilenetV2Wrapper
        }

        self._pre_trained_model_names_dict = {
            ModelNames.FASTER_RCNN_RESNET50_FPN: PretrainedModelNames.FASTERRCNN_RESNET50_FPN_COCO,
            ModelNames.FASTER_RCNN_RESNET18_FPN: PretrainedModelNames.RESNET18,
            # ModelNames.FASTER_RCNN_MOBILENETV2: PretrainedModelNames.MOBILENET_V2
        }

        self._default_model = ModelNames.FASTER_RCNN_RESNET50_FPN

    def get_model_wrapper(self, number_of_classes=None, model_name=None, **kwargs):
        """ Get the wrapper for a fasterrcnn model

        :param number_of_classes: number of classes in object detection
        :type number_of_classes: int
        :param model_name: string name of the model
        :type model_name: str
        """

        if model_name is None:
            model_name = self._default_model

        if model_name not in self._models_dict:
            raise ValueError('Unsupported model')

        return self._models_dict[model_name](number_of_classes=number_of_classes, **kwargs)
