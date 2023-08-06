from azureml.contrib.automl.dnn.vision.common.pretrained_model_utilities import PretrainedModelFactory
from azureml.contrib.automl.dnn.vision.object_detection.models.base_model_wrapper import \
    BaseObjectDetectionModelWrapper


class CocoBaseModelWrapper(BaseObjectDetectionModelWrapper):
    num_classes = 91

    def __init__(self):
        model = self._create_model()
        super().__init__(model=model, number_of_classes=CocoBaseModelWrapper.num_classes)

    def _create_model(self):
        return PretrainedModelFactory.fasterrcnn_resnet50_fpn(pretrained=True)
