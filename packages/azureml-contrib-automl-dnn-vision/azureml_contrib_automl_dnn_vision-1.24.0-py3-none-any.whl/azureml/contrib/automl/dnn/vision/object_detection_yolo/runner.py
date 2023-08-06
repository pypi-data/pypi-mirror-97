# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Entry script that is invoked by the driver script from automl."""

import argparse
import os
import time

import torch.optim as optim

from azureml.core.run import Run
from azureml.automl.core.shared.exceptions import ClientException

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.object_detection_yolo.writers.score import _score_with_model
from azureml.contrib.automl.dnn.vision.common.constants import (
    ArtifactLiterals, SettingsLiterals, DistributedLiterals, PretrainedModelUrls
)

from .common.constants import (
    yolo_hyp_defaults, training_settings_defaults, TrainingLiterals,
    TrainingParameters, YoloLiterals, YoloParameters
)
from .data.datasets import FileObjectDetectionDatasetWrapperYolo, AmlDatasetObjectDetectionWrapperYolo
from .models.yolo import Model
from .trainer.train import train
from .utils.utils import check_img_size, init_seeds, WarmupCosineSchedule, check_file
from .utils.ema import ModelEMA
from ..common import distributed_utils
from ..common.data_utils import get_labels_files_paths_from_settings, validate_labels_files_paths
from ..common.exceptions import AutoMLVisionValidationException
from ..common.logging_utils import get_logger
from ..common.pretrained_model_utilities import PretrainedModelFactory
from ..common.system_meter import SystemMeter
from ..common.sku_validation import validate_gpu_sku
from ..object_detection.common.object_detection_utils import score_validation_data
from ..object_detection.writers.modelsaver import write_model
from ..object_detection.data.loaders import setup_dataloader
from ..object_detection.data.utils import read_aml_dataset, read_file_dataset

azureml_run = Run.get_context()

logger = get_logger(__name__)


def setup_dataloaders(settings, output_directory):
    """Settings for (file and aml) datasets and data loaders

    :param settings: Dictionary with all training and model settings
    :type settings: Dictionary
    :param output_directory: Name of dir to save files for training/validation dataset
    :type output_directory: String
    :return: train_loader and validation_loader
    :rtype: Tuple of form (dataloaders.RobustDataLoader, dataloaders.RobustDataLoader)
    """
    # Settings for Aml dataset
    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)

    # Settings for both
    ignore_data_errors = settings.get(SettingsLiterals.IGNORE_DATA_ERRORS, True)
    settings['img_size'] = check_img_size(settings['img_size'], settings['gs'])

    # Setup Dataset
    if utils.is_aml_dataset_input(settings):
        train_dataset, validation_dataset = read_aml_dataset(dataset_id=dataset_id,
                                                             validation_dataset_id=validation_dataset_id,
                                                             settings=settings,
                                                             ignore_data_errors=ignore_data_errors,
                                                             output_dir=output_directory,
                                                             master_process=distributed_utils.master_process(),
                                                             dataset_class=AmlDatasetObjectDetectionWrapperYolo,
                                                             download_files=True)
        logger.info("[train dataset_id: {}, validation dataset_id: {}]".format(dataset_id, validation_dataset_id))
    else:
        image_folder = settings.get(SettingsLiterals.IMAGE_FOLDER, None)

        if image_folder is None:
            raise ClientException("images_folder or dataset_id needs to be specified", has_pii=False)
        else:
            image_folder = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)

        train_labels_file, val_labels_file = get_labels_files_paths_from_settings(settings)

        train_dataset, validation_dataset = read_file_dataset(image_folder=image_folder,
                                                              annotations_file=train_labels_file,
                                                              annotations_test_file=val_labels_file,
                                                              settings=settings,
                                                              ignore_data_errors=ignore_data_errors,
                                                              output_dir=output_directory,
                                                              dataset_class=FileObjectDetectionDatasetWrapperYolo,
                                                              master_process=distributed_utils.master_process())
        logger.info("[train file: {}, validation file: {}]".format(train_labels_file, val_labels_file))

    # Update classes
    if train_dataset.classes != validation_dataset.classes:
        all_classes = list(set(train_dataset.classes + validation_dataset.classes))
        train_dataset.reset_classes(all_classes)
        validation_dataset.reset_classes(all_classes)

    logger.info("[# train images: {}, # validation images: {}, # labels: {}, image size: {}]".format(
        len(train_dataset), len(validation_dataset), train_dataset.num_classes, settings['img_size']))

    # Setup Dataloaders
    train_dataloader_settings = {'batch_size': settings[TrainingLiterals.TRAINING_BATCH_SIZE],
                                 'shuffle': True,
                                 'num_workers': settings[SettingsLiterals.NUM_WORKERS]}
    val_dataloader_settings = {'batch_size': settings[TrainingLiterals.VALIDATION_BATCH_SIZE],
                               'shuffle': False,
                               'num_workers': settings[SettingsLiterals.NUM_WORKERS]}

    train_loader = setup_dataloader(train_dataset, **train_dataloader_settings)
    validation_loader = setup_dataloader(validation_dataset, **val_dataloader_settings)

    return train_loader, validation_loader


def _find_config(settings):
    """Find a file path for cfg

    :param settings: Dictionary with all training and model settings
    :type settings: Dictionary
    :return: File path for model_cfg
    :rtype: String
    """
    # Verify model_name
    model_name = settings['model_name']
    if model_name != training_settings_defaults[SettingsLiterals.MODEL_NAME]:
        settings['model_name'] = training_settings_defaults[SettingsLiterals.MODEL_NAME]
        logger.warning("[{} model_name is NOT supported. Currently, only {} is supported. "
                       "Using {} instead]".format(model_name, training_settings_defaults[SettingsLiterals.MODEL_NAME],
                                                  settings['model_name']))

    # Verify model_size
    model_size = settings['model_size']
    size = model_size[0].lower()
    if size not in ['s', 'm', 'l', 'x']:
        settings['model_size'] = YoloParameters.DEFAULT_MODEL_SIZE
        size = settings['model_size'][0]
        logger.warning("[{} model_size is NOT supported. It should start with s, m, l or x. "
                       "Using {} instead]".format(model_size, settings['model_size']))

    # Find cfg file name based on the model_name and model_size
    cfg = settings['model_name'][:-1] + YoloParameters.DEFAULT_MODEL_VERSION + size + '.yaml'

    # TODO: when large or xlarge is chosen, reduce batch_size to avoid CUDA out of memory
    if settings['device'] != 'cpu' and size in ['l', 'x']:
        logger.warning("[model_size (medium) is supported on 12GiB GPU memory with a batch_size of 16. "
                       "Your choice of model_size ({}) and a batch_size of {} might lead to CUDA OOM]"
                       .format(settings['model_size'], settings['training_batch_size']))

    current_file_path = os.path.dirname(__file__)
    model_cfg = check_file(os.path.join(current_file_path, YoloLiterals.MODELS, cfg))

    return model_cfg


def _create_model(cfg, number_of_classes, settings):
    """Create a yolo model

    :param cfg: yaml file for model definition
    :type cfg: string
    :param number_of_classes: number of classes
    :type number_of_classes: int
    :param settings: Dictionary with all training and model settings
    :type settings: Dictionary
    :return: yolo model
    :rtype: <class 'azureml.contrib.automl.dnn.vision.object_detection_yolo.models.yolo.Model'>
    """

    model = Model(model_cfg=cfg, nc=number_of_classes)

    size = settings['model_size'][0].lower()
    model_size = settings['model_name'][:-1] + YoloParameters.DEFAULT_MODEL_VERSION + size

    # Download pretrained model weights based on model size
    pretrained_ckpt = PretrainedModelFactory._load_state_dict_from_url_with_retry(
        PretrainedModelUrls.MODEL_URLS[model_size])

    # TODO: support resume
    # Update a model with pretrained weights
    new_ckpt = {}
    for k, v in pretrained_ckpt.items():
        if model.state_dict()[k].numel() == v.numel():
            new_ckpt[k] = v
    model.load_state_dict(new_ckpt, strict=False)

    return model


@utils._exception_handler
def run(automl_settings):
    """Invoke training by passing settings and write the resulting model.

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    """
    script_start_time = time.time()

    settings, unknown = _parse_argument_settings(automl_settings)

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

    # TODO: support multi-gpu
    if DistributedLiterals.DISTRIBUTED in settings:
        if settings[DistributedLiterals.DISTRIBUTED]:
            logger.error("Distributed is not supported for yolo. Continuing with a single gpu.")
            settings[DistributedLiterals.DISTRIBUTED] = False
    else:
        settings[DistributedLiterals.DISTRIBUTED] = False

    # Find cfg (for model definition) based on model_size and update settings['model_size'] if necessary
    cfg = _find_config(settings)

    # TODO JEDI
    # This is ok to log now because it can only be system metadata. When we expose the package to customers
    # we need to revisit.
    logger.info("Final settings: \n {}".format(settings))

    validate_labels_files_paths(settings)

    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    tb_writer = utils.init_tensorboard()

    # Set random seed
    init_seeds(1)

    epochs = settings['number_of_epochs']
    device = settings[SettingsLiterals.DEVICE]
    validate_gpu_sku(device=device)
    output_directory = ArtifactLiterals.OUTPUT_DIR

    utils.warn_for_cpu_devices(device, azureml_run)

    # Set data loaders
    train_loader, validation_loader = setup_dataloaders(settings, output_directory)

    # Update # of class
    nc = train_loader.dataset.num_classes

    # Create model
    model = _create_model(cfg=cfg, number_of_classes=nc, settings=settings)
    model.to(device)
    num_params = sum(x.numel() for x in model.parameters())  # number parameters
    logger.info("[model: {} ({}), # layers: {}, # param: {}]".format(settings[SettingsLiterals.MODEL_NAME],
                                                                     settings['model_size'],
                                                                     len(list(model.parameters())), num_params))

    # Model parameters
    settings['cls'] *= nc / 80.  # scale coco-tuned settings['cls'] to current dataset
    model.nc = nc  # attach number of classes to model
    model.hyp = settings  # attach hyperparameters to model
    model.gr = 1.0  # giou loss ratio (obj_loss = 1.0 or giou)
    model.names = train_loader.dataset.classes
    model.device = device
    # Exponential moving average
    ema = ModelEMA(model)

    # Optimizer
    pg0, pg1, pg2 = [], [], []  # optimizer parameter groups
    for k, v in model.named_parameters():
        if v.requires_grad:
            if '.bias' in k:
                pg2.append(v)  # biases
            elif '.weight' in k and '.bn' not in k:
                pg1.append(v)  # apply weight decay
            else:
                pg0.append(v)  # all else

    optimizer = optim.SGD(pg0, lr=settings['learning_rate'], momentum=settings['momentum'], nesterov=True)
    optimizer.add_param_group({'params': pg1, 'weight_decay': settings['weight_decay']})  # add pg1 with weight_decay
    optimizer.add_param_group({'params': pg2})  # add pg2 (biases)
    del pg0, pg1, pg2

    # Scheduler
    nb = len(train_loader)  # number of batches
    lf_warmpcosine = WarmupCosineSchedule(warmup_steps=nb * 2, t_total=epochs * nb)
    scheduler = optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lf_warmpcosine.lr_lambda)

    log_verbsose_metrics = settings.get(SettingsLiterals.LOG_VERBOSE_METRICS, False)

    # Train
    train(model, ema, optimizer, scheduler, train_loader, validation_loader, tb_writer, azureml_run,
          log_verbsose_metrics)

    # Save Model
    model_name = settings[SettingsLiterals.MODEL_NAME]
    utils._set_train_run_properties(azureml_run, model_name)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    score_script_dir = os.path.join(current_dir, 'writers')

    model_settings = {
        YoloLiterals.BOX_SCORE_THRESH: settings[TrainingLiterals.SCORING_BOX_SCORE_THRESH],
        YoloLiterals.BOX_IOU_THRESH: settings[TrainingLiterals.SCORING_BOX_IOU_THRESH]
    }
    write_model(azureml_run, model, labels=model.names, output_dir=output_directory,
                device=device, score_script_dir=score_script_dir,
                enable_onnx_norm=settings[SettingsLiterals.ENABLE_ONNX_NORMALIZATION],
                model_settings=model_settings, is_yolo=True)

    # Run scoring
    run_scoring = settings.get(SettingsLiterals.OUTPUT_SCORING, False)
    if run_scoring:
        score_validation_data(run=azureml_run, model_settings=model_settings,
                              settings=settings, device=device,
                              score_with_model=_score_with_model)

    utils.log_script_duration(script_start_time, settings, azureml_run)


def _parse_argument_settings(automl_settings):
    """Parse all arguments and merge settings

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    :return: automl settings dictionary with all settings filled in
    :rtype: dict
    """

    parser = argparse.ArgumentParser(description="Object detection - Yolo", allow_abbrev=False)

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
    parser.add_argument(utils._make_arg(TrainingLiterals.LEARNING_RATE), type=float,
                        help="learning rate for optimizer",
                        default=TrainingParameters.DEFAULT_LEARNING_RATE)

    # Yolov5 Settings
    parser.add_argument(utils._make_arg(YoloLiterals.IMG_SIZE), type=int,
                        help='image size for train and val',
                        default=YoloParameters.DEFAULT_IMG_SIZE)
    parser.add_argument(utils._make_arg(YoloLiterals.MODEL_SIZE), type=str,
                        help='model size (small, medium, large, xlarge)',
                        default=YoloParameters.DEFAULT_MODEL_SIZE)
    parser.add_argument(utils._make_arg(YoloLiterals.MULTI_SCALE),
                        help='vary img-size +/- 50%%', action="store_true")

    # inference settings
    parser.add_argument(utils._make_arg(TrainingLiterals.SCORING_BOX_SCORE_THRESH), type=float,
                        help="during inference, only return proposals with a score \
                              greater than box_score_thresh. The score is the multiplication of \
                              the objectness score and classification probability",
                        default=training_settings_defaults[TrainingLiterals.SCORING_BOX_SCORE_THRESH])
    parser.add_argument(utils._make_arg(TrainingLiterals.SCORING_BOX_IOU_THRESH), type=float,
                        help="IOU threshold used during inference in nms post processing",
                        default=training_settings_defaults[TrainingLiterals.SCORING_BOX_IOU_THRESH])

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

    # Update training default settings with yolo specific hyper-parameters
    training_settings_defaults.update(yolo_hyp_defaults)

    # Training settings
    return utils._merge_settings_args_defaults(automl_settings, args_dict, training_settings_defaults), unknown
