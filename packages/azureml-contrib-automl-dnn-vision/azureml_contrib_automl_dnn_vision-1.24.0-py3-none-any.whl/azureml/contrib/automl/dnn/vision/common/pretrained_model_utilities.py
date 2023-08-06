# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Pretrained model utilities for the package."""


try:
    from torchvision.models.resnet import ResNet, BasicBlock, Bottleneck
    from torchvision.models.mobilenet import MobileNetV2
    from torchvision.models.utils import load_state_dict_from_url

    from torchvision.models.detection.faster_rcnn import FasterRCNN
    from torchvision.models.detection.mask_rcnn import MaskRCNN
    from torchvision.ops import misc as misc_nn_ops
    from torchvision.models.detection.backbone_utils import BackboneWithFPN

    from pretrainedmodels.models.senet import SENet, SEResNeXtBottleneck, pretrained_settings

except ImportError:
    print('ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and '
          'pytorch-ignite separately before running the package.')

from urllib.error import URLError, ContentTooShortError

from .constants import PretrainedModelNames, PretrainedModelUrls, PretrainedSettings
from .exceptions import AutoMLVisionSystemException
from .logging_utils import get_logger

logger = get_logger(__name__)


class PretrainedModelFactory:
    """The Factory class of creating the pretrained models that are used by the package."""

    @staticmethod
    def _load_state_dict_from_url_with_retry(url, progress=True, check_hash=True, **kwargs):
        """Fetch state dict from a url.

        :param url: Url to download state dict from
        :type url: str
        :param progress: Whether or not to display download progress
                         (see torchvision.models.utils.load_state_dict_from_url)
        :type progress: bool
        :param check_hash: Whether or not to check hash of the downloaded file
                           (see torchvision.models.utils.load_state_dict_from_url)
        :type check_hash: bool
        :param kwargs: keywords args for torchvision.models.utils.load_state_dict_from_url
        :type kwargs: dict
        :return: state dict for torch model
        :rtype: dict
        """
        for i in range(PretrainedSettings.DOWNLOAD_RETRY_COUNT - 1):
            try:
                return load_state_dict_from_url(url, progress=progress, check_hash=check_hash, **kwargs)
            except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError,
                    URLError, ContentTooShortError, RuntimeError) as e:
                logger.warning('Encountered {} error while loading state dict. Retry count: {}. Error details: {}'
                               .format(e.__class__.__name__, i + 1, e))

        return load_state_dict_from_url(url, progress=progress, check_hash=check_hash, **kwargs)

    @staticmethod
    def download_pretrained_model_weights(model_name, progress=True):
        """Fetch pretrained state dict from a url and download to a local path.

        :param model_name: Name of the pretrained model.
        :type model_name: PretrainedModelNames
        :param progress: If True, displays a progress bar of the download to stderr
        :type progress: bool
        """
        PretrainedModelFactory._load_state_dict_from_url_with_retry(
            PretrainedModelUrls.MODEL_URLS[model_name], progress=progress)

    @staticmethod
    def resnet18(pretrained=False, progress=True, **kwargs):
        r"""ResNet-18 model from
        `"Deep Residual Learning for Image Recognition" <https://arxiv.org/pdf/1512.03385.pdf>`_

        Args:
            pretrained (bool): If True, returns a model pre-trained on ImageNet
            progress (bool): If True, displays a progress bar of the download to stderr
        """
        return PretrainedModelFactory._resnet(PretrainedModelNames.RESNET18,
                                              BasicBlock,
                                              [2, 2, 2, 2],
                                              pretrained,
                                              progress,
                                              **kwargs)

    @staticmethod
    def resnet50(pretrained=False, progress=True, **kwargs):
        r"""ResNet-50 model from
        `"Deep Residual Learning for Image Recognition" <https://arxiv.org/pdf/1512.03385.pdf>`_

        Args:
            pretrained (bool): If True, returns a model pre-trained on ImageNet
            progress (bool): If True, displays a progress bar of the download to stderr
        """
        return PretrainedModelFactory._resnet(PretrainedModelNames.RESNET50,
                                              Bottleneck,
                                              [3, 4, 6, 3],
                                              pretrained,
                                              progress,
                                              **kwargs)

    @staticmethod
    def mobilenet_v2(pretrained=False, progress=True, **kwargs):
        """
        Constructs a MobileNetV2 architecture from
        `"MobileNetV2: Inverted Residuals and Linear Bottlenecks" <https://arxiv.org/abs/1801.04381>`_.

        Args:
            pretrained (bool): If True, returns a model pre-trained on ImageNet
            progress (bool): If True, displays a progress bar of the download to stderr
        """
        model = MobileNetV2(**kwargs)
        if pretrained:
            state_dict = PretrainedModelFactory._load_state_dict_from_url_with_retry(
                PretrainedModelUrls.MODEL_URLS[PretrainedModelNames.MOBILENET_V2], progress=progress)
            model.load_state_dict(state_dict)
        return model

    @staticmethod
    def se_resnext50_32x4d(num_classes=1000, pretrained=True, pretrained_on='imagenet'):
        """
        Constructs a se_resnext50_32x4d pretrained model.
        """
        model = SENet(SEResNeXtBottleneck, [3, 4, 6, 3], groups=32, reduction=16,
                      dropout_p=None, inplanes=64, input_3x3=False,
                      downsample_kernel_size=1, downsample_padding=0,
                      num_classes=num_classes)
        if pretrained:
            settings = pretrained_settings[PretrainedModelNames.SE_RESNEXT50_32X4D][pretrained_on]
            settings['url'] = PretrainedModelUrls.MODEL_URLS[PretrainedModelNames.SE_RESNEXT50_32X4D]
            PretrainedModelFactory._initialize_pretrained_model(model, num_classes, settings)
        return model

    @staticmethod
    def _setup_resnet50_fpn_backbone_model(model_constructor, pretrained_model_name,
                                           pretrained, progress, num_classes, pretrained_backbone,
                                           load_pretrained_model_dict, **kwargs):

        # Check that number of classes is compatible with pretrained model.

        if pretrained and num_classes != 91:
            raise AutoMLVisionSystemException(
                "Pretrained model is set to true and num_classes "
                "is set to {}, which is different from supported value 91.".format(num_classes))

        if pretrained:
            # no need to download the backbone if pretrained is set
            pretrained_backbone = False
        backbone = PretrainedModelFactory.resnet_fpn_backbone(PretrainedModelNames.RESNET50,
                                                              pretrained_backbone)
        model = model_constructor(backbone, num_classes, **kwargs)
        if pretrained and load_pretrained_model_dict:
            # Note the eventual load_state_dict_from_url method already uses SHA256 hash to ensure the unique
            # file name and check the file content.
            state_dict = PretrainedModelFactory._load_state_dict_from_url_with_retry(
                PretrainedModelUrls.MODEL_URLS[pretrained_model_name],
                progress=progress)
            model.load_state_dict(state_dict)

        return model

    @staticmethod
    def fasterrcnn_resnet50_fpn(pretrained=False, progress=True,
                                num_classes=91, pretrained_backbone=True,
                                load_pretrained_model_dict=True, **kwargs):
        """
        Constructs a Faster R-CNN model with a ResNet-50-FPN backbone.

        Args:
            pretrained (bool): If True, returns a model pre-trained on COCO train2017.
            progress (bool): If True, displays a progress bar of the download to stderr.
            num_classes: Number of classes.
            pretrained_backbone: Pretrained backbone.
            load_pretrained_model_dict: Load pretrained weights for entire model.
        """
        return PretrainedModelFactory._setup_resnet50_fpn_backbone_model(
            FasterRCNN,
            PretrainedModelNames.FASTERRCNN_RESNET50_FPN_COCO,
            pretrained, progress, num_classes, pretrained_backbone,
            load_pretrained_model_dict, **kwargs)

    @staticmethod
    def maskrcnn_resnet50_fpn(pretrained=False, progress=True,
                              num_classes=91, pretrained_backbone=True,
                              load_pretrained_model_dict=True, **kwargs):
        """
        Constructs a Mask R-CNN model with a ResNet-50-FPN backbone.

        Args:
            pretrained (bool): If True, returns a model pre-trained on COCO train2017.
            progress (bool): If True, displays a progress bar of the download to stderr.
            num_classes: Number of classes.
            pretrained_backbone: Pretrained backbone.
            load_pretrained_model_dict: Load pretrained weights for entire model.
        """
        return PretrainedModelFactory._setup_resnet50_fpn_backbone_model(
            MaskRCNN,
            PretrainedModelNames.MASKRCNN_RESNET50_FPN_COCO,
            pretrained, progress, num_classes, pretrained_backbone,
            load_pretrained_model_dict, **kwargs)

    @staticmethod
    def resnet_fpn_backbone(backbone_name, pretrained, norm_layer=misc_nn_ops.FrozenBatchNorm2d, trainable_layers=3):
        """Get the resnet fpn backbone."""
        backbone = getattr(PretrainedModelFactory, backbone_name)(pretrained=pretrained,
                                                                  norm_layer=norm_layer)

        # select layers that wont be frozen
        assert trainable_layers <= 5 and trainable_layers >= 0
        layers_to_train = ['layer4', 'layer3', 'layer2', 'layer1', 'conv1'][:trainable_layers]
        # freeze layers only if pretrained backbone is used
        for name, parameter in backbone.named_parameters():
            if all([not name.startswith(layer) for layer in layers_to_train]):
                parameter.requires_grad_(False)

        return_layers = {'layer1': '0', 'layer2': '1', 'layer3': '2', 'layer4': '3'}

        in_channels_stage2 = backbone.inplanes // 8
        in_channels_list = [
            in_channels_stage2,
            in_channels_stage2 * 2,
            in_channels_stage2 * 4,
            in_channels_stage2 * 8,
        ]
        out_channels = 256
        return BackboneWithFPN(backbone, return_layers, in_channels_list, out_channels)

    @staticmethod
    def _resnet(arch, block, layers, pretrained, progress, **kwargs):
        model = ResNet(block, layers, **kwargs)
        if pretrained:
            # Note the eventual load_state_dict_from_url method already uses SHA256 hash to ensure the unique
            # file name and check the file content.
            state_dict = PretrainedModelFactory._load_state_dict_from_url_with_retry(
                PretrainedModelUrls.MODEL_URLS[arch], progress=progress)
            model.load_state_dict(state_dict)
        return model

    @staticmethod
    def _initialize_pretrained_model(model, num_classes, settings):
        assert num_classes == settings['num_classes'], \
            'num_classes should be {}, but is {}'.format(
                settings['num_classes'], num_classes)
        state_dict = PretrainedModelFactory._load_state_dict_from_url_with_retry(settings['url'])
        model.load_state_dict(state_dict)
        model.input_space = settings['input_space']
        model.input_size = settings['input_size']
        model.input_range = settings['input_range']
        model.mean = settings['mean']
        model.std = settings['std']
