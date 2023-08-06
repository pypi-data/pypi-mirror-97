# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Entry script that is invoked by the driver script from automl."""

import argparse
import os
import time
import torch

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.constants import (
    SettingsLiterals, DistributedLiterals, DistributedParameters
)
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.classification.inference.score import _score_with_model

from azureml.contrib.automl.dnn.vision.classification.common.constants import (
    TrainingLiterals, base_training_settings_defaults,
    multiclass_training_settings_defaults,
    multilabel_training_settings_defaults,
    safe_to_log_settings
)

from .common.classification_utils import _get_train_valid_sub_file_paths, split_train_file_if_needed
from .trainer.trainer import train_model
from .io.read.dataset_wrappers import AmlDatasetWrapper, ImageFolderLabelFileDatasetWrapper
from .io.write.modelsaver import write_model
from .models import ModelFactory

from ..common import distributed_utils
from ..common.data_utils import get_labels_files_paths_from_settings, validate_labels_files_paths
from ..common.exceptions import AutoMLVisionValidationException
from ..common.logging_utils import get_logger, clean_settings_for_logging
from ..common.system_meter import SystemMeter
from ..common.sku_validation import validate_gpu_sku

from azureml.core.run import Run

azureml_run = Run.get_context()

logger = get_logger(__name__)


def read_aml_dataset(dataset_id, validation_dataset_id, multilabel, output_dir, master_process,
                     ignore_data_errors):
    """Read the training and validation datasets from AML datasets.

    :param dataset_id: Training dataset id
    :type dataset_id: str
    :param validation_dataset_id: Validation dataset id
    :type validation_dataset_id: str
    :param multilabel: boolean flag for whether its multilabel or not
    :type multilabel: bool
    :param output_dir: where to save train and val files
    :type output_dir: str
    :param master_process: boolean flag indicating whether current process is master or not.
    :type master_process: bool
    :param ignore_data_errors: flag that specifies if data errors should be ignored
    :type ignore_data_errors: bool
    :return: Training dataset and validation dataset
    :rtype Tuple of form (BaseDatasetWrapper, BaseDatasetWrapper)
    """
    ws = Run.get_context().experiment.workspace

    # Assumption is that aml dataset files are already downloaded to local path
    # by a call to download_required_files()
    download_files = False

    train_dataset_wrapper = AmlDatasetWrapper(dataset_id, multilabel=multilabel, workspace=ws,
                                              download_files=download_files, ignore_data_errors=ignore_data_errors)
    if validation_dataset_id is None:
        train_dataset_wrapper, valid_dataset_wrapper = train_dataset_wrapper.train_val_split()
    else:
        valid_dataset_wrapper = AmlDatasetWrapper(validation_dataset_id, multilabel=multilabel, workspace=ws,
                                                  download_files=download_files, ignore_data_errors=ignore_data_errors)

    if master_process:
        utils._save_image_df(train_df=train_dataset_wrapper._images_df,
                             val_df=valid_dataset_wrapper._images_df,
                             output_dir=output_dir)

    return train_dataset_wrapper, valid_dataset_wrapper


def _get_train_valid_dataset_wrappers(root_dir, train_file=None, valid_file=None, multilabel=False,
                                      ignore_data_errors=True, settings=None, master_process=False):
    """
    :param root_dir: root directory that will be used as prefix for paths in train_file and valid_file
    :type root_dir: str
    :param train_file: labels file for training with filenames and labels
    :type train_file: str
    :param valid_file: labels file for validation with filenames and labels
    :type valid_file: str
    :param multilabel: boolean flag for whether its multilabel or not
    :type multilabel: bool
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param settings: dictionary containing settings for training
    :type settings: dict
    :param master_process: boolean flag indicating whether current process is master or not.
    :type master_process: bool
    :return: tuple of train and validation dataset wrappers
    :rtype: tuple[BaseDatasetWrapper, BaseDatasetWrapper]
    """

    if valid_file is None:
        train_file, valid_file = _get_train_valid_sub_file_paths(output_dir=settings[SettingsLiterals.OUTPUT_DIR])

    train_dataset_wrapper = ImageFolderLabelFileDatasetWrapper(root_dir=root_dir, input_file=train_file,
                                                               multilabel=multilabel,
                                                               ignore_data_errors=ignore_data_errors)
    valid_dataset_wrapper = ImageFolderLabelFileDatasetWrapper(root_dir=root_dir, input_file=valid_file,
                                                               multilabel=multilabel,
                                                               all_labels=train_dataset_wrapper.labels,
                                                               ignore_data_errors=ignore_data_errors)

    if master_process:
        utils._save_image_lf(train_ds=train_file, val_ds=valid_file,
                             output_dir=settings[SettingsLiterals.OUTPUT_DIR])

    return train_dataset_wrapper, valid_dataset_wrapper


@utils._exception_handler
def run(automl_settings, multilabel=False):
    """Invoke training by passing settings and write the output model.

    :param automl_settings: dictionary with automl settings
    :type automl_settings: dict
    :param multilabel: boolean flag for multilabel
    :type multilabel: bool
    """
    script_start_time = time.time()

    settings, unknown = _parse_argument_settings(automl_settings, multilabel)

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
    utils.download_required_files(settings, AmlDatasetWrapper, ModelFactory())
    if not utils.is_aml_dataset_input(settings):
        split_train_file_if_needed(settings)

    # Decide to train in distributed mode or not based on gpu device count and distributed flag
    distributed = settings[DistributedLiterals.DISTRIBUTED]
    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    if distributed and device_count > 1:
        logger.info("Starting distributed training with world_size: {}.".format(device_count))
        distributed_utils.update_settings_for_distributed_training(settings, device_count)
        # Launch multiple processes
        torch.multiprocessing.spawn(train_worker, args=(settings, multilabel), nprocs=device_count, join=True)
    else:
        if distributed:
            logger.warning("Distributed flag is {}, but is not supported as the device_count is {}. "
                           "Training using a single process and setting the flag to False."
                           .format(distributed, device_count))
            settings[DistributedLiterals.DISTRIBUTED] = False
        train_worker(0, settings, multilabel)

    utils.log_script_duration(script_start_time, settings, azureml_run)


# Adding handler to log exceptions directly in the child process if using multigpu
@utils._exception_logger
def train_worker(rank, settings, multilabel):
    """Invoke training on a single device and write the output model.

    :param rank: Rank of the process if invoked in distributed mode. 0 otherwise.
    :type rank: int
    :param settings: Dictionary with all training and model settings
    :type settings: dict
    :param multilabel: boolean flag for multilabel
    :type multilabel: bool
    """
    distributed_utils.enable_distributed_logging(settings, rank)

    distributed = settings[DistributedLiterals.DISTRIBUTED]
    if distributed:
        distributed_utils.setup_distributed_training(rank, settings, logger)

    sys_meter = SystemMeter(log_static_sys_info=True)
    sys_meter.log_system_stats()

    # set multilabel flag in settings
    settings[SettingsLiterals.MULTILABEL] = multilabel
    image_folder = settings.get(SettingsLiterals.IMAGE_FOLDER, None)
    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)
    output_dir = settings[SettingsLiterals.OUTPUT_DIR]
    device = torch.device("cuda:" + str(rank)) if distributed else settings[SettingsLiterals.DEVICE]
    master_process = distributed_utils.master_process()
    validate_gpu_sku(device=device)
    ignore_data_errors = settings[SettingsLiterals.IGNORE_DATA_ERRORS]
    run_scoring = settings.get(SettingsLiterals.OUTPUT_SCORING, False)

    utils.warn_for_cpu_devices(device, azureml_run)

    # set randomization seed for deterministic training
    random_seed = settings.get(SettingsLiterals.RANDOM_SEED, None)
    if distributed and random_seed is None:
        # Set by default for distributed training to ensure all workers have same random parameters.
        random_seed = DistributedParameters.DEFAULT_RANDOM_SEED
    utils._set_random_seed(random_seed)
    utils._set_deterministic(settings.get(SettingsLiterals.DETERMINISTIC, False))

    if utils.is_aml_dataset_input(settings):
        train_dataset_wrapper, valid_dataset_wrapper = read_aml_dataset(
            dataset_id=dataset_id, validation_dataset_id=validation_dataset_id,
            multilabel=multilabel, output_dir=output_dir, master_process=master_process,
            ignore_data_errors=ignore_data_errors)

        logger.info("[train dataset_id: {}, validation dataset_id: {}]".format(dataset_id, validation_dataset_id))
    else:
        labels_path, validation_labels_path = get_labels_files_paths_from_settings(settings)
        if labels_path is None and image_folder is None:
            raise AutoMLVisionValidationException("Neither images_folder or labels_file found in automl settings",
                                                  has_pii=False)

        image_folder_path = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)

        train_dataset_wrapper, valid_dataset_wrapper = _get_train_valid_dataset_wrappers(
            root_dir=image_folder_path, train_file=labels_path, valid_file=validation_labels_path,
            multilabel=multilabel, ignore_data_errors=ignore_data_errors, settings=settings,
            master_process=master_process)

    if valid_dataset_wrapper.labels != train_dataset_wrapper.labels:
        all_labels = list(set(valid_dataset_wrapper.labels + train_dataset_wrapper.labels))
        train_dataset_wrapper.reset_labels(all_labels)
        valid_dataset_wrapper.reset_labels(all_labels)

    logger.info("# train images: {}, # validation images: {}, # labels: {}".format(
        len(train_dataset_wrapper), len(valid_dataset_wrapper), train_dataset_wrapper.num_classes))

    # TODO: Remove this padding logic when we upgrade pytorch with the fix below
    # https://github.com/pytorch/pytorch/commit/a69910868a5962e2d699c6069154836e262a29e2
    if distributed:
        world_size = distributed_utils.get_world_size()
        if len(train_dataset_wrapper) < world_size:
            train_dataset_wrapper.pad(world_size)
        if len(valid_dataset_wrapper) < world_size:
            valid_dataset_wrapper.pad(world_size)
        logger.info("After padding with world_size = {}, # train images: {}, # validation images: {}".format(
            world_size, len(train_dataset_wrapper), len(valid_dataset_wrapper)))

    best_model = train_model(model_name=settings[SettingsLiterals.MODEL_NAME],
                             strategy=settings[TrainingLiterals.STRATEGY],
                             dataset_wrapper=train_dataset_wrapper,
                             settings=settings,
                             valid_dataset=valid_dataset_wrapper,
                             device=device,
                             azureml_run=azureml_run)

    # Save model
    if master_process:
        model_name = settings[SettingsLiterals.MODEL_NAME]
        utils._set_train_run_properties(azureml_run, model_name)
        inference_model_wrapper = write_model(azureml_run, best_model,
                                              labels=train_dataset_wrapper.labels,
                                              output_dir=output_dir, device=device,
                                              enable_onnx_norm=settings[SettingsLiterals.ENABLE_ONNX_NORMALIZATION],
                                              task_type=settings[SettingsLiterals.TASK_TYPE])
        if run_scoring:
            score_validation_data(inference_model_wrapper, azureml_run=azureml_run,
                                  ignore_data_errors=ignore_data_errors,
                                  val_dataset_id=validation_dataset_id,
                                  image_folder=image_folder,
                                  device=device,
                                  settings=settings)


def score_validation_data(inference_model_wrapper, azureml_run, ignore_data_errors,
                          val_dataset_id, image_folder, device, settings):
    """ Runs validations on the best model to give predictions output

    :param inference_model_wrapper: inference model wrapper object
    :type inference_model_wrapper: inference.InferenceModelWrapper
    :param azureml_run: azureml run object
    :type azureml_run: azureml.core.run
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param val_dataset_id: The validation dataset id
    :type val_dataset_id: str
    :param image_folder: default prefix to be added to the paths contained in image_list_file
    :type image_folder: str
    :param device: device to use for scoring
    :type device: str
    :param settings: dictionary containing settings
    :type settings: dict
    """
    logger.info("Beginning validation for the best model")

    # Get image_list_file with path
    root_dir = image_folder
    val_labels_file = settings.get(SettingsLiterals.VALIDATION_LABELS_FILE, None)
    if val_labels_file is not None:
        val_labels_file = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], val_labels_file)
        root_dir = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)

    if val_labels_file is None and val_dataset_id is None:
        logger.warning("No validation dataset or validation file was given, skipping scoring run.")
        return

    # Get target path
    target_path = settings.get(SettingsLiterals.OUTPUT_DATASET_TARGET_PATH, None)
    if target_path is None:
        target_path = AmlLabeledDatasetHelper.get_default_target_path()

    batch_size = settings.get(TrainingLiterals.VALIDATION_BATCH_SIZE, None)
    if batch_size is None:
        batch_size = settings.get(TrainingLiterals.BATCH_SIZE)

    output_file = settings.get(SettingsLiterals.VALIDATION_OUTPUT_FILE, None)
    num_workers = settings[SettingsLiterals.NUM_WORKERS]
    log_scoring_file_info = settings.get(SettingsLiterals.LOG_SCORING_FILE_INFO, False)

    logger.info("[start scoring for validation data: batch_size: {}]".format(batch_size))
    _score_with_model(inference_model_wrapper,
                      run=azureml_run, target_path=target_path,
                      output_file=output_file, root_dir=root_dir,
                      image_list_file=val_labels_file, batch_size=batch_size,
                      ignore_data_errors=ignore_data_errors,
                      input_dataset_id=val_dataset_id,
                      device=device,
                      num_workers=num_workers,
                      log_output_file_info=log_scoring_file_info)


def _parse_argument_settings(automl_settings, multilabel):
    """Parse all arguments and merge settings

    :param automl_settings: dictionary with automl settings
    :type automl_settings: dict
    :param multilabel: boolean flag for multilabel
    :type multilabel: bool
    :return: tuple with automl settings dictionary with all settings filled in and unknown args
    :rtype: tuple
    """

    training_settings_defaults = base_training_settings_defaults
    if multilabel:
        training_settings_defaults.update(multilabel_training_settings_defaults)
        training_settings_defaults.update({SettingsLiterals.MULTILABEL: True})
    else:
        training_settings_defaults.update(multiclass_training_settings_defaults)

    parser = argparse.ArgumentParser(description="cluster images", allow_abbrev=False)

    utils.add_model_arguments(parser)

    parser.add_argument(utils._make_arg(SettingsLiterals.DEVICE), type=str,
                        default=training_settings_defaults[SettingsLiterals.DEVICE],
                        help="Device to train on (cpu/cuda:0/cuda:1,...)")
    parser.add_argument(utils._make_arg(TrainingLiterals.STRATEGY), type=str,
                        default=training_settings_defaults[TrainingLiterals.STRATEGY])
    parser.add_argument(utils._make_arg(TrainingLiterals.BATCH_SIZE), type=int,
                        default=training_settings_defaults[TrainingLiterals.BATCH_SIZE],
                        help="batch size to use")
    parser.add_argument(utils._make_arg(TrainingLiterals.VALIDATION_BATCH_SIZE), type=int,
                        default=training_settings_defaults[TrainingLiterals.VALIDATION_BATCH_SIZE],
                        help="batch size to use for validation")
    # Data args
    parser.add_argument(utils._make_arg(SettingsLiterals.DATA_FOLDER),
                        utils._make_arg(SettingsLiterals.DATA_FOLDER.replace("_", "-")),
                        type=str,
                        default=training_settings_defaults[SettingsLiterals.DATA_FOLDER],
                        help="root of the blob store")
    parser.add_argument(utils._make_arg(SettingsLiterals.LABELS_FILE_ROOT),
                        utils._make_arg(SettingsLiterals.LABELS_FILE_ROOT.replace("_", "-")), type=str,
                        default=training_settings_defaults[SettingsLiterals.LABELS_FILE_ROOT],
                        help="root relative to which label file paths exist")

    args, unknown = parser.parse_known_args()

    args_dict = utils.parse_model_conditional_space(vars(args))

    return utils._merge_settings_args_defaults(automl_settings, args_dict, training_settings_defaults), unknown
