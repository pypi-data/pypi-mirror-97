# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines a common interface for learning rate schedulers."""

from abc import ABC
from enum import Enum
import math
import torch.optim
from . import lrschedule_parameters
from .. import constants
from ..exceptions import AutoMLVisionSystemException
from azureml.automl.core.shared.exceptions import ClientException


class LRSchedulerUpdateType(Enum):
    """Type indicating when lr scheduler should be updated during training."""
    BATCH = 0
    EPOCH = 1


class BaseLRSchedulerWrapper(ABC):
    """Class that provides a common interface for all learning
    rate schedulers"""

    def __init__(self, optimizer, **kwargs):
        """
        :param optimizer: Optimizer the scheduler will operate on
        :type optimizer: Pytorch optimizer
        :param kwargs: Parameters that define learning rate scheduler
        :type kwargs: dict
        """
        self._lr_scheduler = None
        self._update_type = None

    @property
    def lr_scheduler(self):
        """Get the learning rate scheduler.

        :return: learning rate scheduler
        :rtype: pytoch learning rate scheduler
        """
        return self._lr_scheduler

    @property
    def update_type(self):
        """Get the scheduler update type.

        :return: scheduler update type.
        :rtype: LRSchedulerUpdateType
        """
        return self._update_type


class StepLRWrapper(BaseLRSchedulerWrapper):
    """Wrapper for Step Learning Rate Scheduler."""

    def __init__(self, optimizer, **kwargs):
        """
        :param optimizer: Optimizer the scheduler will operate on
        :type optimizer: Pytorch optimizer
        :param kwargs: Parameters that define learning rate scheduler. StepLR supports:
                            - step_size
                            - gamma
        :type kwargs: dict
        """

        lr_scheduler_parameters = lrschedule_parameters.StepLRSchedulerParameters(**kwargs)

        if lr_scheduler_parameters.step_size is None:
            raise AutoMLVisionSystemException("step_size is missing from lrschedule_parameters. "
                                              "Cannot use step lr scheduler.")
        if lr_scheduler_parameters.gamma is None:
            raise AutoMLVisionSystemException("gamma is missing from lrschedule_parameters. "
                                              "Cannot use step lr scheduler.")

        self._step_size = lr_scheduler_parameters.step_size
        self._gamma = lr_scheduler_parameters.gamma

        self._lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                             step_size=self._step_size,
                                                             gamma=self._gamma)
        self._update_type = LRSchedulerUpdateType.EPOCH


class WarmUpCosineLRWrapper(BaseLRSchedulerWrapper):
    """Wrapper for warmUp cosine learning rate scheduler. Linearly increases the lr from 0 to `initial_learning_rate`
    set in optimizer over `warmup_steps` number of training steps. Decreases the lr from `initial_learning_rate`
    over remaining `total_steps - warmup_steps` steps following a cosine curve.
    If `cycles` is 0.5, lr reaches 0 by end of total_steps.
    If `cycles` < 0.5, lr decreases following cosine curve, but doesn't reach 0 at end of total_steps.
    Please note that if `cycles` > 0.5, lr starts to increase after decrease to 0.
    """

    def __init__(self, optimizer, **kwargs):
        """
        :param optimizer: Optimizer the scheduler will operate on
        :type optimizer: Pytorch optimizer
        :param kwargs: Parameters that define learning rate scheduler. WarmUp Cosine LR Supports:
                            - warmup_steps
                            - total_steps
                            - cycles
        :type kwargs: dict
        """

        lr_scheduler_parameters = lrschedule_parameters.WarmUpCosineLRSchedulerParameters(**kwargs)

        if lr_scheduler_parameters.warmup_steps is None:
            raise AutoMLVisionSystemException("warmup_steps is missing from lrschedule_parameters. "
                                              "Cannot use warmUp cosine lr scheduler.")
        if lr_scheduler_parameters.total_steps is None:
            raise AutoMLVisionSystemException("total_steps is missing from lrschedule_parameters. "
                                              "Cannot use warmUp cosine lr scheduler.")
        if lr_scheduler_parameters.cycles is None:
            raise AutoMLVisionSystemException("cycles is missing from lrschedule_parameters. "
                                              "Cannot use warmUp cosine lr scheduler.")

        self._warmup_steps = lr_scheduler_parameters.warmup_steps
        self._total_steps = lr_scheduler_parameters.total_steps
        self._cycles = lr_scheduler_parameters.cycles

        self._lr_scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=self._lr_lambda)
        self._update_type = LRSchedulerUpdateType.BATCH

    def _lr_lambda(self, step):
        """Function to return the lr multiplicative factor to be used at step

        Note: This code has been copied from here:
        https://huggingface.co/transformers/v1.2.0/_modules/pytorch_transformers/optimization.html#WarmupCosineSchedule

        :param step: Current step
        :type step: Int
        :return: lr multiplicative factor
        :rtype: Float
        """
        if step < self._warmup_steps:
            return float(step) / float(max(1.0, self._warmup_steps))
        # progress after warmup
        progress = float(step - self._warmup_steps) / float(max(1, self._total_steps - self._warmup_steps))
        return max(0.0, 0.5 * (1. + math.cos(math.pi * float(self._cycles) * 2.0 * progress)))


class LRSchedulerFactory:
    """Factory class that produces different learning rate scheduler algorithms."""
    _scheduler_dict = {
        constants.LRSchedulerNames.STEP: StepLRWrapper,
        constants.LRSchedulerNames.WARMUP_COSINE: WarmUpCosineLRWrapper
    }

    def get_lr_scheduler(self, lr_scheduler_name, optimizer, **kwargs):
        """Construct and return a learning rate scheduler wrapper.

        :param lr_scheduler_name: Name of the learning rate scheduler
        :type lr_scheduler_name: String
        :param optimizer: Optimizer that scheduler will change learning rate for
        :type optimizer: Pytorch optimizer
        :param kwargs: Optional scheduler parameters
        :type kwargs: dict
        :returns: Learning rate scheduler wrapper
        :rtype: BaseLRSchedulerWrapper
        """

        if lr_scheduler_name is None:
            lr_scheduler_name = constants.LRSchedulerNames.DEFAULT_LR_SCHEDULER

        if lr_scheduler_name not in LRSchedulerFactory._scheduler_dict:
            raise ClientException('{} not supported'.format(lr_scheduler_name))\
                .with_generic_msg("Scheduler name not supported.")

        return LRSchedulerFactory._scheduler_dict[lr_scheduler_name](optimizer, **kwargs)


def setup_lr_scheduler(optimizer, scheduler=None, **kwargs):
    """Creates learning rate scheduler.

    :param optimizer: Optimizer that scheduler will operate on
    :type optimizer: Pytorch optimizer
    :param scheduler: (optional) Name of scheduler to use. Defaults to StepLR.
    :type scheduler: str
    :param kwargs: Optional scheduler parameters
    :type kwargs: dict
    :returns: Learning rate scheduler wrapper
    :rtype: BaseLRSchedulerWrapper
    """

    scheduler_factory = LRSchedulerFactory()

    return scheduler_factory.get_lr_scheduler(scheduler, optimizer, **kwargs)
