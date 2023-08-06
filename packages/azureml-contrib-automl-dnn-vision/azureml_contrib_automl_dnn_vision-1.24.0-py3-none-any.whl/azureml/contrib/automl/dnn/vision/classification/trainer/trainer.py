# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Training functions."""

import collections
import copy
import pickle
import time

import numpy as np
from contextlib import nullcontext

try:
    import torch
except ImportError:
    print("ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and "
          "pytorch-ignite separately before running the package.")

from azureml.contrib.automl.dnn.vision.classification.common.constants import MetricsLiterals, TrainingLiterals
from azureml.contrib.automl.dnn.vision.classification.common.transforms import (_get_common_train_transforms,
                                                                                _get_common_valid_transforms)
from azureml.contrib.automl.dnn.vision.classification.io.read.dataloader import _get_data_loader
from azureml.contrib.automl.dnn.vision.classification.models import ModelFactory
from azureml.contrib.automl.dnn.vision.classification.trainer.optimize import (_get_criterion, _get_lr_scheduler,
                                                                               _get_optimizer)
from azureml.contrib.automl.dnn.vision.common import distributed_utils, utils
from azureml.contrib.automl.dnn.vision.common.average_meter import AverageMeter
from azureml.contrib.automl.dnn.vision.common.constants import SettingsLiterals
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionSystemException, AutoMLVisionDataException
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.system_meter import SystemMeter
from azureml.contrib.automl.dnn.vision.common.trainer.lrschedule import LRSchedulerUpdateType
from azureml.contrib.automl.dnn.vision.common.utils import (_accuracy, _add_run_properties, log_end_training_stats,
                                                            _data_exception_safe_iterator)
from azureml.contrib.automl.dnn.vision.metrics import ClassificationMetrics

logger = get_logger(__name__)


def train_model(model_name, strategy, dataset_wrapper, settings, valid_dataset, device=None,
                train_transforms=None, valid_transforms=None, azureml_run=None):
    """
    :param model_name: name of model
    :type model_name: str
    :param strategy: strategy
    :type strategy: str
    :param dataset_wrapper: datasetwrapper object for training
    :type dataset_wrapper: azureml.automl.contrib.dnn.vision.io.read.DatasetWrapper
    :param settings: dictionary containing settings for training
    :type settings: dict
    :param valid_dataset: datasetwrapper object for validation
    :type valid_dataset: azureml.contrib.automl.dnn.vision.io.read.DatasetWrapper
    :param device: device where model should be run (usually "cpu" or "cuda:0" if it is the first gpu)
    :type device: str
    :param train_transforms: transformation function to apply to a pillow image object
    :type train_transforms: function
    :param valid_transforms: transformation function to apply to a pillow image object
    :type valid_transforms: function
    :param azureml_run: azureml run object
    :type azureml_run: azureml.core.Run
    :return: model wrapper object
    :rtype: azureml.contrib.automl.dnn.vision.models.base_model_wrapper.ModelWrapper
    """

    multilabel = settings.get(SettingsLiterals.MULTILABEL, False)

    distributed = distributed_utils.dist_available_and_initialized()
    master_process = distributed_utils.master_process()
    rank = distributed_utils.get_rank()

    # support resume to handle missing classes
    # TODO: Fix in case of distributed training.
    resume_pkl_file = settings.get(SettingsLiterals.RESUME, None)
    if resume_pkl_file:
        with open(resume_pkl_file, "rb") as fp:
            resume_pkl_model = pickle.load(fp)
        dataset_wrapper.reset_labels(resume_pkl_model.labels)

    model_wrapper = ModelFactory().get_model_wrapper(model_name, num_classes=dataset_wrapper.num_classes,
                                                     multilabel=multilabel)

    model_wrapper.model = model_wrapper.model.to(device)

    if distributed:
        model_wrapper.model = torch.nn.parallel.DistributedDataParallel(model_wrapper.model,
                                                                        device_ids=[rank], output_device=rank)
    model_wrapper.distributed = distributed

    num_params = sum([p.data.nelement() for p in model_wrapper.model.parameters()])
    logger.info("[model: {}, #param: {}]".format(model_wrapper.name, num_params))

    num_epochs = settings[TrainingLiterals.NUM_EPOCHS]

    patience = settings[TrainingLiterals.EARLY_STOPPING_PATIENCE]
    batch_size = settings[TrainingLiterals.BATCH_SIZE]
    validation_batch_size = settings[TrainingLiterals.VALIDATION_BATCH_SIZE]

    metrics = ClassificationMetrics(num_classes=dataset_wrapper.num_classes, multilabel=multilabel,
                                    detailed=settings[TrainingLiterals.DETAILED_METRICS])

    optimizer = _get_optimizer(model_wrapper, strategy=strategy, settings=settings)
    criterion = _get_criterion(multilabel=multilabel)

    # check imbalance rate to enable oversampling sampler for multi-class
    classidx_groups = None
    oversample_enable = False
    if not multilabel:
        imbalance_ratio, classidx_groups, weight = _data_analyzer(dataset_wrapper, device=device)
        if imbalance_ratio > settings[TrainingLiterals.IMBALANCE_RATE_THRESHOLD]:
            mesg = "[Data Analysis]: Imbalance ratio: {0} (Oversample: {1}, " \
                   "Weighted loss: {2})".format(imbalance_ratio, bool(settings[TrainingLiterals.OVERSAMPLE]),
                                                bool(settings[TrainingLiterals.WEIGHTED_LOSS]))
            if settings[TrainingLiterals.OVERSAMPLE] and settings[TrainingLiterals.WEIGHTED_LOSS]:
                mesg += ", Either should be set (Neither Enabled)"
            elif settings[TrainingLiterals.OVERSAMPLE]:
                if distributed:
                    mesg += ", Oversample not supported in distributed mode (Neither Enabled)"
                else:
                    oversample_enable = True
                    mesg += ", Oversample Enabled"
            elif settings[TrainingLiterals.WEIGHTED_LOSS]:
                criterion = _get_criterion(multilabel=multilabel, class_weights=weight)
                mesg += ", Weighted loss Enabled"
            else:
                mesg += ", Neither Enabled"
            logger.info(mesg)

    # support resume to load previously trained weights
    # TODO: Fix in case of distributed training.
    if resume_pkl_file:
        model_wrapper.model.load_state_dict(resume_pkl_model.model_wrapper.model.state_dict())
        optimizer.load_state_dict(resume_pkl_model.model_wrapper.optimizer.state_dict())

    best_model_wts = copy.deepcopy(model_wrapper.get_state_dict())
    best_metric = 0

    # set num workers for dataloader
    num_workers = settings.get(SettingsLiterals.NUM_WORKERS, None)

    train_dataloader, valid_dataloader = _get_train_test_dataloaders(dataset_wrapper, valid_dataset=valid_dataset,
                                                                     resize_to_size=model_wrapper.resize_to_size,
                                                                     crop_size=model_wrapper.crop_size,
                                                                     train_transforms=train_transforms,
                                                                     valid_transforms=valid_transforms,
                                                                     batch_size=batch_size,
                                                                     validation_batch_size=validation_batch_size,
                                                                     oversample=oversample_enable,
                                                                     num_workers=num_workers,
                                                                     distributed=distributed)

    logger.info("[start training: "
                "train batch_size: {}, val batch_size: {}]".format(batch_size, validation_batch_size))

    lr_scheduler = _get_lr_scheduler(optimizer, settings=settings, num_epochs=num_epochs,
                                     batches_per_epoch=len(train_dataloader))
    # TODO: Fix in case of distributed training.
    if resume_pkl_file:
        lr_scheduler.lr_scheduler.load_state_dict(
            resume_pkl_model.model_wrapper.lr_scheduler.lr_scheduler.state_dict())

    primary_metric = settings[TrainingLiterals.PRIMARY_METRIC]
    primary_metric_supported = metrics.metric_supported(primary_metric)
    backup_primary_metric = MetricsLiterals.ACCURACY  # Accuracy is always supported.
    if not primary_metric_supported:
        logger.warning("Given primary metric {} is not supported. "
                       "Reporting {} values as {} values.".format(primary_metric,
                                                                  backup_primary_metric, primary_metric))

    no_progress_counter = 0
    epoch_time = AverageMeter()
    epoch_end = time.time()
    train_start = time.time()
    train_sys_meter = SystemMeter()
    valid_sys_meter = SystemMeter()
    for epoch in range(num_epochs):

        if distributed:
            if train_dataloader.distributed_sampler is None:
                msg = "train_dataloader.distributed_sampler is None in distributed mode. " \
                      "Cannot shuffle data after each epoch."
                logger.error(msg)
                raise AutoMLVisionSystemException(msg, has_pii=False)
            train_dataloader.distributed_sampler.set_epoch(epoch)

        _train(model_wrapper, epoch=epoch, dataloader=train_dataloader, criterion=criterion, optimizer=optimizer,
               device=device, multilabel=multilabel, system_meter=train_sys_meter, distributed=distributed,
               lr_scheduler=lr_scheduler)

        _validate(model_wrapper, dataloader=valid_dataloader, metrics=metrics, device=device,
                  multilabel=multilabel, classidx_groups=classidx_groups,
                  system_meter=valid_sys_meter, distributed=distributed)
        computed_metrics = metrics.compute()
        if not primary_metric_supported:
            computed_metrics.update({
                primary_metric: computed_metrics[backup_primary_metric]
            })

        no_progress_counter += 1

        if computed_metrics[primary_metric] == best_metric:
            best_model_wts = copy.deepcopy(model_wrapper.get_state_dict())
        elif computed_metrics[primary_metric] > best_metric:
            best_metric = computed_metrics[primary_metric]
            best_model_wts = copy.deepcopy(model_wrapper.get_state_dict())
            no_progress_counter = 0

        logger.info("Current best metric {0:.3f}".format(best_metric))
        if master_process and azureml_run is not None:
            utils.log_all_metrics(computed_metrics, azureml_run=azureml_run)
        metrics.reset()

        if no_progress_counter >= patience:
            break

        # measure elapsed time
        epoch_time.update(time.time() - epoch_end)
        epoch_end = time.time()
        mesg = "Epoch-level: [{0}]\t" \
               "Epoch-level Time {epoch_time.value:.4f} " \
               "(avg {epoch_time.avg:.4f})".format(epoch, epoch_time=epoch_time)
        logger.info(mesg)

    # measure total training time
    train_time = time.time() - train_start
    log_end_training_stats(train_time, epoch_time, train_sys_meter, valid_sys_meter)

    if settings.get(SettingsLiterals.LOG_VERBOSE_METRICS, False):
        utils.log_verbose_metrics_to_rh(train_time, epoch_time, train_sys_meter, valid_sys_meter, azureml_run)

    model_wrapper.load_state_dict(best_model_wts)
    if master_process and azureml_run is not None:
        _add_run_properties(azureml_run, best_metric)

    # set transformations on model wrapper object
    if valid_transforms is None:
        valid_transforms = _get_common_valid_transforms(resize_to=model_wrapper.resize_to_size,
                                                        crop_size=model_wrapper.crop_size)
    model_wrapper.transforms = valid_transforms
    model_wrapper.optimizer = optimizer
    model_wrapper.lr_scheduler = lr_scheduler

    return model_wrapper


def _get_train_test_dataloaders(
        dataset,
        valid_dataset,
        resize_to_size=None,
        crop_size=None,
        train_transforms=None,
        valid_transforms=None,
        batch_size=None,
        validation_batch_size=None,
        oversample=False,
        num_workers=None,
        distributed=False):
    if train_transforms is None:
        train_transforms = _get_common_train_transforms(crop_size)

    if valid_transforms is None:
        valid_transforms = _get_common_valid_transforms(resize_to=resize_to_size, crop_size=crop_size)

    train_dataloader = _get_data_loader(dataset, is_train=True, transform_fn=train_transforms,
                                        batch_size=batch_size, oversample=oversample, num_workers=num_workers,
                                        distributed=distributed)
    valid_dataloader = _get_data_loader(valid_dataset, transform_fn=valid_transforms,
                                        batch_size=validation_batch_size,
                                        num_workers=num_workers, distributed=distributed)

    return train_dataloader, valid_dataloader


def _train(model_wrapper, epoch, dataloader=None,
           criterion=None, optimizer=None, device=None, multilabel=False,
           system_meter=None, distributed=False, lr_scheduler=None):

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()

    model_wrapper.model.train()

    end = time.time()
    uneven_batches_context_manager = model_wrapper.model.join() if \
        distributed_utils.dist_available_and_initialized() else nullcontext()

    with uneven_batches_context_manager:
        for i, (inputs, labels) in enumerate(_data_exception_safe_iterator(iter(dataloader))):
            # measure data loading time
            data_time.update(time.time() - end)

            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model_wrapper.model(inputs)
            loss = criterion(outputs, labels)
            loss_value = loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if lr_scheduler.update_type == LRSchedulerUpdateType.BATCH:
                lr_scheduler.lr_scheduler.step()

            if not multilabel:
                # record loss and measure elapsed time
                prec1 = _accuracy(outputs.data, labels)
                top1.update(prec1[0][0], inputs.size(0))
            losses.update(loss_value, inputs.size(0))

            batch_time.update(time.time() - end)
            end = time.time()

            # delete tensors which have a valid grad_fn
            del loss, outputs

            last_batch = i == len(dataloader) - 1
            if i % 100 == 0 or last_batch:
                msg = "Epoch: [{0}][{1}/{2}]\t" "lr: {3}\t" "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t"\
                      "Data {data_time.value:.4f} ({data_time.avg:.4f})\t" "Loss {loss.value:.4f} " \
                      "({loss.avg:.4f})\t".format(epoch, i, len(dataloader), optimizer.param_groups[0]["lr"],
                                                  batch_time=batch_time, data_time=data_time, loss=losses)
                if not multilabel:
                    msg += "Acc@1 {top1.value:.3f} ({top1.avg:.3f})\t".format(top1=top1)

                msg += system_meter.get_gpu_stats()
                logger.info(msg)
                system_meter.log_system_stats(True)

    if lr_scheduler.update_type == LRSchedulerUpdateType.EPOCH:
        lr_scheduler.lr_scheduler.step()


def _update_metrics_and_confusion_matrix(metrics, confusion_matrix, outputs, labels, model_wrapper, multilabel):
    probs = model_wrapper.predict_probs_from_outputs(outputs)
    preds = model_wrapper.predict_from_outputs(outputs)
    metrics.update(probs=probs, preds=preds, labels=labels)

    if not multilabel:
        for t, p in zip(labels.view(-1), preds.view(-1)):
            confusion_matrix[t.data.item(), p.data.item()] += 1


def _validate(model_wrapper, dataloader=None, metrics=None, device=None, multilabel=False,
              classidx_groups=None, system_meter=None, distributed=False):
    batch_time = AverageMeter()
    top1 = AverageMeter()

    confusion_matrix = None
    if not multilabel:
        num_classes = len(dataloader.dataset.labels)
        confusion_matrix = torch.zeros(num_classes, num_classes)

    model_wrapper.model.eval()

    total_outputs_list = []
    total_labels_list = []

    end = time.time()
    with torch.no_grad():
        for i, (inputs, labels) in enumerate(_data_exception_safe_iterator(iter(dataloader))):
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model_wrapper.model(inputs)
            _update_metrics_and_confusion_matrix(metrics, confusion_matrix, outputs, labels, model_wrapper, multilabel)

            total_outputs_list.append(outputs)
            total_labels_list.append(labels)

            if not multilabel:
                prec1 = _accuracy(outputs.data, labels)
                top1.update(prec1[0][0], inputs.size(0))

            # measure elapsed time
            batch_time.update(time.time() - end)
            end = time.time()

            if i % 100 == 0 or i == len(dataloader) - 1:
                mesg = "Test: [{0}/{1}]\t"\
                       "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t".format(i, len(dataloader),
                                                                                     batch_time=batch_time)
                if not multilabel:
                    mesg += "Acc@1 {top1.value:.3f} ({top1.avg:.3f})\t".format(top1=top1)
                mesg += system_meter.get_gpu_stats()
                logger.info(mesg)
                system_meter.log_system_stats(True)

    if not total_labels_list:
        exception_message = "All images in the validation set processed by worker {} are invalid. " \
                            "Cannot compute primary metric.".format(distributed_utils.get_rank())
        raise AutoMLVisionDataException(exception_message, has_pii=False)

    if distributed:
        # Gather metrics data from other workers.
        outputs_list = distributed_utils.all_gather_uneven_tensors(torch.cat(total_outputs_list))
        labels_list = distributed_utils.all_gather_uneven_tensors(torch.cat(total_labels_list))
        if len(outputs_list) != len(labels_list):
            raise AutoMLVisionSystemException("Outputs list is of size {} and labels list is of size {}. "
                                              "Both lists should be of same size after all_gather."
                                              .format(len(outputs_list), len(labels_list)), has_pii=False)

        for index, outputs in enumerate(outputs_list):
            if index != distributed_utils.get_rank():
                _update_metrics_and_confusion_matrix(metrics, confusion_matrix, outputs, labels_list[index],
                                                     model_wrapper, multilabel)

    if not multilabel:
        # per-class accuracy
        fine_grained_acc = __confusion_matrix_analyzer(confusion_matrix, classidx_groups)
        logger.info("Avg per-class accuracy: {0:.3f} (high_freq gr: {1:.3f}, mid_freq gr: {2:.3f}, "
                    "low_freq gr: {3:.3f})".format(fine_grained_acc["avg_per-class"],
                                                   fine_grained_acc["high_freq"],
                                                   fine_grained_acc["mid_freq"],
                                                   fine_grained_acc["low_freq"]))

    return metrics


def _data_analyzer(dataset_wrapper, device=None):
    """Analyze data to determine imbalance ratio and group classes into 3 sub groups based on the frequencies.

    :param dataset_wrapper: dataset wrapper
    :type dataset_wrapper: azureml.contrib.automl.dnn.vision.io.read.dataset_wrapper.BaseDatasetWrapper
    :param device: device where model should be run (usually "cpu" or "cuda:0" if it is the first gpu)
    :type device: str
    :return: imbalance_ratio: data imbalance ratio
    :rtype: imbalance_ratio: int
    :return: classidx_groups: class indices group based on the frequencies
    :rtype: classidx_groups: dictionary
    :return: weights: class-level rescaling weights for CrossEntropyLoss() for imbalance data
    :rtype: weights: torch.Tensor
    """
    images2label = dataset_wrapper._CommonImageDatasetWrapper__files_to_labels_dict
    class_weights = [0] * dataset_wrapper.num_classes
    for key in images2label:
        label_idx = dataset_wrapper.label_to_index_map[images2label[key]]
        class_weights[label_idx] += 1

    sorted_weights_index = sorted(range(len(class_weights)), key=lambda k: class_weights[k])

    classidx_groups = {}
    block = len(sorted_weights_index) // 3
    classidx_groups["low_freq"] = sorted_weights_index[:block]
    classidx_groups["high_freq"] = sorted_weights_index[-block:]

    weights = torch.FloatTensor(class_weights).to(device)
    weights = 1. / weights
    weights[weights == float("Inf")] = 0

    imbalance_ratio = max(class_weights) // max(1, min(class_weights))
    return imbalance_ratio, classidx_groups, weights


def __confusion_matrix_analyzer(confusion_matrix, classidx_groups):
    """Confusion matrix to calculate per-class accuracy
    and using this per-class accuracy to provide group-level accuracy

    :param confusion_matrix: confusion matrix (num of classes by num of classes)
    :type confusion_matrix: torch.Tensor
    :param classidx_groups: class indices group based on the frequencies
    :type classidx_groups: dictionary
    :return: accuracy (avg per-class accuracy, group-level accuracy)
    :rtype: dictionary
    """
    per_class_accuracy = confusion_matrix.diag() / confusion_matrix.sum(1)
    per_class_accuracy = per_class_accuracy.numpy()

    high_group_acc = []
    mid_group_acc = []
    low_group_acc = []
    for idx, class_accuracy in enumerate(per_class_accuracy):
        if idx in classidx_groups["high_freq"]:
            high_group_acc.append(class_accuracy)
        elif idx in classidx_groups["low_freq"]:
            low_group_acc.append(class_accuracy)
        else:
            mid_group_acc.append(class_accuracy)

    acc = collections.defaultdict()
    acc["avg_per-class"] = np.nanmean(per_class_accuracy) * 100
    acc["high_freq"] = np.nanmean(high_group_acc) * 100
    acc["mid_freq"] = np.nanmean(mid_group_acc) * 100
    acc["low_freq"] = np.nanmean(low_group_acc) * 100
    return acc
