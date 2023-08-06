# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Per class and Per sample metrics for classification using sklearn methods."""

from ignite.metrics import EpochMetric
from sklearn.metrics import fbeta_score, jaccard_similarity_score, precision_recall_fscore_support

from ..classification.common.constants import MetricsLiterals


def _sklearn_metrics_compute_fn_wrapper(detailed, include_per_sample_metrics):
    """
    :param detailed: flag indicating whether to compute detailed metrics
    :type detailed: bool
    :param include_per_sample_metrics: flag indicating whether to compute per sample metrics.
                                       Takes effect only when detailed is set to True.
    :type include_per_sample_metrics: bool
    :return: Dictionary of (MetricLiteral, metric values).
    """
    def sklearn_metrics_compute_fn(y_preds, y_targets):
        y_true = y_targets.numpy()
        y_pred = y_preds.numpy()

        # IoU
        metrics = {
            MetricsLiterals.IOU: jaccard_similarity_score(y_true, y_pred)
        }

        if detailed:
            if include_per_sample_metrics:
                # Per Sample metrics
                # Average: "samples" computes the average across samples.
                # Beta parameter determines the weight of recall in computed F-beta score from precision and recall.
                metrics.update({
                    MetricsLiterals.AVERAGE_SAMPLE_F1_SCORE: fbeta_score(y_true, y_pred, average="samples", beta=1.0),
                    MetricsLiterals.AVERAGE_SAMPLE_F2_SCORE: fbeta_score(y_true, y_pred, average="samples", beta=2.0)
                })

            # Per class(label) metrics
            # Average: "macro" computes the average across classes.
            combined_per_class_metric = precision_recall_fscore_support(y_true, y_pred, average="macro", beta=1.0)
            metrics.update({
                MetricsLiterals.AVERAGE_CLASS_PRECISION: combined_per_class_metric[0],
                MetricsLiterals.AVERAGE_CLASS_RECALL: combined_per_class_metric[1],
                MetricsLiterals.AVERAGE_CLASS_F1_SCORE: combined_per_class_metric[2]
            })
            metrics[MetricsLiterals.AVERAGE_CLASS_F2_SCORE] = fbeta_score(y_true, y_pred, average="macro", beta=2.0)

        return metrics
    return sklearn_metrics_compute_fn


class SkLearnMetrics(EpochMetric):
    """
    This metric calls fbeta_score, jaccard_similarity_score and precision_recall_fscore_support
    from sklearn.metrics to compute various per class and per sample metrics.
    Please see sklearn documentation for further details.
    """

    def __init__(self, detailed, include_per_sample_metrics, output_transform=lambda x: x):
        """
        :param detailed: flag indicating whether to compute detailed metrics
        :type detailed: bool
        :param include_per_sample_metrics: flag indicating whether to compute per sample metrics.
                                           Takes effect only when detailed is set to True.
        :type include_per_sample_metrics: bool
        :param output_transform: Callable to transform output into a format expected by the metric.
        :type output_transform (optional): callable
        """
        super(SkLearnMetrics, self).__init__(
            _sklearn_metrics_compute_fn_wrapper(detailed, include_per_sample_metrics),
            output_transform=output_transform)
