# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines literals and constants for the object detection part of the package."""

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.constants import (
    ArtifactLiterals, SettingsLiterals, DistributedLiterals, DistributedParameters,
    safe_to_log_vision_common_settings, safe_to_log_automl_settings
)


class CriterionNames:
    """String names for different loss functions."""
    FASTER_RCNN = "FASTER_RCNN"


class DataLoaderParameterLiterals:
    """String names for dataloader parameters."""
    BATCH_SIZE = "batch_size"
    SHUFFLE = "shuffle"
    NUM_WORKERS = "num_workers"
    DISTRIBUTED = "distributed"
    DROP_LAST = "drop_last"


class DataLoaderParameters:
    """Default parameters for dataloaders."""
    DEFAULT_BATCH_SIZE = 4
    DEFAULT_SHUFFLE = True
    DEFAULT_NUM_WORKERS = None
    DEFAULT_DISTRIBUTED = False
    DEFAULT_DROP_LAST = False


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
    POLYGON = "polygon"


class LearningParameters:
    """Default learning parameters."""
    SGD_DEFAULT_LEARNING_RATE = 0.005
    SGD_DEFAULT_MOMENTUM = 0.9
    SGD_DEFAULT_WEIGHT_DECAY = 0.0001


class ModelNames:
    """String names for model backbones."""
    FASTER_RCNN_RESNET50_FPN = "fasterrcnn_resnet50_fpn"
    FASTER_RCNN_RESNET18_FPN = "fasterrcnn_resnet18_fpn"
    FASTER_RCNN_MOBILENETV2 = "fasterrcnn_mobilenet_v2"
    MASK_RCNN_RESNET50_FPN = "maskrcnn_resnet50_fpn"
    YOLO_V5 = "yolov5"


class OutputFields:
    """Keys for the outputs of the object detection network."""
    BOXES_LABEL = "boxes"
    CLASSES_LABEL = "labels"
    SCORES_LABEL = "scores"
    VOCMAP_RESULT = "vocmap_result"


class OptimizerNames:
    """String names and defaults for optimizers."""
    DEFAULT_OPTIMIZER = "SGD"
    SGD = "SGD"


class RCNNBackbones:
    """String keys for the different faster rcnn backbones."""
    RESNET_50_FPN_BACKBONE = "resnet50fpn"
    RESNET_18_FPN_BACKBONE = "resnet18fpn"
    RESNET_152_FPN_BACKBONE = "resnet152fpn"
    MOBILENET_V2_BACKBONE = "mobilenet_v2"


class RCNNSpecifications:
    """String keys for different faster rcnn speficiations"""
    BACKBONE = "backbone"
    DEFAULT_BACKBONE = RCNNBackbones.RESNET_50_FPN_BACKBONE
    RESNET_FPN_BACKBONES = [RCNNBackbones.RESNET_18_FPN_BACKBONE,
                            RCNNBackbones.RESNET_50_FPN_BACKBONE,
                            RCNNBackbones.RESNET_152_FPN_BACKBONE]
    CNN_BACKBONES = [RCNNBackbones.MOBILENET_V2_BACKBONE]


class ValidationMetricType:
    """ Metric computation method to use for validation metrics."""
    NONE = "none"
    COCO = "coco"
    VOC = "voc"
    COCO_VOC = "coco_voc"

    ALL_COCO = [COCO, COCO_VOC]
    ALL_VOC = [VOC, COCO_VOC]
    ALL_TYPES = [NONE, COCO, VOC, COCO_VOC]


class SchedulerParameters:
    """Default learning rate scheduler parameters."""
    DEFAULT_STEP_LR_STEP_SIZE = 3
    DEFAULT_STEP_LR_GAMMA = 0.5
    DEFAULT_WARMUP_COSINE_LR_CYCLES = 0.45


class TrainingParameters:
    """Default training parameters."""
    DEFAULT_NUMBER_EPOCHS = 15
    DEFAULT_TRAINING_BATCH_SIZE = 2
    DEFAULT_VALIDATION_BATCH_SIZE = 1
    DEFAULT_PATIENCE_ITERATIONS = 3
    DEFAULT_PRIMARY_METRIC = "mean_average_precision"
    DEFAULT_EARLY_STOP_DELAY_ITERATIONS = 3
    DEFAULT_VALIDATION_METRIC_TYPE = ValidationMetricType.VOC


class TrainingLiterals:
    """String keys for training parameters."""
    PRIMARY_METRIC = "primary_metric"
    NUMBER_OF_EPOCHS = "number_of_epochs"
    MAX_PATIENCE_ITERATIONS = "max_patience_iterations"
    LEARNING_RATE = "learning_rate"
    LR = "lr"
    MOMENTUM = "momentum"
    WEIGHT_DECAY = "weight_decay"
    STEP_SIZE = "step_size"
    GAMMA = "gamma"
    TRAINING_BATCH_SIZE = "training_batch_size"
    VALIDATION_BATCH_SIZE = "validation_batch_size"
    EARLY_STOP_DELAY_ITERATIONS = "early_stop_delay_iterations"
    VALIDATION_METRIC_TYPE = "validation_metric_type"


class PredictionLiterals:
    """Strings that will be keys in the output json during prediction."""
    BOX = 'box'
    BOXES = 'boxes'
    FILENAME = 'filename'
    LABEL = 'label'
    SCORE = 'score'


training_settings_defaults = {
    TrainingLiterals.PRIMARY_METRIC: TrainingParameters.DEFAULT_PRIMARY_METRIC,
    SettingsLiterals.DEVICE: utils._get_default_device(),
    SettingsLiterals.IGNORE_DATA_ERRORS: True,
    SettingsLiterals.NUM_WORKERS: 4,
    SettingsLiterals.ENABLE_ONNX_NORMALIZATION: False,
    DistributedLiterals.DISTRIBUTED: DistributedParameters.DEFAULT_DISTRIBUTED,
    DistributedLiterals.MASTER_ADDR: DistributedParameters.DEFAULT_MASTER_ADDR,
    DistributedLiterals.MASTER_PORT: DistributedParameters.DEFAULT_MASTER_PORT,
    SettingsLiterals.OUTPUT_DIR: ArtifactLiterals.OUTPUT_DIR,
    SettingsLiterals.OUTPUT_SCORING: False,
    SettingsLiterals.VALIDATE_SCORING: False,
    TrainingLiterals.VALIDATION_METRIC_TYPE: TrainingParameters.DEFAULT_VALIDATION_METRIC_TYPE,
    SettingsLiterals.LOG_SCORING_FILE_INFO: False
}


class ScoringParameters:
    """Default scoring parameters."""
    DEFAULT_SCORING_BATCH_SIZE = 2
    DEFAULT_NUM_WORKERS = 4


class FasterRCNNLiterals:
    """String keys for FasterRCNN parameters."""
    MIN_SIZE = "min_size"
    BOX_SCORE_THRESH = "box_score_thresh"
    BOX_NMS_THRESH = "box_nms_thresh"
    BOX_DETECTIONS_PER_IMG = "box_detections_per_img"


class FasterRCNNParameters:
    """Default FasterRCNN parameters."""
    DEFAULT_MIN_SIZE = 600
    DEFAULT_BOX_SCORE_THRESH = 0.3
    DEFAULT_BOX_NMS_THRESH = 0.5
    DEFAULT_BOX_DETECTIONS_PER_IMG = 100


class MaskRCNNLiterals:
    """String keys for MaskRCNN parameters."""
    MASK_PREDICTOR_HIDDEN_DIM = "mask_predictor_hidden_dim"


class MaskRCNNParameters:
    """Default MaskRCNN parameters."""
    DEFAULT_MASK_PREDICTOR_HIDDEN_DIM = 256


class MaskToolsParameters:
    """Default values for mask tool parameters."""
    DEFAULT_MASK_PIXEL_SCORE_THRESHOLD = 0.5
    DEFAULT_MAX_NUMBER_OF_POLYGON_SIMPLIFICATIONS = 25
    DEFAULT_MAX_NUMBER_OF_POLYGON_POINTS = 100
    DEFAULT_MASK_SAFETY_PADDING = 1


class PredefinedLiterals:
    """Predefined string literals"""
    BG_LABEL = "--bg--"


# not safe: 'data_folder', 'labels_file_root', 'path'
safe_to_log_vision_od_settings = {
    TrainingLiterals.PRIMARY_METRIC,
    TrainingLiterals.EARLY_STOP_DELAY_ITERATIONS,
    TrainingLiterals.GAMMA,
    TrainingLiterals.LEARNING_RATE,
    TrainingLiterals.LR,
    TrainingLiterals.MAX_PATIENCE_ITERATIONS,
    TrainingLiterals.MOMENTUM,
    TrainingLiterals.NUMBER_OF_EPOCHS,
    TrainingLiterals.STEP_SIZE,
    TrainingLiterals.TRAINING_BATCH_SIZE,
    TrainingLiterals.VALIDATION_BATCH_SIZE,
    TrainingLiterals.VALIDATION_METRIC_TYPE,
    TrainingLiterals.WEIGHT_DECAY,

    DistributedLiterals.DISTRIBUTED,
    DistributedLiterals.MASTER_ADDR,
    DistributedLiterals.MASTER_PORT,
    DistributedLiterals.WORLD_SIZE,

    FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG,
    FasterRCNNLiterals.BOX_NMS_THRESH,
    FasterRCNNLiterals.BOX_SCORE_THRESH,
    FasterRCNNLiterals.MIN_SIZE,
}

safe_to_log_settings = \
    safe_to_log_automl_settings | \
    safe_to_log_vision_common_settings | \
    safe_to_log_vision_od_settings
