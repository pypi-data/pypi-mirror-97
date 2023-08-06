# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classification metrics for the package."""

from itertools import chain

try:
    from ignite.metrics import Accuracy, Precision, Recall
    from ignite.contrib.metrics import AveragePrecision
    import torch
except ImportError:
    print("ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and "
          "pytorch-ignite separately before running the package.")
from ..classification.common.constants import MetricsLiterals
from .sklearn_metrics import SkLearnMetrics
from ..common.logging_utils import get_logger


logger = get_logger(__name__)


class ClassificationMetrics:
    """Class to calculate classification metrics.

    This class is modeled on the ignite Metrics class. Enabling us to compute metrics per batch,
    aggregate them and compute them only at the end. This is done without saving the full list of
    predictions.

    For multilabel, input predictions are supposed to be one hot encoded already. Since this is required for data
    loader to stack multiple tensors of labels anyways. For multiclass, prediction is a single column tensor of the
    predictions.
    """
    def __init__(self, num_classes=2, multilabel=False, detailed=True):
        """
        :param num_classes: number of classes
        :type num_classes: int
        :param multilabel: flag indicating whether this is multilabel problem
        :type multilabel: bool
        :param detailed: flag indicating whether to compute detailed metrics
        :type detailed: bool
        """
        self._multilabel = multilabel
        self._num_classes = num_classes
        self._unsupported_metrics = set([])

        if not multilabel and self._num_classes > 2:
            # sklearn.metrics.average_precision_score is not supported for multi-class cases.
            self._prob_metrics = {}
            self._unsupported_metrics.add(MetricsLiterals.AVERAGE_PRECISION)
        else:
            self._prob_metrics = {
                MetricsLiterals.AVERAGE_PRECISION: AveragePrecision(_get_single_column_label) if multilabel else
                AveragePrecision(),
            }

        self._pred_metrics = {
            MetricsLiterals.ACCURACY: Accuracy()
        }

        if self._num_classes == 1 and self._multilabel:
            self._unsupported_metrics.update([MetricsLiterals.PRECISION, MetricsLiterals.RECALL])
        else:
            self._pred_metrics.update({
                MetricsLiterals.PRECISION: Precision(is_multilabel=multilabel, average=True),
                MetricsLiterals.RECALL: Recall(is_multilabel=multilabel, average=True),
            })

        include_per_sample_metrics = self._num_classes != 1
        if not include_per_sample_metrics:
            self._unsupported_metrics.update([MetricsLiterals.AVERAGE_SAMPLE_F1_SCORE,
                                              MetricsLiterals.AVERAGE_SAMPLE_F2_SCORE])
        self._sklearn_pred_metrics = {
            MetricsLiterals.SKLEARN_METRICS: SkLearnMetrics(detailed, include_per_sample_metrics)
        }

        if self._unsupported_metrics:
            logger.warning("Metrics not supported in current configuration: {}.".format(self._unsupported_metrics))

    def metric_supported(self, metric):
        """ Check if a metric is supported.

        :param metric: Name of the metric.
        :type metric: MetricsLiterals
        :return: Boolean indicating whether a metric is supported.
        """
        return metric not in self._unsupported_metrics

    def _get_one_hot_labels(self, preds=None, num_classes=None):
        """
        :param preds: predictions
        :type preds: torch.Tensor
        :param num_classes: number of classes
        :type num_classes: int
        :return: one hot encoded predictions
        :rtype: torch.Tensor
        """
        y = torch.zeros(preds.shape[0], num_classes).to(preds.device)
        return y.scatter_(1, preds.reshape(-1, 1), 1)

    def reset(self):
        """Resets batch metric."""
        for _, metric in chain(self._pred_metrics.items(), self._prob_metrics.items(),
                               self._sklearn_pred_metrics.items()):
            metric.reset()

    def update(self, probs=None, preds=None, labels=None):
        """Update the metrics.

        :param probs: probabilities
        :type probs: torch.Tensor
        :param preds: predictions
        :type preds: torch.Tensor
        :param labels: labels
        :type labels: torch.Tensor
        """
        for _, metric in self._pred_metrics.items():
            if self._num_classes > 2 and not self._multilabel:
                # since pytorch-ignite takes probs as input for >2 classes
                metric.update((probs, labels))
            else:
                metric.update((preds, labels))

        if not self._multilabel:
            labels = self._get_one_hot_labels(labels, num_classes=self._num_classes)
            # since preds are 1D array in this case.
            preds = self._get_one_hot_labels(preds, num_classes=self._num_classes)

        for _, metric in self._sklearn_pred_metrics.items():
            metric.update((preds, labels))

        for _, metric in self._prob_metrics.items():
            metric.update((probs, labels))

    def compute(self):
        """Compute the metrics."""
        metrics = {}
        for name, metric in chain(self._pred_metrics.items(), self._prob_metrics.items()):
            metrics[name] = round(metric.compute() * 100, 3)

        for name, metric in self._sklearn_pred_metrics.items():
            metrics[name] = metric.compute()
            if isinstance(metrics[name], dict):
                metrics[name] = {key: (round(value * 100, 3) if value is not None else None)
                                 for key, value in metrics[name].items()}
            else:
                metrics[name] = round(metrics[name] * 100, 3)

        if MetricsLiterals.SKLEARN_METRICS in metrics:
            metrics.update(metrics[MetricsLiterals.SKLEARN_METRICS])
            metrics.pop(MetricsLiterals.SKLEARN_METRICS)

        return metrics


def _get_single_column_label(output):
    y_prob, y_truth = output
    return y_prob.view(-1), y_truth.view(-1)
