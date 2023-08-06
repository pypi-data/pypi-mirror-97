# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes that contain all the parameters associated with training
models. """


class StepLRSchedulerParameters:
    """Class that contains all parameters needed by Step learning rate scheduler."""

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional learning rate scheduler parameters. Currently supported parameters include:
          -step_size: Number of steps before changing learning rate
          -gamma: Rate at which to decrease the learning rate
        :type kwargs: dict
        """

        self._step_size = kwargs.get('step_size', None)
        self._gamma = kwargs.get('gamma', None)

    @property
    def step_size(self):
        """
        :return: step size
        :rtype: Int
        """
        return self._step_size

    @property
    def gamma(self):
        """
        :return: gamma
        :rtype: Int
        """
        return self._gamma


class WarmUpCosineLRSchedulerParameters:
    """Class that contains all parameters needed by warmup cosine learning rate scheduler."""

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional learning rate scheduler parameters. Currently supported parameters include:
          -warmup_steps: Number of steps to linearly increase the learning rate (warmup)
          -total_steps: Total number of steps in training.
          -cycles: A factor by which learning rate follows the cosine curve after warmup.
        """

        self._warmup_steps = kwargs.get("warmup_steps", None)
        self._total_steps = kwargs.get("total_steps", None)
        self._cycles = kwargs.get("cycles", None)

    @property
    def warmup_steps(self):
        """
        :return: warmup steps.
        :rtype: Int
        """
        return self._warmup_steps

    @property
    def total_steps(self):
        """
        :return: total steps.
        :rtype: Int
        """
        return self._total_steps

    @property
    def cycles(self):
        """
        :return: Cycles.
        :rtype: Float
        """
        return self._cycles
