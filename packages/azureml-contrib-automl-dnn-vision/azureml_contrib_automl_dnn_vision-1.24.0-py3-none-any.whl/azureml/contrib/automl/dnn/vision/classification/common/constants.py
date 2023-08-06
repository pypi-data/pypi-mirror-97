# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines literals and constants for the classification part of the package."""

try:
    import torch
except ImportError:
    print('ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and '
          'pytorch-ignite separately before running the package.')

from azureml.contrib.automl.dnn.vision.common.constants import (
    ArtifactLiterals, DistributedLiterals,
    DistributedParameters, SettingsLiterals,
    safe_to_log_vision_common_settings, safe_to_log_automl_settings
)


class MetricsLiterals:
    """String key names for metrics."""
    ACCURACY = 'accuracy'
    PRECISION = 'precision'
    RECALL = 'recall'
    AVERAGE_PRECISION = 'average_precision'
    ACCURACY_TOP5 = 'accuracy_top5'
    SKLEARN_METRICS = 'sklearn_metrics'
    IOU = 'iou'
    AVERAGE_SAMPLE_F1_SCORE = 'average_sample_f1_score'
    AVERAGE_SAMPLE_F2_SCORE = 'average_sample_f2_score'
    AVERAGE_CLASS_PRECISION = 'average_class_precision'
    AVERAGE_CLASS_RECALL = 'average_class_recall'
    AVERAGE_CLASS_F1_SCORE = 'average_class_f1_score'
    AVERAGE_CLASS_F2_SCORE = 'average_class_f2_score'


class PredictionLiterals:
    """Strings that will be keys in the output json during prediction."""
    FEATURE_VECTOR = 'feature_vector'
    FILENAME = 'filename'
    LABELS = 'labels'
    PROBS = 'probs'


class TrainingLiterals:
    """String keys for training parameters."""
    BATCH_SIZE = 'batch_size'
    # Report detailed metrics like per class/sample f1, f2, precision, recall scores.
    DETAILED_METRICS = 'detailed_metrics'
    DIFF_LR = 'diff_lr'
    EARLY_STOPPING_PATIENCE = 'early_stopping_patience'
    FIT_LAST = 'fit_last'
    # data imbalance ratio (#data from largest class /#data from smallest class)
    IMBALANCE_RATE_THRESHOLD = "imbalance_rate_threshold"
    LAST_LAYER_LR = 'last_layer_lr'
    LR = 'lr'
    MOMENTUM = 'momentum'
    NUM_EPOCHS = 'epochs'
    # allow oversampling from small classes when imbalance_rate above IMBALANCE_RATE_THRESHOLD
    OVERSAMPLE = 'oversample'
    PARAMS = 'params'
    PRIMARY_METRIC = 'primary_metric'
    STEP_LR_GAMMA = 'step_lr_gamma'
    STEP_LR_STEP_SIZE = 'step_lr_step_size'
    STRATEGY = 'strategy'
    TEST_RATIO = 'test_ratio'
    VALIDATION_BATCH_SIZE = 'validation_batch_size'
    WEIGHT_DECAY = 'weight_decay'
    # applying rescaling class-level weights for CrossEntropyLoss()
    WEIGHTED_LOSS = 'weighted_loss'
    WARMUP_COSINE_LR_CYCLES = "warmup_cosine_lr_cycles"


class LoggingLiterals:
    """Literals that help logging and correlating different training runs."""
    PROJECT_ID = 'project_id'
    VERSION_NUMBER = 'version_number'
    TASK_TYPE = 'task_type'


class ModelNames:
    """Currently supported model names."""
    RESNET18 = 'resnet18'
    RESNET50 = 'resnet50'
    MOBILENETV2 = 'mobilenetv2'
    SERESNEXT = 'seresnext'


class PackageInfo:
    """Contains package details."""
    PYTHON_VERSION = '3.6'
    CONDA_PACKAGE_NAMES = ['pip']
    PIP_PACKAGE_NAMES = ['azureml-contrib-automl-dnn-vision']


base_training_settings_defaults = {
    TrainingLiterals.STRATEGY: TrainingLiterals.DIFF_LR,
    SettingsLiterals.LABELS_FILE_ROOT: '',
    SettingsLiterals.DATA_FOLDER: '',
    TrainingLiterals.BATCH_SIZE: 78,
    TrainingLiterals.VALIDATION_BATCH_SIZE: 78,
    SettingsLiterals.DEVICE: torch.device("cuda:0" if torch.cuda.is_available() else "cpu"),
    TrainingLiterals.EARLY_STOPPING_PATIENCE: 5,
    SettingsLiterals.IGNORE_DATA_ERRORS: True,
    TrainingLiterals.IMBALANCE_RATE_THRESHOLD: 2,
    SettingsLiterals.MULTILABEL: False,
    TrainingLiterals.NUM_EPOCHS: 15,
    SettingsLiterals.OUTPUT_DIR: ArtifactLiterals.OUTPUT_DIR,
    TrainingLiterals.OVERSAMPLE: False,
    TrainingLiterals.TEST_RATIO: 0.2,
    TrainingLiterals.WEIGHTED_LOSS: True,
    TrainingLiterals.DETAILED_METRICS: True,
    TrainingLiterals.WEIGHT_DECAY: 1e-4,
    TrainingLiterals.MOMENTUM: 0.9,
    SettingsLiterals.NUM_WORKERS: 8,
    SettingsLiterals.ENABLE_ONNX_NORMALIZATION: False,
    DistributedLiterals.DISTRIBUTED: DistributedParameters.DEFAULT_DISTRIBUTED,
    DistributedLiterals.MASTER_ADDR: DistributedParameters.DEFAULT_MASTER_ADDR,
    DistributedLiterals.MASTER_PORT: DistributedParameters.DEFAULT_MASTER_PORT,
    TrainingLiterals.WARMUP_COSINE_LR_CYCLES: 0.45,
    SettingsLiterals.OUTPUT_SCORING: False,
    SettingsLiterals.LOG_SCORING_FILE_INFO: False
}

multiclass_training_settings_defaults = {
    TrainingLiterals.PRIMARY_METRIC: MetricsLiterals.ACCURACY,
    TrainingLiterals.LR: 0.01,
    TrainingLiterals.LAST_LAYER_LR: 0.1,
    TrainingLiterals.STEP_LR_STEP_SIZE: 5,
    TrainingLiterals.STEP_LR_GAMMA: 0.5
}

multilabel_training_settings_defaults = {
    TrainingLiterals.PRIMARY_METRIC: MetricsLiterals.IOU,
    TrainingLiterals.LR: 0.035,
    TrainingLiterals.LAST_LAYER_LR: 0.1,
    TrainingLiterals.STEP_LR_STEP_SIZE: 5,
    TrainingLiterals.STEP_LR_GAMMA: 0.35
}

scoring_settings_defaults = {
    SettingsLiterals.NUM_WORKERS: 8
}

featurization_settings_defaults = {
    SettingsLiterals.NUM_WORKERS: 8
}

safe_to_log_vision_classification_settings = {
    TrainingLiterals.BATCH_SIZE,
    TrainingLiterals.DETAILED_METRICS,
    TrainingLiterals.DIFF_LR,
    TrainingLiterals.EARLY_STOPPING_PATIENCE,
    TrainingLiterals.FIT_LAST,
    TrainingLiterals.IMBALANCE_RATE_THRESHOLD,
    TrainingLiterals.LAST_LAYER_LR,
    TrainingLiterals.LR,
    TrainingLiterals.MOMENTUM,
    TrainingLiterals.NUM_EPOCHS,
    TrainingLiterals.OVERSAMPLE,
    TrainingLiterals.PARAMS,
    TrainingLiterals.PRIMARY_METRIC,
    TrainingLiterals.STEP_LR_GAMMA,
    TrainingLiterals.STEP_LR_STEP_SIZE,
    TrainingLiterals.STRATEGY,
    TrainingLiterals.TEST_RATIO,
    TrainingLiterals.VALIDATION_BATCH_SIZE,
    TrainingLiterals.WEIGHT_DECAY,
    TrainingLiterals.WEIGHTED_LOSS,
    TrainingLiterals.WARMUP_COSINE_LR_CYCLES
}

safe_to_log_settings = \
    safe_to_log_automl_settings | \
    safe_to_log_vision_common_settings | \
    safe_to_log_vision_classification_settings
