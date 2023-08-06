import pytest
import torch

from azureml.contrib.automl.dnn.vision.metrics import ClassificationMetrics
from azureml.contrib.automl.dnn.vision.classification.common.constants import MetricsLiterals


@pytest.mark.usefixtures("new_clean_dir")
class TestClassificationMetrics:
    def test_binary_classification(self):
        y_probs = torch.rand(10, 2)
        y_pred = torch.randint(0, 2, size=(10,)).type(torch.LongTensor)
        y = torch.randint(0, 2, size=(10,)).type(torch.LongTensor)
        metrics = ClassificationMetrics(num_classes=2)
        assert not metrics._unsupported_metrics
        metrics.update(probs=y_probs, preds=y_pred, labels=y)

        metrics.compute()

        assert True

    def test_binary_multilabel(self):
        y_probs = torch.rand(10, 2)
        y_pred = torch.zeros(10, 2)
        y_pred[:, 0] = torch.randint(0, 2, size=(10,)).type(torch.LongTensor)
        y_pred[:, 1] = 1 - y_pred[:, 0]
        y = torch.randint(0, 2, size=(10, 2)).type(torch.LongTensor)

        metrics = ClassificationMetrics(num_classes=2, multilabel=True)
        assert not metrics._unsupported_metrics
        metrics.update(probs=y_probs, preds=y_pred, labels=y)

        metrics.compute()

        assert True

    def test_multiclass(self):
        y_probs = torch.rand(10, 4)
        y_pred = torch.randint(0, 4, size=(10,)).type(torch.LongTensor)

        y = torch.randint(0, 4, size=(10,)).type(torch.LongTensor)

        metrics = ClassificationMetrics(num_classes=4, multilabel=False)
        assert not metrics.metric_supported(MetricsLiterals.AVERAGE_PRECISION)
        metrics.update(probs=y_probs, preds=y_pred, labels=y)

        metrics.compute()

        assert True

    def test_multilabel_not_binary(self):
        y_probs = torch.rand(10, 4)
        y_pred = torch.randint(0, 2, size=(10, 4))
        y = torch.randint(0, 1, size=(10, 4)).type(torch.LongTensor)

        metrics = ClassificationMetrics(num_classes=4, multilabel=True)
        assert not metrics._unsupported_metrics
        metrics.update(probs=y_probs, preds=y_pred, labels=y)

        metrics.compute()

        assert True

    def test_multiclass_single_label(self):
        # Number of labels can be 1 if all images were labelled with same label.
        y_probs = torch.rand(10, 1)
        y_pred = torch.zeros(10, 1, dtype=torch.long)
        y = torch.zeros(10, 1, dtype=torch.long)

        metrics = ClassificationMetrics(num_classes=1, multilabel=False)
        assert not metrics.metric_supported(MetricsLiterals.AVERAGE_SAMPLE_F1_SCORE)
        assert not metrics.metric_supported(MetricsLiterals.AVERAGE_SAMPLE_F2_SCORE)
        metrics.update(probs=y_probs, preds=y_pred, labels=y)

        metrics.compute()

        assert True

    def test_multilabel_single_label(self):
        # Number of labels can be 1 if all images were labelled with same label.
        y_probs = torch.rand(10, 1)
        y_pred = torch.zeros((10, 1))
        y = torch.zeros((10, 1))

        metrics = ClassificationMetrics(num_classes=1, multilabel=True)
        assert not metrics.metric_supported(MetricsLiterals.PRECISION)
        assert not metrics.metric_supported(MetricsLiterals.RECALL)
        assert not metrics.metric_supported(MetricsLiterals.AVERAGE_SAMPLE_F1_SCORE)
        assert not metrics.metric_supported(MetricsLiterals.AVERAGE_SAMPLE_F2_SCORE)
        metrics.update(probs=y_probs, preds=y_pred, labels=y)

        metrics.compute()

        assert True
