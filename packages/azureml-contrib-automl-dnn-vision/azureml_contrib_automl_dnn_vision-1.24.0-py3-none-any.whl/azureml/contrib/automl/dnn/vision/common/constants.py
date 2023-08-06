# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Constants for the package."""


class ArtifactLiterals:
    """Filenames for artifacts."""
    FEATURIZE_SCRIPT = 'featurize_script.py'
    LABEL_FILE_NAME = 'labels.json'
    LABEL_METRICS_FILE_NAME = "label_metrics.json"
    MODEL_FILE_NAME = 'model.pt'
    MODEL_WRAPPER_PKL = 'model_wrapper.pkl'
    ONNX_MODEL_FILE_NAME = 'model.onnx'
    OUTPUT_DIR = 'train_artifacts'
    SCORE_SCRIPT = 'score_script.py'
    TRAIN_SUB_FILE_NAME = "train_sub.json"
    VAL_SUB_FILE_NAME = "val_sub.json"


class MetricsLiterals:
    """String key names for metrics."""
    SCRIPT_DURATION_SECONDS = "script_duration_seconds"

    TRAIN_DURATION_SECONDS = "train_duration_seconds"
    TRAIN_EPOCH_COUNT = "train_epoch_count"

    TRAIN_EPOCH_DURATION_SECONDS_AVG = "train_epoch_duration_seconds_avg"
    TRAIN_EPOCH_DURATION_SECONDS_MAX = "train_epoch_duration_seconds_max"
    TRAIN_EPOCH_DURATION_SECONDS_MIN = "train_epoch_duration_seconds_min"

    TRAIN_GPU_MEM_USED_MB_AVG = "train_gpu_mem_used_mb_avg"
    TRAIN_GPU_MEM_USED_MB_MAX = "train_gpu_mem_used_mb_max"
    TRAIN_GPU_MEM_USED_MB_MIN = "train_gpu_mem_used_mb_min"

    TRAIN_GPU_USED_PCT_AVG = "train_gpu_used_pct_avg"
    TRAIN_GPU_USED_PCT_MAX = "train_gpu_used_pct_max"
    TRAIN_GPU_USED_PCT_MIN = "train_gpu_used_pct_min"

    TRAIN_SYS_MEM_PCT_AVG = "train_sys_mem_pct_avg"
    TRAIN_SYS_MEM_PCT_MAX = "train_sys_mem_pct_max"
    TRAIN_SYS_MEM_PCT_MIN = "train_sys_mem_pct_min"

    TRAIN_SYS_MEM_SHARED_MB_AVG = "train_sys_mem_shared_mb_avg"
    TRAIN_SYS_MEM_SHARED_MB_MAX = "train_sys_mem_shared_mb_max"
    TRAIN_SYS_MEM_SHARED_MB_MIN = "train_sys_mem_shared_mb_min"

    TRAIN_SYS_MEM_USED_MB_AVG = "train_sys_mem_used_mb_avg"
    TRAIN_SYS_MEM_USED_MB_MAX = "train_sys_mem_used_mb_max"
    TRAIN_SYS_MEM_USED_MB_MIN = "train_sys_mem_used_mb_min"

    VALID_GPU_MEM_USED_MB_AVG = "valid_gpu_mem_used_mb_avg"
    VALID_GPU_MEM_USED_MB_MAX = "valid_gpu_mem_used_mb_max"
    VALID_GPU_MEM_USED_MB_MIN = "valid_gpu_mem_used_mb_min"

    VALID_GPU_USED_PCT_AVG = "valid_gpu_used_pct_avg"
    VALID_GPU_USED_PCT_MAX = "valid_gpu_used_pct_max"
    VALID_GPU_USED_PCT_MIN = "valid_gpu_used_pct_min"

    VALID_SYS_MEM_PCT_AVG = "valid_sys_mem_pct_avg"
    VALID_SYS_MEM_PCT_MAX = "valid_sys_mem_pct_max"
    VALID_SYS_MEM_PCT_MIN = "valid_sys_mem_pct_min"

    VALID_SYS_MEM_SHARED_MB_AVG = "valid_sys_mem_shared_mb_avg"
    VALID_SYS_MEM_SHARED_MB_MAX = "valid_sys_mem_shared_mb_max"
    VALID_SYS_MEM_SHARED_MB_MIN = "valid_sys_mem_shared_mb_min"

    VALID_SYS_MEM_USED_MB_AVG = "valid_sys_mem_used_mb_avg"
    VALID_SYS_MEM_USED_MB_MAX = "valid_sys_mem_used_mb_max"
    VALID_SYS_MEM_USED_MB_MIN = "valid_sys_mem_used_mb_min"


class SystemSettings:
    """System settings."""
    NAMESPACE = 'azureml.contrib.automl.dnn.vision'
    LOG_FILENAME = 'azureml_automl_vision.log'
    LOG_FOLDER = 'logs'


class PretrainedModelNames:
    """Pre trained model names."""
    RESNET18 = 'resnet18'
    RESNET50 = 'resnet50'
    MOBILENET_V2 = 'mobilenet_v2'
    SE_RESNEXT50_32X4D = 'se_resnext50_32x4d'
    FASTERRCNN_RESNET50_FPN_COCO = 'fasterrcnn_resnet50_fpn_coco'
    MASKRCNN_RESNET50_FPN_COCO = 'maskrcnn_resnet50_fpn_coco'
    YOLOV5_SMALL = 'yolov5.3.0s'
    YOLOV5_MEDIUM = 'yolov5.3.0m'
    YOLOV5_LARGE = 'yolov5.3.0l'
    YOLOV5_XLARGE = 'yolov5.3.0x'


class RunPropertyLiterals:
    """String keys important for finding the best run."""
    PIPELINE_SCORE = 'score'


class ScoringLiterals:
    """String names for scoring settings"""
    BATCH_SIZE = 'batch_size'
    DEFAULT_OUTPUT_DIR = 'outputs'
    EXPERIMENT_NAME = 'experiment_name'
    FEATURE_FILE_NAME = 'features.txt'
    FEATURIZATION_OUTPUT_FILE = 'featurization_output_file'
    IMAGE_LIST_FILE = 'image_list_file'
    INPUT_DATASET_ID = 'input_dataset_id'
    LABELED_DATASET_FILE_NAME = 'labeled_dataset.json'
    OUTPUT_FILE = 'output_file'
    OUTPUT_FEATURIZATION = 'output_featurization'
    PREDICTION_FILE_NAME = 'predictions.txt'
    ROOT_DIR = 'root_dir'
    RUN_ID = 'run_id'
    VALIDATE_SCORE = 'validate_score'
    LOG_OUTPUT_FILE_INFO = 'log_output_file_info'


class SettingsLiterals:
    """String names for automl settings"""
    DATA_FOLDER = 'data_folder'
    DATASET_ID = 'dataset_id'
    DEVICE = 'device'
    DETERMINISTIC = 'deterministic'
    ENABLE_ONNX_NORMALIZATION = 'enable_onnx_normalization'
    IGNORE_DATA_ERRORS = 'ignore_data_errors'
    IMAGE_FOLDER = 'images_folder'
    LABELS_FILE = 'labels_file'
    LABELS_FILE_ROOT = 'labels_file_root'
    LOG_SCORING_FILE_INFO = 'log_scoring_file_info'
    LOG_VERBOSE_METRICS = 'log_verbose_metrics'
    MODEL = 'model'
    MODEL_NAME = 'model_name'
    MULTILABEL = 'multilabel'
    NUM_WORKERS = 'num_workers'
    OUTPUT_DIR = 'output_dir'
    OUTPUT_DATASET_TARGET_PATH = 'output_dataset_target_path'
    OUTPUT_SCORING = 'output_scoring'
    PRINT_LOCAL_PACKAGE_VERSIONS = 'print_local_package_versions'
    RANDOM_SEED = 'seed'
    RESUME = 'resume'
    TASK_TYPE = 'task_type'
    VALIDATION_DATASET_ID = 'validation_dataset_id'
    VALIDATION_LABELS_FILE = 'validation_labels_file'
    VALIDATION_OUTPUT_FILE = 'validation_output_file'
    VALIDATE_SCORING = 'validate_scoring'


class PretrainedModelUrls:
    """The urls of the pretrained models which are stored in the CDN."""

    MODEL_FOLDER_URL = 'https://aka.ms/automl-resources/data/models-vision-pretrained'

    MODEL_URLS = {
        PretrainedModelNames.RESNET18:
            '{}/{}'.format(MODEL_FOLDER_URL, 'resnet18-5c106cde.pth'),
        PretrainedModelNames.RESNET50:
            '{}/{}'.format(MODEL_FOLDER_URL, 'resnet50-19c8e357.pth'),
        PretrainedModelNames.MOBILENET_V2:
            '{}/{}'.format(MODEL_FOLDER_URL, 'mobilenet_v2-b0353104.pth'),
        PretrainedModelNames.SE_RESNEXT50_32X4D:
            '{}/{}'.format(MODEL_FOLDER_URL, 'se_resnext50_32x4d-a260b3a4.pth'),
        PretrainedModelNames.FASTERRCNN_RESNET50_FPN_COCO:
            '{}/{}'.format(MODEL_FOLDER_URL, 'fasterrcnn_resnet50_fpn_coco-258fb6c6.pth'),
        PretrainedModelNames.MASKRCNN_RESNET50_FPN_COCO:
            '{}/{}'.format(MODEL_FOLDER_URL, 'maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth'),
        PretrainedModelNames.YOLOV5_SMALL:
            '{}/{}'.format(MODEL_FOLDER_URL, 'yolov5.3.0s-3058c1cb.pth'),
        PretrainedModelNames.YOLOV5_MEDIUM:
            '{}/{}'.format(MODEL_FOLDER_URL, 'yolov5.3.0m-a04eea56.pth'),
        PretrainedModelNames.YOLOV5_LARGE:
            '{}/{}'.format(MODEL_FOLDER_URL, 'yolov5.3.0l-84ff5751.pth'),
        PretrainedModelNames.YOLOV5_XLARGE:
            '{}/{}'.format(MODEL_FOLDER_URL, 'yolov5.3.0x-be3180f8.pth')
    }


class PretrainedSettings:
    """Settings related to fetching pretrained models."""
    DOWNLOAD_RETRY_COUNT = 3


class DistributedLiterals:
    """String keys for distributed parameters."""
    DISTRIBUTED = "distributed"
    MASTER_ADDR = "MASTER_ADDR"
    MASTER_PORT = "MASTER_PORT"
    WORLD_SIZE = "world_size"


class DistributedParameters:
    """Default distributed parameters."""
    DEFAULT_DISTRIBUTED = True
    DEFAULT_BACKEND = "nccl"
    DEFAULT_MASTER_ADDR = "127.0.0.1"
    DEFAULT_MASTER_PORT = "29500"  # TODO: What if this port is not available.
    DEFAULT_RANDOM_SEED = 47


class LRSchedulerNames:
    """String names for scheduler parameters."""
    DEFAULT_LR_SCHEDULER = "STEP"
    STEP = "STEP"
    WARMUP_COSINE = "warmup_cosine"


class Warnings:
    """Warning strings."""
    CPU_DEVICE_WARNING = "The device being used for training is 'cpu'. Training can be slow and may lead to " \
                         "out of memory errors. Please switch to a compute with gpu devices. " \
                         "If you are already running on a compute with gpu devices, please check to make sure " \
                         "your nvidia drivers are compatible with torch version {}."


safe_to_log_vision_common_settings = {
    # SettingsLiterals.DATA_FOLDER # not safe
    SettingsLiterals.DATASET_ID,
    SettingsLiterals.DEVICE,
    SettingsLiterals.DETERMINISTIC,
    SettingsLiterals.ENABLE_ONNX_NORMALIZATION,
    SettingsLiterals.IGNORE_DATA_ERRORS,
    # SettingsLiterals.IMAGE_FOLDER # not safe
    # SettingsLiterals.LABELS_FILE # not safe
    # SettingsLiterals.LABELS_FILE_ROOT # not safe
    SettingsLiterals.LOG_SCORING_FILE_INFO,
    SettingsLiterals.LOG_VERBOSE_METRICS,
    SettingsLiterals.MODEL_NAME,
    SettingsLiterals.MULTILABEL,
    SettingsLiterals.NUM_WORKERS,
    SettingsLiterals.OUTPUT_DIR,
    # SettingsLiterals.OUTPUT_DATASET_TARGET_PATH, # not safe
    SettingsLiterals.OUTPUT_SCORING,
    SettingsLiterals.PRINT_LOCAL_PACKAGE_VERSIONS,
    SettingsLiterals.RANDOM_SEED,
    SettingsLiterals.RESUME,
    SettingsLiterals.TASK_TYPE,
    SettingsLiterals.VALIDATION_DATASET_ID,
    # SettingsLiterals.VALIDATION_LABELS_FILE # not safe
    # SettingsLiterals.VALIDATION_OUTPUT_FILE, # not safe
    SettingsLiterals.VALIDATE_SCORING,

    ScoringLiterals.BATCH_SIZE,
    ScoringLiterals.DEFAULT_OUTPUT_DIR,
    # ScoringLiterals.EXPERIMENT_NAME, # not safe
    # This can stay as it is not exposed
    ScoringLiterals.FEATURE_FILE_NAME,
    # This can stay as it is not exposed
    ScoringLiterals.FEATURIZATION_OUTPUT_FILE,
    # ScoringLiterals.IMAGE_LIST_FILE,  # not safe
    ScoringLiterals.INPUT_DATASET_ID,
    # ScoringLiterals.OUTPUT_FILE,  # not safe
    ScoringLiterals.OUTPUT_FEATURIZATION,
    # ScoringLiterals.PREDICTION_FILE_NAME,  # not safe
    # ScoringLiterals.ROOT_DIR,  # not safe
    ScoringLiterals.RUN_ID,
    ScoringLiterals.VALIDATE_SCORE
}

# most of these settings do not have any effect on vision workflow
# but we'll log them in case we need to analyse a side effect that they might create
safe_to_log_automl_settings = {
    '_debug_log',
    '_ignore_package_version_incompatibilities',
    '_local_managed_run_id',
    'allowed_private_models',
    'auto_blacklist',
    'azure_service',
    'blacklist_algos',
    'blacklist_samples_reached',
    'compute_target',
    'cost_mode',
    'cv_split_column_names',
    'data_script',
    'early_stopping_n_iters',
    'enable_dnn',
    'enable_early_stopping',
    'enable_ensembling',
    'enable_feature_sweeping',
    'enable_local_managed',
    'enable_nimbusml',
    'enable_onnx_compatible_models',
    'enable_split_onnx_featurizer_estimator_models',
    'enable_stack_ensembling',
    'enable_streaming',
    'enable_subsampling',
    'enable_tf',
    'enforce_time_on_windows',
    'ensemble_iterations',
    'environment_label',
    'exclude_nan_labels',
    'experiment_exit_score',
    'experiment_timeout_minutes',
    'featurization',
    'force_streaming',
    'force_text_dnn',
    'is_gpu'
    'is_timeseries',
    'iteration_timeout_minutes',
    'iterations',
    'lag_length',
    'many_models',
    'max_concurrent_iterations',
    'max_cores_per_iteration',
    'mem_in_mb',
    'metric_operation',
    'metrics',
    'model_explainability',
    'n_cross_validations',
    'num_classes',
    'pipeline_fetch_max_batch_size',
    'preprocess',
    'region',
    'resource_group',
    'scenario',
    'sdk_packages',
    'sdk_url',
    'send_telemetry',
    'service_url',
    'show_warnings',
    'spark_service',
    'subsample_seed',
    'subscription_id',
    'supported_models',
    'task_type',
    'telemetry_verbosity',
    'track_child_runs',
    'validation_size',
    'verbosity',
    'vm_type',
    'weight_column_name',
    'whitelist_models',
    'workspace_name',
    'y_max',
    'y_min',
}
