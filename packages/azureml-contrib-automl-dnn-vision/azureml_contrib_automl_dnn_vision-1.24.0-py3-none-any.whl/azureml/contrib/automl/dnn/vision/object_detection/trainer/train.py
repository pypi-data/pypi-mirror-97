# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Classes that wrap training steps"""

import copy
import itertools
import json
import os
import time
import torch
from contextlib import nullcontext

from azureml.contrib.automl.dnn.vision.common import utils

from ..eval import cocotools
from ..eval.utils import prepare_bounding_boxes_for_eval
from ..eval.vocmap import VocMap
from ..common import boundingbox, masktools
from ..common.constants import TrainingParameters, ValidationMetricType
from ..common.object_detection_utils import compute_metrics
from ...common import distributed_utils
from ...common.constants import ArtifactLiterals
from ...common.exceptions import AutoMLVisionSystemException
from ...common.logging_utils import get_logger
from ...common.system_meter import SystemMeter
from ...common.trainer.lrschedule import LRSchedulerUpdateType
from ...common.utils import _add_run_properties, _data_exception_safe_iterator, log_end_training_stats
from ...common.average_meter import AverageMeter

logger = get_logger(__name__)


class TrainSettings:
    """Settings for training."""

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional training parameters. Currently supports
          -number_of_epochs: Number of epochs to train for (int)
          -max_patience_iterations: Number of epochs with no validation
          improvement before stopping.
          -primary_metric: Metric that is evaluated and logged by AzureML run object.
          -early_stop_delay_iterations: Number of epochs to wait before tracking validation
          improvement for early stopping.
        :type kwargs: dict
        """

        self._number_of_epochs = kwargs.get(
            "number_of_epochs", TrainingParameters.DEFAULT_NUMBER_EPOCHS)
        self._max_patience_iterations = kwargs.get(
            "max_patience_iterations", TrainingParameters.DEFAULT_PATIENCE_ITERATIONS)
        self.primary_metric = kwargs.get(
            "primary_metric", TrainingParameters.DEFAULT_PRIMARY_METRIC)
        self._early_stop_delay_iterations = kwargs.get(
            "early_stop_delay_iterations", TrainingParameters.DEFAULT_EARLY_STOP_DELAY_ITERATIONS)

    @property
    def number_of_epochs(self):
        """Get number of epochs

        :return: number_of_epochs
        :rtype: int
        """
        return self._number_of_epochs

    @property
    def max_patience_iterations(self):
        """Get number of patience iterations

        :return: max_patience_iterations
        :rtype: int
        """
        return self._max_patience_iterations

    @property
    def early_stop_delay_iterations(self):
        """Get number of iterations to wait before early stop logic is executed.

        :return: early_stop_delay_iterations
        :rtype: int
        """
        return self._early_stop_delay_iterations


def move_images_to_device(images, device):
    """Convenience function to move images to device (gpu/cpu).

    :param images: Batch of images
    :type images: Pytorch tensor
    :param device: Target device
    :type device: Pytorch device
    """

    return [image.to(device) for image in images]


def move_targets_to_device(targets, device):
    """Convenience function to move training targets to device (gpu/cpu)

    :param targets: Batch Training targets (bounding boxes and classes)
    :type targets: Dictionary
    :param device: Target device
    :type device: Pytorch device
    """

    return [{k: v.to(device) for k, v in target.items()} for
            target in targets]


def train_one_epoch(model, optimizer, scheduler, train_data_loader,
                    device, criterion, epoch, print_freq, system_meter):
    """Train a model for one epoch

    :param model: Model to be trained
    :type model: Pytorch nn.Module
    :param optimizer: Optimizer used in training
    :type optimizer: Pytorch optimizer
    :param scheduler: Learning Rate Scheduler wrapper
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_data_loader: Data loader for training data
    :type train_data_loader: Pytorch data loader
    :param device: Target device
    :type device: Pytorch device
    :param criterion: Loss function wrapper
    :type criterion: Object derived from BaseCriterionWrapper (see object_detection.train.criterion)
    :param epoch: Current training epoch
    :type epoch: int
    :param print_freq: How often you want to print the output
    :type print_freq: int
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter: SystemMeter
    """

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    model.train()

    end = time.time()
    uneven_batches_context_manager = model.join() if distributed_utils.dist_available_and_initialized() \
        else nullcontext()

    with uneven_batches_context_manager:
        for i, (images, targets, info) in enumerate(_data_exception_safe_iterator(iter(train_data_loader))):
            # measure data loading time
            data_time.update(time.time() - end)

            images = move_images_to_device(images, device)
            targets = move_targets_to_device(targets, device)

            loss_dict = criterion.evaluate(model, images, targets)
            loss = sum(loss_dict.values())
            loss_value = loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if scheduler.update_type == LRSchedulerUpdateType.BATCH:
                scheduler.lr_scheduler.step()

            # record loss and measure elapsed time
            losses.update(loss_value, len(images))
            batch_time.update(time.time() - end)
            end = time.time()

            # delete tensors which have a valid grad_fn
            del loss, loss_dict

            if i % print_freq == 0 or i == len(train_data_loader) - 1:
                mesg = "Epoch: [{0}][{1}/{2}]\t" "lr: {3}\t" "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t"\
                       "Data {data_time.value:.4f} ({data_time.avg:.4f})\t" "Loss {loss.value:.4f} " \
                       "({loss.avg:.4f})\t".format(epoch, i, len(train_data_loader), optimizer.param_groups[0]["lr"],
                                                   batch_time=batch_time, data_time=data_time, loss=losses)

                mesg += system_meter.get_gpu_stats()
                logger.info(mesg)
                system_meter.log_system_stats(True)

    if scheduler.update_type == LRSchedulerUpdateType.EPOCH:
        scheduler.lr_scheduler.step()


def validate(model, val_data_loader, device, val_index_map, system_meter):
    """Gets model results on validation set.

    :param model: Model to score
    :type mode: Pytorch nn.Module
    :param val_data_loader: Data loader for validation data
    :type val_data_loader: Pytorch Data Loader
    :param device: Target device
    :type device: Pytorch device
    :param val_index_map: Map from numerical indices to class names
    :type val_index_map: List of strings
    :returns: List of detections
    :rtype: List of ImageBoxes (see object_detection.common.boundingbox)
    :param system_meter: A SystemMeter to collect system properties
    :type SystemMeter
    """

    batch_time = AverageMeter()

    model.eval()

    bounding_boxes = []
    end = time.time()
    with torch.no_grad():
        for i, (images, targets, info) in enumerate(_data_exception_safe_iterator(iter(val_data_loader))):
            images = move_images_to_device(images, device)

            labels = model(images)

            for info, label in zip(info, labels):
                image_boxes = boundingbox.ImageBoxes(
                    info["filename"], val_index_map)

                # encode masks as rle to save memory
                masks = label.get("masks", None)
                if masks is not None:
                    masks = masks.cpu()
                    masks = (masks > 0.5)
                    rle_masks = []
                    for mask in masks:
                        rle = masktools.encode_mask_as_rle(mask)
                        rle_masks.append(rle)

                # move predicted labels to cpu
                image_boxes.add_boxes(label["boxes"].cpu(),
                                      label["labels"].cpu(),
                                      label["scores"].cpu(),
                                      rle_masks if masks is not None else None)

                bounding_boxes.append(image_boxes)

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % 100 == 0 or i == len(val_data_loader) - 1:
                mesg = "Test: [{0}/{1}]\t"\
                       "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t".format(i, len(val_data_loader),
                                                                                     batch_time=batch_time)
                mesg += system_meter.get_gpu_stats()
                logger.info(mesg)
                system_meter.log_system_stats(collect_only=True)

    return bounding_boxes


def train(model, optimizer, scheduler,
          train_data_loader, device, criterion,
          train_settings, val_data_loader, val_dataset,
          val_metric_type, val_index_map=None,
          azureml_run=None, ignore_data_errors=True, log_verbsose_metrics=False):
    """Train a model

    :param model: Model to train
    :type model: Object derived from CommonObjectDetectionModelWrapper (see object_detection.models.base_model_wrapper)
    :param optimizer: Model Optimizer
    :type optimizer: Pytorch Optimizer
    :param scheduler: Learning Rate Scheduler wrapper.
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_data_loader: Data loader with training data
    :type train_data_loader: Pytorch data loader
    :param device: Target device (gpu/cpu)
    :type device: Pytorch Device
    :param criterion: Loss function
    :type criterion: Object derived from CommonCriterionWrapper (see object_detection.train.criterion)
    :param train_settings: Settings for training.
    :type train_settings: TrainSettings object
    :param val_data_loader: Data loader with validation data.
    :type val_data_loader: Pytorch data loader
    :param val_dataset: Validation dataset.
    :type val_dataset: CommonObjectDetectionDatasetWrapper (see object_detection.data.datasets)
    :param val_metric_type: Validation metric evaluation type.
    :type val_metric_type: ValidationMetricType.
    :param val_index_map: Map from class indices to class names
    :type val_index_map: List of strings
    :param azureml_run: azureml run object
    :type azureml_run: azureml.core.run.Run
    :param ignore_data_errors: boolean flag to turn on or off errors due to missing or malformed input data
    :type ignore_data_errors: bool
    :param log_verbsose_metrics: Whether to log verbose metrics to Run History
    :type log_verbsose_metrics: bool
    :returns: Trained model
    :rtype: Object derived from CommonObjectDetectionModelWrapper
    """
    epoch_time = AverageMeter()

    base_model = model.model

    distributed = distributed_utils.dist_available_and_initialized()
    master_process = distributed_utils.master_process()

    best_score = 0.0
    best_model = copy.deepcopy(model.get_state_dict())

    no_progress_counter = 0

    # Setup evaluation tools
    val_coco_index = None
    val_vocmap = None
    if val_metric_type in ValidationMetricType.ALL_COCO:
        val_coco_index = cocotools.create_coco_index(val_dataset)
    if val_metric_type in ValidationMetricType.ALL_VOC:
        val_vocmap = VocMap(val_dataset)

    label_metrics = {}

    epoch_end = time.time()
    train_start = time.time()
    coco_metric_time = AverageMeter()
    voc_metric_time = AverageMeter()
    train_sys_meter = SystemMeter()
    valid_sys_meter = SystemMeter()
    for epoch in range(train_settings.number_of_epochs):
        logger.info("Training epoch {}.".format(epoch))

        if distributed:
            if train_data_loader.distributed_sampler is None:
                msg = "train_data_loader.distributed_sampler is None in distributed mode. " \
                      "Cannot shuffle data after each epoch."
                logger.error(msg)
                raise AutoMLVisionSystemException(msg, has_pii=False)
            train_data_loader.distributed_sampler.set_epoch(epoch)

        train_one_epoch(base_model, optimizer, scheduler,
                        train_data_loader, device, criterion, epoch,
                        print_freq=100, system_meter=train_sys_meter)

        bounding_boxes = validate(base_model, val_data_loader, device, val_index_map, valid_sys_meter)
        eval_bounding_boxes = prepare_bounding_boxes_for_eval(bounding_boxes)

        if distributed:
            # Gather eval bounding boxes from all processes.
            eval_bounding_boxes_list = distributed_utils.all_gather(eval_bounding_boxes)
            eval_bounding_boxes = list(itertools.chain.from_iterable(eval_bounding_boxes_list))

            logger.info("Gathered {} eval bounding boxes from all processes.".format(len(eval_bounding_boxes)))

        if not eval_bounding_boxes:
            logger.info("no detected bboxes for evaluation")

        if val_metric_type != ValidationMetricType.NONE:
            map_score = compute_metrics(eval_bounding_boxes, val_metric_type,
                                        val_coco_index, val_vocmap, val_index_map, label_metrics,
                                        coco_metric_time, voc_metric_time, master_process, azureml_run)

            if epoch >= train_settings.early_stop_delay_iterations:
                # Start incrementing no progress counter only after early_stop_delay_iterations.
                no_progress_counter += 1

            if map_score == best_score:
                best_model = copy.deepcopy(model.get_state_dict())
            elif map_score > best_score:
                best_model = copy.deepcopy(model.get_state_dict())
                no_progress_counter = 0
                best_score = map_score

            if master_process and azureml_run is not None:
                azureml_run.log(train_settings.primary_metric, round(map_score, 3))
        else:
            logger.info("val_metric_type is None. Not computing metrics.")
            best_model = copy.deepcopy(model.get_state_dict())

        # measure elapsed time
        epoch_time.update(time.time() - epoch_end)
        epoch_end = time.time()
        mesg = "Epoch-level: [{0}]\t" \
               "Epoch-level Time {epoch_time.value:.4f} ({epoch_time.avg:.4f})".format(epoch, epoch_time=epoch_time)
        logger.info(mesg)

        if no_progress_counter > train_settings.max_patience_iterations:
            break

    # measure total training time
    train_time = time.time() - train_start
    log_end_training_stats(train_time, epoch_time, train_sys_meter, valid_sys_meter)

    if log_verbsose_metrics:
        utils.log_verbose_metrics_to_rh(train_time, epoch_time, train_sys_meter, valid_sys_meter, azureml_run)

    if master_process:
        model.load_state_dict(best_model)
        if azureml_run is not None:
            _add_run_properties(azureml_run, best_score)
        # Write label metrics to output file.
        output_dir = ArtifactLiterals.OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        label_metrics_file_path = os.path.join(output_dir, ArtifactLiterals.LABEL_METRICS_FILE_NAME)
        with open(label_metrics_file_path, 'w') as f:
            json.dump(label_metrics, f)
