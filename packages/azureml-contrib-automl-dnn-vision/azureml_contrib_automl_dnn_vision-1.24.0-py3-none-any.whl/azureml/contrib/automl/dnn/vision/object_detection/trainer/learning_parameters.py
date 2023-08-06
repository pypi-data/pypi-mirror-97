# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes that contain all the parameters assocaiated with training
models. """


class OptimizerParameters:
    """Class that contains all parameters assocatiated with the optimizer."""

    def __init__(self, **kwargs):
        """
        :param kwargs: Dictionary of optional keyword parameters. Currently supported include:
          -lr: learning rate
          -momentum: momentum
          -weight_decay: weight decay
        :type kwargs: dict
        """
        self._learning_rate = kwargs.get('lr', None)
        self._momentum = kwargs.get('momentum', None)
        self._weight_decay = kwargs.get('weight_decay', None)

    @property
    def learning_rate(self):
        """Get learning rate

        :returns: learning rate
        :rtype: float
        """
        return self._learning_rate

    @property
    def momentum(self):
        """Get momentum

        :returns: momentum
        :rtype: float
        """
        return self._momentum

    @property
    def weight_decay(self):
        """Get weight decay

        :returns: weight decay
        :rtype: float
        """
        return self._weight_decay
