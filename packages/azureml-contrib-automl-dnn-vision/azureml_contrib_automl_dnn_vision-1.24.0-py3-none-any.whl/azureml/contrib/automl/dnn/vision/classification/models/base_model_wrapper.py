# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Base class for model wrappers."""

from abc import ABC
import pickle
import time
try:
    import torch
except ImportError:
    print('ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and '
          'pytorch-ignite separately before running the package.')

from torchvision import transforms
from ..common.transforms import _make_3d_tensor
from ...common.constants import ArtifactLiterals
from ...common.logging_utils import get_logger

logger = get_logger(__name__)


class BaseModelWrapper(ABC):
    """Base class for model wrappers.

    Base class that model wrappers should inherit from. All inheriting concrete classes should call the base
    constructor.
    """

    def __init__(self, model=None, multilabel=False, name=None, resize_to_size=256, crop_size=224,
                 image_mean=[0.485, 0.456, 0.406], image_std=[0.229, 0.224, 0.225], featurizer=None):
        """BaseModelWrapper constructor that the concrete classes should call.

        :param model: torch model
        :type model: torch.nn.module
        :param multilabel: boolean flag for whether the model is trained for multilabel
        :type multilabel: bool
        :param name: name of the model that is used by ModelFactory to retrieve the model
        :type name: str
        :param resize_to_size: length of side of the square that we have to resize to
        :type resize_to_size: int
        :param crop_size: length of side of the square that we have to crop for passing to model
        :type crop_size: int
        :param image_mean: mean for each channel
        :type image_mean: list[float]
        :param image_std: std for each channel
        :type image_std: list[float]
        :param featurizer: torch model that outputs features for an image
        :type featurizer: torch.nn.module
        """
        self._model = model
        self._multilabel = multilabel
        self._name = name
        self._resize_to_size = resize_to_size
        self._crop_size = crop_size
        self._image_mean = image_mean
        self._image_std = image_std
        self._featurizer = featurizer
        self._featurizer.eval()
        self._transforms = None
        self._optimizer = None
        self._lr_scheduler = None
        self._distributed = False

    @staticmethod
    def load_serialized_model_wrapper(torch_model_file=None, model_wrapper_pkl_file=None):
        """Load model wrapper from serialized files.

        :param torch_model_file: path to torch model file
        :type torch_model_file: str
        :param model_wrapper_pkl_file: path to model wrapper pickle file
        :type model_wrapper_pkl_file: str
        :return: model wrapper object
        :rtype: base_model_wrapper object
        """
        with open(model_wrapper_pkl_file, 'rb') as fp:
            model_wrapper = pickle.load(fp)
        model_wrapper.model = torch.load(torch_model_file)

        return model_wrapper

    def _get_model_output(self, input_tensor):
        """Do a forward pass on the model.

        :param input_tensor: torch tensor representing the images
        :type input_tensor: torch.Tensor
        :return: model output
        :rtype: torch.Tensor
        """
        output = None
        is_model_train = self.model.training
        self.model.eval()
        with torch.no_grad():
            output = self.model(input_tensor)
        # restore model training mode
        if is_model_train:
            self.model.train()
        return output

    def _get_multilabel_preds(self, outputs, cutoff_for_multilabel=0.5):
        """
        :param outputs: model output from forward pass
        :type outputs: torch.Tensor
        :param cutoff_for_multilabel: cutoff for multilabel
        :type cutoff_for_multilabel: torch.Tensor
        :return: one hot encoded prediction
        :rtype: torch.Tensor
        """
        outputs = torch.sigmoid(outputs)
        return (outputs > cutoff_for_multilabel).type(torch.float)

    def _resize_and_crop(self, img):
        """
        :param img: PIL Image object
        :type img: PIL.Image
        :return: image as tensor
        :rtype: torch.Tensor
        """
        transforms_list = []
        if self._resize_to_size is not None:
            transforms_list.append(transforms.Resize(self.resize_to_size))

            transforms_list.extend([
                transforms.CenterCrop(self.crop_size),
                transforms.ToTensor(),
                transforms.Lambda(_make_3d_tensor),
                transforms.Normalize(self._image_mean, self._image_std)
            ])
        return transforms.Compose(transforms_list)(img)

    @property
    def featurizer(self):
        """Return featurizer."""
        return self._featurizer

    @property
    def model(self):
        """Model."""
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def name(self):
        """Name of the model."""
        return self._name

    def predict_from_outputs(self, outputs=None, cutoff_for_multilabel=0.5):
        """
        :param outputs: model output from forward pass
        :type outputs: torch.Tensor
        :param cutoff_for_multilabel: cutoff for multilabel
        :type cutoff_for_multilabel: torch.Tensor
        :return: integer labels for multiclass, one hot encoded results for multilabel
        :rtype: torch.Tensor
        """
        if self._multilabel:
            preds = self._get_multilabel_preds(outputs, cutoff_for_multilabel=cutoff_for_multilabel)
        else:
            _, preds = torch.max(outputs, 1)

        return preds

    def predict_probs_from_outputs(self, outputs=None):
        """
        :param outputs: model output from forward pass
        :type outputs: torch.Tensor
        :return: num_images x num_classes tensor
        :rtype: torch.Tensor
        """
        if self._multilabel:
            probs = torch.sigmoid(outputs)
        else:
            probs = torch.softmax(outputs, dim=-1)

        return probs

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
        onnx_export_start = time.time()

        class ModelNormalizerWrapper(torch.nn.Module):
            def __init__(self, model, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]):
                super(ModelNormalizerWrapper, self).__init__()
                self.model = model
                self.mean = mean
                self.std = std

            def forward(self, x):
                norm_x = self.normalize(x)
                output = self.model(norm_x)
                return output

            def normalize(self, imgs):
                # https://discuss.pytorch.org/t/tracerwarning-there-are-2-live-references-to-the-data-region-being-modified-when-tracing-in-place-operator-copy/68704/2
                new_imgs = imgs.clone()
                new_imgs /= 255
                # R
                new_imgs = torch.cat(((new_imgs[:, 0:1, :, :] - self.mean[0]) / self.std[0],
                                      new_imgs[:, 1:, :, :]), dim=1)
                # G
                new_imgs = torch.cat((new_imgs[:, 0:1, :, :],
                                      (new_imgs[:, 1:2, :, :] - self.mean[1]) / self.std[1],
                                      new_imgs[:, 2:, :, :]), dim=1)
                # B
                new_imgs = torch.cat((new_imgs[:, :2, :, :],
                                      (new_imgs[:, 2:, :, :] - self.mean[2]) / self.std[2]), dim=1)
                return new_imgs

        dummy_input = torch.rand(1, 3, self.crop_size, self.crop_size, device=device, requires_grad=False)
        model = self._model.module if self._distributed else self._model
        if device is not None:
            model.to(device=device)
        model.eval()
        new_model = model
        if enable_norm:
            dummy_input *= 255.
            new_model = ModelNormalizerWrapper(model, self._image_mean, self._image_std)
        torch.onnx.export(new_model,
                          dummy_input,
                          file_path,
                          do_constant_folding=True,
                          input_names=['input1'],
                          output_names=['output1'],
                          dynamic_axes={'input1': {0: 'batch'}, 'output1': {0: 'batch'}})
        onnx_export_time = time.time() - onnx_export_start
        logger.info('ONNX ({}) export time {:.4f} with enable_onnx_normalization ({})'
                    .format(file_path, onnx_export_time, enable_norm))

    @property
    def resize_to_size(self):
        """Size to which to resize before cropping."""
        return self._resize_to_size

    @property
    def crop_size(self):
        """Size to which to crop."""
        return self._crop_size

    @property
    def transforms(self):
        """Get image transforms

        :return: Image transforms
        :rtype: Function
        """
        return self._transforms

    @transforms.setter
    def transforms(self, value):
        """Set image transforms

        :param value: Transforms to apply to image
        :type value: Function
        """
        self._transforms = value

    @property
    def optimizer(self):
        """Get model optimizer

        :return: Training optimizer
        :rtype: Function
        """
        return self._optimizer

    @optimizer.setter
    def optimizer(self, value):
        """Set model optimizer

        :param value: Training optimizer
        :type value: Function
        """
        self._optimizer = value

    @property
    def lr_scheduler(self):
        """Get model lr_scheduler

        :return: Training lr_scheduler
        :rtype: Function
        """
        return self._lr_scheduler

    @lr_scheduler.setter
    def lr_scheduler(self, value):
        """Set model optimizer

        :param value: Training lr_scheduler
        :type value: Function
        """
        self._lr_scheduler = value

    @property
    def distributed(self):
        """Get if the model is a DistributedDataParallel model.

        :return: distributed
        :rtype: bool
        """
        return self._distributed

    @distributed.setter
    def distributed(self, value):
        """Set flag to indicate that the model is a DistributedDataParallel model.

        :param value: distributed
        :type value: bool
        """
        self._distributed = value

    def get_state_dict(self):
        """Get the state dictionary from PyTorch model.

        :return: State dictionary.
        :rtype: dict
        """
        if self._distributed:
            return self._model.module.state_dict()
        return self._model.state_dict()

    def load_state_dict(self, state_dict):
        """Set the state dictionary for PyTorch model.

        :param state_dict: State dictionary
        :type state_dict: dict
        """
        if self._distributed:
            self._model.module.load_state_dict(state_dict)
        else:
            self._model.load_state_dict(state_dict)
