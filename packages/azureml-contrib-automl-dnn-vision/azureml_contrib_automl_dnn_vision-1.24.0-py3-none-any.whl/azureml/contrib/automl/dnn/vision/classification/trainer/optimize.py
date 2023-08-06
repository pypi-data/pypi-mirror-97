# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines functions related to optimization."""
from azureml.automl.core.shared.exceptions import ClientException

try:
    from torch import nn
    import torch.optim as optim
    import torch
    import torch.nn.functional as F
except ImportError:
    print('ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and '
          'pytorch-ignite separately before running the package.')
from ..common.constants import TrainingLiterals
from ..common.classification_utils import _get_model_params
from ...common import distributed_utils
from ...common.constants import LRSchedulerNames
from ...common.trainer import lrschedule


class FocalLoss(nn.Module):
    """Criterion that computes Focal loss based on https://arxiv.org/pdf/1708.02002.pdf
        variant of nn.CrossEntropyLoss
        FL(p_t) = -alpha_t * (1 - p_t)^gamma * log(p_t), p_t is the model's estimated probability for each class.
    """

    def __init__(self, gamma=2., alpha=1):
        """
        :param gamma: focusing parameter
        :type gamma: float
        :param alpha: balancing parameter
        :type alpha: float
        """
        nn.Module.__init__(self)
        self.gamma = gamma
        self.alpha = alpha

    def forward(self, input, target):
        """
        :param input: logics from the model
        :type input: torch tensor
        :param target: labels
        :type target: torch tensor
        """
        log_prob = F.log_softmax(input, dim=-1)
        prob = torch.exp(log_prob)
        return F.nll_loss((self.alpha * ((1 - prob) ** self.gamma)) * log_prob, target)


def _get_sgd_params(strategy, last_layer_params=None, other_layers_params=None, batchnorm_params=None,
                    lr=None, weight_decay=None, last_layer_lr=None):
    if strategy == TrainingLiterals.FIT_LAST:
        sgd_params = [
            {
                TrainingLiterals.PARAMS: last_layer_params,
                TrainingLiterals.LR: lr,
                TrainingLiterals.WEIGHT_DECAY: weight_decay
            }
        ]
    elif strategy == TrainingLiterals.DIFF_LR:
        sgd_params = [
            {
                TrainingLiterals.PARAMS: last_layer_params,
                TrainingLiterals.LR: last_layer_lr,
                TrainingLiterals.WEIGHT_DECAY: weight_decay
            },
            {
                TrainingLiterals.PARAMS: other_layers_params,
                TrainingLiterals.LR: lr,
                TrainingLiterals.WEIGHT_DECAY: weight_decay
            },
            {
                TrainingLiterals.PARAMS: batchnorm_params,
                TrainingLiterals.LR: lr,
                TrainingLiterals.WEIGHT_DECAY: 0.
            }
        ]
    else:
        raise ClientException('invalid strategy passed', has_pii=False)

    return sgd_params


def _get_optimizer(model_wrapper, settings, strategy=TrainingLiterals.DIFF_LR):
    """Get torch optimizer.

    :param model_wrapper: model wrapper object
    :type model_wrapper: azureml.contrib.automl.dnn.vision.base_model_wrapper.BaseModelWrapper
    :param settings: dictionary containing settings for training
    :type settings: dict
    :param strategy: training strategy
    :type strategy: str
    :return: get optimizer
    :rtype: torch.optim.Optimizer object
    """
    last_layer, other_layers, batchnorm = _get_model_params(model_wrapper.model, model_wrapper.name)
    lr = settings[TrainingLiterals.LR] * distributed_utils.get_world_size()
    momentum = settings[TrainingLiterals.MOMENTUM]
    weight_decay = settings[TrainingLiterals.WEIGHT_DECAY]
    last_layer_lr = settings[TrainingLiterals.LAST_LAYER_LR] * distributed_utils.get_world_size()
    params = _get_sgd_params(strategy, last_layer_params=last_layer, other_layers_params=other_layers,
                             batchnorm_params=batchnorm, lr=lr, weight_decay=weight_decay, last_layer_lr=last_layer_lr)
    return optim.SGD(params, lr=lr, momentum=momentum, weight_decay=weight_decay, nesterov=True)


def _get_lr_scheduler(optimizer, settings, num_epochs, batches_per_epoch):
    """Get torch lr scheduler.

    :param optimizer: optimizer for model training
    :type: torch.optim.Optimizer object
    :param settings: dictionary containing settings for training
    :type settings: dict
    :param num_epochs: Number of epochs in the training process
    :type num_epochs: int
    :param batches_per_epoch: Number of batches in an epoch
    :type: batches_per_epoch: int
    :return: lr_scheduler
    :rtype: common.trainer.BaseLRSchedulerWrapper object
    """
    lr_scheduler_settings = {
        "warmup_steps": batches_per_epoch * 2,
        "total_steps": num_epochs * batches_per_epoch,
        "cycles": settings[TrainingLiterals.WARMUP_COSINE_LR_CYCLES]
    }
    lr_scheduler = lrschedule.setup_lr_scheduler(
        optimizer, LRSchedulerNames.WARMUP_COSINE, **lr_scheduler_settings)
    return lr_scheduler


def _get_criterion(multilabel=False, class_weights=None):
    """Get torch criterion.

    :param multilabel: flag indicating if it is a multilabel problem or not.
    :type multilabel: bool
    :param class_weights: class-level rescaling weights
    :type class_weights: torch.Tensor
    :return: torch criterion
    :rtype: object from one of torch.nn criterion classes
    """
    if multilabel:
        criterion = nn.BCEWithLogitsLoss()
    else:
        criterion = nn.CrossEntropyLoss(weight=class_weights)
    return criterion
