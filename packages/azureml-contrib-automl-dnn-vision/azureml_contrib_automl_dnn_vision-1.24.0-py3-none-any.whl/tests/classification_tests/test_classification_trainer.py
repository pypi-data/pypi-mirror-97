import pytest

from azureml.contrib.automl.dnn.vision.classification.common.constants import ModelNames
from azureml.contrib.automl.dnn.vision.classification.io.read.dataloader import _get_data_loader
from azureml.contrib.automl.dnn.vision.classification.models.classification_model_wrappers import ModelFactory
from azureml.contrib.automl.dnn.vision.classification.trainer.trainer import _validate
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException
from azureml.contrib.automl.dnn.vision.metrics import ClassificationMetrics

from ..common.run_mock import ClassificationDatasetWrapperMock


@pytest.mark.usefixtures('new_clean_dir')
class TestClassificationTrainer:
    def test_validate_with_invalid_dataset(self):
        # All values in the dataset are invalid
        num_classes = 3
        dataset = ClassificationDatasetWrapperMock([None, None, None, None], num_classes)
        dataloader = _get_data_loader(dataset, transform_fn=None, batch_size=10, num_workers=0)
        metrics = ClassificationMetrics(num_classes=num_classes, multilabel=False)
        model_wrapper = ModelFactory().get_model_wrapper(ModelNames.SERESNEXT, num_classes=num_classes,
                                                         multilabel=False)
        # Should raise exception when all images in validation dataset are invalid
        with pytest.raises(AutoMLVisionDataException):
            _validate(model_wrapper, dataloader=dataloader, metrics=metrics)
