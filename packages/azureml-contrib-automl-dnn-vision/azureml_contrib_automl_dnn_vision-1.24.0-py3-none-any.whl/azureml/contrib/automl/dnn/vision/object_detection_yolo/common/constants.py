# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" Defines literals and constants for the object detection part of the package """

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.constants import SettingsLiterals
from azureml.contrib.automl.dnn.vision.object_detection.common.constants import ModelNames


class DatasetFieldLabels:
    """Keys for input datasets."""
    X_0_PERCENT = "topX"
    Y_0_PERCENT = "topY"
    X_1_PERCENT = "bottomX"
    Y_1_PERCENT = "bottomY"
    IS_CROWD = "isCrowd"
    IMAGE_URL = "imageUrl"
    IMAGE_DETAILS = "imageDetails"
    IMAGE_LABEL = "label"
    CLASS_LABEL = "label"
    WIDTH = "width"
    HEIGHT = "height"


class TrainingParameters:
    """Default training parameters."""
    DEFAULT_NUMBER_EPOCHS = 30
    DEFAULT_TRAINING_BATCH_SIZE = 16
    DEFAULT_VALIDATION_BATCH_SIZE = 16
    DEFAULT_PATIENCE_ITERATIONS = 3
    DEFAULT_PRIMARY_METRIC = "mean_average_precision"
    DEFAULT_LEARNING_RATE = 0.01


class TrainingLiterals:
    """String keys for training parameters."""
    PRIMARY_METRIC = "primary_metric"
    NUMBER_OF_EPOCHS = "number_of_epochs"
    MAX_PATIENCE_ITERATIONS = "max_patience_iterations"
    TRAINING_BATCH_SIZE = "training_batch_size"
    VALIDATION_BATCH_SIZE = "validation_batch_size"
    LEARNING_RATE = "learning_rate"
    SCORING_BOX_SCORE_THRESH = "scoring_box_score_thresh"
    SCORING_BOX_IOU_THRESH = "scoring_box_iou_thresh"


class ScoringParameters:
    """Default scoring parameters."""
    DEFAULT_SCORING_BATCH_SIZE = 16
    DEFAULT_NUM_WORKERS = 8
    DEFAULT_BOX_SCORE_THRESH = 0.4
    DEFAULT_BOX_IOU_THRESH = 0.5


yolo_hyp_defaults = {
    'momentum': 0.937,  # SGD momentum/Adam beta1
    'weight_decay': 1e-4,  # 5e-4,  # optimizer weight decay
    'giou': 0.05,  # giou loss gain
    'cls': 0.58,  # cls loss gain
    'cls_pw': 1.0,  # cls BCELoss positive_weight
    'obj': 1.0,  # obj loss gain (*=img_size/320 if img_size != 320)
    'obj_pw': 1.0,  # obj BCELoss positive_weight
    'anchor_t': 4.0,  # anchor-multiple threshold
    'fl_gamma': 0.0,  # focal loss gamma (efficientDet default is gamma=1.5)
    'degrees': 0.0,  # image rotation (+/- deg)
    'translate': 0.0,  # image translation (+/- fraction)
    'scale': 0.5,  # image scale (+/- gain)
    'shear': 0.0,  # image shear (+/- deg)
    'gs': 32}  # grid size


class YoloLiterals:
    """String keys for Yolov5 parameters."""
    IMG_SIZE = "img_size"
    MODEL_SIZE = 'model_size'
    MULTI_SCALE = "multi_scale"
    BOX_SCORE_THRESH = "box_score_thresh"
    BOX_IOU_THRESH = "box_iou_thresh"
    MODELS = 'models'


class YoloParameters:
    """Default Yolov5 parameters."""
    DEFAULT_IMG_SIZE = 640
    DEFAULT_MODEL_SIZE = 'medium'
    DEFAULT_MODEL_VERSION = '5.3.0'


training_settings_defaults = {
    TrainingLiterals.PRIMARY_METRIC: TrainingParameters.DEFAULT_PRIMARY_METRIC,
    SettingsLiterals.DEVICE: utils._get_default_device(),
    SettingsLiterals.IGNORE_DATA_ERRORS: True,
    SettingsLiterals.MODEL_NAME: ModelNames.YOLO_V5,
    SettingsLiterals.NUM_WORKERS: 8,
    SettingsLiterals.ENABLE_ONNX_NORMALIZATION: False,
    YoloLiterals.BOX_IOU_THRESH: 0.5,
    YoloLiterals.BOX_SCORE_THRESH: 0.001,
    SettingsLiterals.VALIDATE_SCORING: False,
    SettingsLiterals.OUTPUT_SCORING: False,
    SettingsLiterals.LOG_SCORING_FILE_INFO: False,
    TrainingLiterals.SCORING_BOX_IOU_THRESH: ScoringParameters.DEFAULT_BOX_IOU_THRESH,
    TrainingLiterals.SCORING_BOX_SCORE_THRESH: ScoringParameters.DEFAULT_BOX_SCORE_THRESH
}
