# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Entry script that is invoked by the driver script from automl."""

import argparse
import os
import time
import torch

from azureml.core.run import Run
from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.core.shared.constants import Tasks

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.object_detection.writers.score import _score_with_model
from azureml.contrib.automl.dnn.vision.object_detection.common.constants import (
    TrainingParameters, LearningParameters,
    SchedulerParameters, training_settings_defaults,
    TrainingLiterals, FasterRCNNLiterals, FasterRCNNParameters,
    DataLoaderParameterLiterals, ValidationMetricType, safe_to_log_settings,
    ModelNames
)

from azureml.contrib.automl.dnn.vision.common.constants import (
    SettingsLiterals, DistributedLiterals,
    DistributedParameters, LRSchedulerNames
)

from azureml.contrib.automl.dnn.vision.object_detection_yolo import runner as yolo_runner
from .data import datasets, loaders
from .data.utils import read_aml_dataset, read_file_dataset
from .models import detection
from .models.object_detection_model_wrappers import ObjectDetectionModelFactory
from .models.instance_segmentation_model_wrappers import InstanceSegmentationModelFactory
from .trainer import optimize, criterion, train
from .writers.modelsaver import write_model
from .common.object_detection_utils import score_validation_data
from ..common import distributed_utils
from ..common.data_utils import get_labels_files_paths_from_settings, validate_labels_files_paths
from ..common.exceptions import AutoMLVisionValidationException
from ..common.logging_utils import get_logger, clean_settings_for_logging
from ..common.trainer import lrschedule

from ..common.system_meter import SystemMeter
from ..common.sku_validation import validate_gpu_sku

azureml_run = Run.get_context()

logger = get_logger(__name__)


@utils._exception_handler
def run(automl_settings):
    """Invoke training by passing settings and write the resulting model.

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    """
    script_start_time = time.time()

    settings, unknown = _parse_argument_settings(automl_settings)

    # Temporary hack to expose yolo as a model_name setting
    model_name = settings.get(SettingsLiterals.MODEL_NAME, None)
    if model_name == ModelNames.YOLO_V5:
        yolo_runner.run(automl_settings)
        return

    utils._top_initialization(settings)

    task_type = settings.get(SettingsLiterals.TASK_TYPE, None)

    if not task_type:
        raise AutoMLVisionValidationException("Task type was not found in automl settings.",
                                              has_pii=False)
    utils._set_logging_parameters(task_type, settings)

    # TODO JEDI
    # When we expose the package to customers we need to revisit. We should not log any unknown
    # args when the customers send their hp space.
    if unknown:
        logger.info("Got unknown args, will ignore them: {}".format(unknown))

    logger.info("Final settings (pii free): \n {}".format(clean_settings_for_logging(settings, safe_to_log_settings)))
    logger.info("Settings not logged (might contain pii): \n {}".format(settings.keys() - safe_to_log_settings))

    validate_labels_files_paths(settings)

    # Download required files before launching train_worker to avoid concurrency issues in distributed mode
    if task_type == Tasks.IMAGE_INSTANCE_SEGMENTATION:
        utils.download_required_files(settings, datasets.AmlDatasetObjectDetectionWrapper,
                                      InstanceSegmentationModelFactory())
    else:
        utils.download_required_files(settings, datasets.AmlDatasetObjectDetectionWrapper,
                                      ObjectDetectionModelFactory())

    # Decide to train in distributed mode or not based on gpu device count and distributed flag
    distributed = settings[DistributedLiterals.DISTRIBUTED]
    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    if distributed and device_count > 1:
        logger.info("Starting distributed training with world_size: {}.".format(device_count))
        distributed_utils.update_settings_for_distributed_training(settings, device_count)
        # Launch multiple processes
        torch.multiprocessing.spawn(train_worker, args=(settings,), nprocs=device_count, join=True)
    else:
        if distributed:
            logger.warning("Distributed flag is {}, but is not supported as the device_count is {}. "
                           "Training using a single process and settings the flag to False"
                           .format(distributed, device_count))
            settings[DistributedLiterals.DISTRIBUTED] = False
        train_worker(0, settings)

    utils.log_script_duration(script_start_time, settings, azureml_run)


# Adding handler to log exceptions directly in the child process if using multigpu
@utils._exception_logger
def train_worker(rank, settings):
    """Invoke training on a single device and write the resulting model.

    :param rank: Rank of the process if invoked in distributed mode. 0 otherwise.
    :type rank: int
    :param settings: Dictionary with all training and model settings
    :type settings: Dictionary
    """
    distributed_utils.enable_distributed_logging(settings, rank)

    distributed = settings[DistributedLiterals.DISTRIBUTED]
    if distributed:
        distributed_utils.setup_distributed_training(rank, settings, logger)

    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    model_name = settings[SettingsLiterals.MODEL_NAME]
    device = torch.device("cuda:" + str(rank)) if distributed else settings[SettingsLiterals.DEVICE]
    master_process = distributed_utils.master_process()
    validate_gpu_sku(device=device)

    utils.warn_for_cpu_devices(device, azureml_run)

    training_settings = {
        TrainingLiterals.NUMBER_OF_EPOCHS: settings[TrainingLiterals.NUMBER_OF_EPOCHS],
        TrainingLiterals.LR: settings[TrainingLiterals.LEARNING_RATE] * distributed_utils.get_world_size(),
        TrainingLiterals.MOMENTUM: settings[TrainingLiterals.MOMENTUM],
        TrainingLiterals.WEIGHT_DECAY: settings[TrainingLiterals.WEIGHT_DECAY],
        TrainingLiterals.MAX_PATIENCE_ITERATIONS: settings[TrainingLiterals.MAX_PATIENCE_ITERATIONS],
        TrainingLiterals.PRIMARY_METRIC: settings[TrainingLiterals.PRIMARY_METRIC],
        TrainingLiterals.VALIDATION_METRIC_TYPE: settings[TrainingLiterals.VALIDATION_METRIC_TYPE],
        TrainingLiterals.EARLY_STOP_DELAY_ITERATIONS: settings[TrainingLiterals.EARLY_STOP_DELAY_ITERATIONS]}

    fasterrcnn_settings = {
        FasterRCNNLiterals.MIN_SIZE: settings[FasterRCNNLiterals.MIN_SIZE],
        FasterRCNNLiterals.BOX_SCORE_THRESH: settings[FasterRCNNLiterals.BOX_SCORE_THRESH],
        FasterRCNNLiterals.BOX_NMS_THRESH: settings[FasterRCNNLiterals.BOX_NMS_THRESH],
        FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG: settings[FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG]}

    # Set dataloaders' num_workers
    num_workers = settings.get(SettingsLiterals.NUM_WORKERS, None)

    train_data_loader_settings = {
        DataLoaderParameterLiterals.BATCH_SIZE: settings[TrainingLiterals.TRAINING_BATCH_SIZE],
        DataLoaderParameterLiterals.SHUFFLE: True,
        DataLoaderParameterLiterals.NUM_WORKERS: num_workers,
        DataLoaderParameterLiterals.DISTRIBUTED: distributed,
        DataLoaderParameterLiterals.DROP_LAST: False}

    validation_data_loader_settings = {
        DataLoaderParameterLiterals.BATCH_SIZE: settings[TrainingLiterals.VALIDATION_BATCH_SIZE],
        DataLoaderParameterLiterals.SHUFFLE: False,
        DataLoaderParameterLiterals.NUM_WORKERS: num_workers,
        DataLoaderParameterLiterals.DISTRIBUTED: distributed,
        DataLoaderParameterLiterals.DROP_LAST: False}

    # Set randomization seed for deterministic training.
    random_seed = settings.get(SettingsLiterals.RANDOM_SEED, None)
    if distributed and random_seed is None:
        # Set by default for distributed training to ensure
        # all workers have same random parameters.
        random_seed = DistributedParameters.DEFAULT_RANDOM_SEED
    utils._set_random_seed(random_seed)
    utils._set_deterministic(settings.get(SettingsLiterals.DETERMINISTIC, False))

    # Extract Automl Settings
    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)

    ignore_data_errors = settings.get(SettingsLiterals.IGNORE_DATA_ERRORS, True)
    output_directory = settings[SettingsLiterals.OUTPUT_DIR]
    resume_file = settings.get(SettingsLiterals.RESUME, None)
    run_scoring = settings.get(SettingsLiterals.OUTPUT_SCORING, False)

    # Setup Dataset

    if utils.is_aml_dataset_input(settings):
        training_dataset, validation_dataset = read_aml_dataset(dataset_id,
                                                                validation_dataset_id,
                                                                ignore_data_errors,
                                                                output_directory,
                                                                master_process)
        logger.info("[train dataset_id: {}, validation dataset_id: {}]".format(dataset_id, validation_dataset_id))
    else:
        image_folder = settings.get(SettingsLiterals.IMAGE_FOLDER, None)

        if image_folder is None:
            raise ClientException("images_folder or dataset_id needs to be specified", has_pii=False)
        else:
            image_folder = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)

        annotations_file, annotations_test_file = get_labels_files_paths_from_settings(settings)

        training_dataset, validation_dataset = read_file_dataset(image_folder,
                                                                 annotations_file,
                                                                 annotations_test_file,
                                                                 ignore_data_errors,
                                                                 output_directory,
                                                                 master_process)
        logger.info("[train file: {}, validation file: {}]".format(annotations_file, annotations_test_file))

    if training_dataset.classes != validation_dataset.classes:
        all_classes = list(set(training_dataset.classes + validation_dataset.classes))
        training_dataset.reset_classes(all_classes)
        validation_dataset.reset_classes(all_classes)

    logger.info("# train images: {}, # validation images: {}, # labels: {}".format(
        len(training_dataset), len(validation_dataset), training_dataset.num_classes - 1))  # excluding "--bg--" class

    # TODO: Remove this padding logic when we upgrade pytorch with the fix below
    # https://github.com/pytorch/pytorch/commit/a69910868a5962e2d699c6069154836e262a29e2
    if distributed:
        world_size = distributed_utils.get_world_size()
        if len(training_dataset) < world_size:
            training_dataset.pad(world_size)
        if len(validation_dataset) < world_size:
            validation_dataset.pad(world_size)
        logger.info("After padding with world_size = {}, # train images: {}, # validation images: {}".format(
            world_size, len(training_dataset), len(validation_dataset)))

    # Setup Model
    model_wrapper = detection.setup_model(model_name=model_name, number_of_classes=training_dataset.num_classes,
                                          **fasterrcnn_settings)

    # TODO: Both classes and device should not be set here but in initialization
    model_wrapper.classes = training_dataset.classes
    model_wrapper.device = device

    # Move base model to device
    model_wrapper.to_device(device)

    # if the model exposes some transformations
    # enable those in the datasets.
    training_dataset.transform = model_wrapper.get_train_validation_transform()
    validation_dataset.transform = model_wrapper.get_train_validation_transform()
    # Replace model.transform resize and normalize with identity methods
    # so that we avoid re-doing the transform in the model
    if training_dataset.transform is not None and validation_dataset.transform is not None:
        logger.info("Found transform not None in both training and validation dataset - disabling in model.")
        model_wrapper.disable_model_transform()
    else:
        logger.info("Transform is None for datasets. Keep it in the model - this will increase GPU mem usage.")

    if distributed:
        model_wrapper.model = torch.nn.parallel.DistributedDataParallel(model_wrapper.model,
                                                                        device_ids=[rank],
                                                                        output_device=rank)
    model_wrapper.distributed = distributed

    num_params = sum([p.data.nelement() for p in model_wrapper.parameters()])
    logger.info("[model: {}, #param: {}]".format(model_name, num_params))

    # Resume

    if resume_file:
        checkpoint = torch.load(resume_file, map_location="cpu")
        model_wrapper.model.load_state_dict(checkpoint)  # TODO: Fix this in case of Distributed training.

    # Setup Dataloaders

    train_loader = loaders.setup_dataloader(training_dataset, **train_data_loader_settings)
    validation_loader = loaders.setup_dataloader(validation_dataset, **validation_data_loader_settings)

    # Setup Optimizer

    optimizer = optimize.setup_optimizer(model_wrapper, **training_settings)
    num_batches_per_epoch = len(train_loader)
    lr_scheduler_settings = {
        "warmup_steps": num_batches_per_epoch * 2,
        "total_steps": num_batches_per_epoch * training_settings["number_of_epochs"],
        "cycles": SchedulerParameters.DEFAULT_WARMUP_COSINE_LR_CYCLES
    }
    lr_scheduler = lrschedule.setup_lr_scheduler(
        optimizer, LRSchedulerNames.WARMUP_COSINE, **lr_scheduler_settings)
    loss_function = criterion.setup_criterion("FASTER_RCNN")

    # Train Model

    train_settings = train.TrainSettings(**training_settings)
    logger.info("[start training: train batch_size: {}, val batch_size: {}, train_settings {}]".format(
        train_data_loader_settings["batch_size"], validation_data_loader_settings["batch_size"], vars(train_settings)))

    system_meter.log_system_stats()

    log_verbsose_metrics = settings.get(SettingsLiterals.LOG_VERBOSE_METRICS, False)

    train.train(model=model_wrapper,
                optimizer=optimizer,
                scheduler=lr_scheduler,
                train_data_loader=train_loader,
                device=device,
                criterion=loss_function,
                train_settings=train_settings,
                val_data_loader=validation_loader,
                val_dataset=validation_dataset,
                val_metric_type=training_settings[TrainingLiterals.VALIDATION_METRIC_TYPE],
                val_index_map=model_wrapper.classes,
                azureml_run=azureml_run,
                ignore_data_errors=ignore_data_errors,
                log_verbsose_metrics=log_verbsose_metrics)

    # Save model
    if master_process:
        model_name = settings[SettingsLiterals.MODEL_NAME]
        utils._set_train_run_properties(azureml_run, model_name)
        write_model(azureml_run, model_wrapper, labels=training_dataset.classes, output_dir=output_directory,
                    device=device, enable_onnx_norm=settings[SettingsLiterals.ENABLE_ONNX_NORMALIZATION],
                    task_type=settings[SettingsLiterals.TASK_TYPE], model_settings=fasterrcnn_settings)

        if run_scoring:
            score_validation_data(run=azureml_run, model_settings=fasterrcnn_settings,
                                  settings=settings, device=device,
                                  score_with_model=_score_with_model)


def _parse_argument_settings(automl_settings):
    """Parse all arguments and merge settings

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    :return: tuple of the automl settings dictionary with all settings filled in and a list of any unknown args
    :rtype: tuple
    """

    parser = argparse.ArgumentParser(description="Object detection", allow_abbrev=False)

    # Model and Device Settings
    utils.add_model_arguments(parser)

    parser.add_argument(utils._make_arg(SettingsLiterals.DEVICE), type=str,
                        help="Device to train on (cpu/cuda:0/cuda:1,...)",
                        default=training_settings_defaults[SettingsLiterals.DEVICE])

    # Training Related Settings
    parser.add_argument(utils._make_arg(TrainingLiterals.NUMBER_OF_EPOCHS), type=int,
                        help="number of training epochs",
                        default=TrainingParameters.DEFAULT_NUMBER_EPOCHS)
    parser.add_argument(utils._make_arg(TrainingLiterals.MAX_PATIENCE_ITERATIONS), type=int,
                        help="max number of epochs with no validation improvement",
                        default=TrainingParameters.DEFAULT_PATIENCE_ITERATIONS)
    parser.add_argument(utils._make_arg(TrainingLiterals.VALIDATION_METRIC_TYPE),
                        help="metric computation method to use for validation metrics",
                        choices=ValidationMetricType.ALL_TYPES,
                        default=TrainingParameters.DEFAULT_VALIDATION_METRIC_TYPE)
    parser.add_argument(utils._make_arg(TrainingLiterals.EARLY_STOP_DELAY_ITERATIONS), type=int,
                        help="number of epochs to wait before validation improvement is tracked for early stopping",
                        default=TrainingParameters.DEFAULT_EARLY_STOP_DELAY_ITERATIONS)

    parser.add_argument(utils._make_arg(TrainingLiterals.LEARNING_RATE), type=float,
                        help="learning rate for optimizer",
                        default=LearningParameters.SGD_DEFAULT_LEARNING_RATE)
    parser.add_argument(utils._make_arg(TrainingLiterals.MOMENTUM), type=float,
                        help="momentum for optimizer",
                        default=LearningParameters.SGD_DEFAULT_MOMENTUM)
    parser.add_argument(utils._make_arg(TrainingLiterals.WEIGHT_DECAY), type=float,
                        help="optimizer weight decay",
                        default=LearningParameters.SGD_DEFAULT_WEIGHT_DECAY)

    parser.add_argument(utils._make_arg(TrainingLiterals.STEP_SIZE), type=int,
                        help="step size for learning rate scheduler",
                        default=SchedulerParameters.DEFAULT_STEP_LR_STEP_SIZE)
    parser.add_argument(utils._make_arg(TrainingLiterals.GAMMA), type=float,
                        help="decay rate for learning rate scheduler",
                        default=SchedulerParameters.DEFAULT_STEP_LR_GAMMA)

    # Faster-rcnn Settings
    parser.add_argument(utils._make_arg(FasterRCNNLiterals.MIN_SIZE), type=int,
                        help="minimum size of the image to be rescaled before feeding it to the backbone",
                        default=FasterRCNNParameters.DEFAULT_MIN_SIZE)
    parser.add_argument(utils._make_arg(FasterRCNNLiterals.BOX_SCORE_THRESH), type=float,
                        help="during inference, only return proposals with a classification score \
                        greater than box_score_thresh",
                        default=FasterRCNNParameters.DEFAULT_BOX_SCORE_THRESH)
    parser.add_argument(utils._make_arg(FasterRCNNLiterals.BOX_NMS_THRESH), type=float,
                        help="NMS threshold for the prediction head. Used during inference",
                        default=FasterRCNNParameters.DEFAULT_BOX_NMS_THRESH)
    parser.add_argument(utils._make_arg(FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG), type=int,
                        help="maximum number of detections per image, for all classes.",
                        default=FasterRCNNParameters.DEFAULT_BOX_DETECTIONS_PER_IMG)

    # Dataloader Settings
    parser.add_argument(utils._make_arg(TrainingLiterals.TRAINING_BATCH_SIZE), type=int,
                        help="training batch size",
                        default=TrainingParameters.DEFAULT_TRAINING_BATCH_SIZE)

    parser.add_argument(utils._make_arg(TrainingLiterals.VALIDATION_BATCH_SIZE), type=int,
                        help="validation batch size",
                        default=TrainingParameters.DEFAULT_VALIDATION_BATCH_SIZE)

    parser.add_argument(utils._make_arg(SettingsLiterals.DATA_FOLDER),
                        utils._make_arg(SettingsLiterals.DATA_FOLDER.replace("_", "-")),
                        type=str,
                        help="root of the blob store",
                        default="")

    parser.add_argument(utils._make_arg(SettingsLiterals.LABELS_FILE_ROOT),
                        utils._make_arg(SettingsLiterals.LABELS_FILE_ROOT.replace("_", "-")),
                        type=str,
                        help="root relative to which label file paths exist",
                        default="")

    # Extract Commandline Settings

    args, unknown = parser.parse_known_args()

    args_dict = utils.parse_model_conditional_space(vars(args))

    return utils._merge_settings_args_defaults(automl_settings, args_dict, training_settings_defaults), unknown
