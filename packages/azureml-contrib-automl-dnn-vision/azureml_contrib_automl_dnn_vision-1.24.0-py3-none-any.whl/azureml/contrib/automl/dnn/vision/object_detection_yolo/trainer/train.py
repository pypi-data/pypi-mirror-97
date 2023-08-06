# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" Contain functions for training and validation """

import copy
import logging
import math
import random
import time

import torch
from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.average_meter import AverageMeter
from azureml.contrib.automl.dnn.vision.common.system_meter import SystemMeter
from azureml.contrib.automl.dnn.vision.object_detection_yolo.common.constants import TrainingLiterals, YoloLiterals
from azureml.contrib.automl.dnn.vision.object_detection_yolo.eval.mean_ap import MeanAP
from azureml.contrib.automl.dnn.vision.object_detection_yolo.utils.utils import compute_loss, non_max_suppression

logger = logging.getLogger(__name__)


def train_one_epoch(model, ema, optimizer, scheduler, train_loader,
                    epoch, device, system_meter, print_freq=100, tb_writer=None):
    """Train a model for one epoch

    :param model: Model to train
    :type model: <class 'azureml.contrib.automl.dnn.vision.object_detection_yolo.models.yolo.Model'>
    :param ema: Model Exponential Moving Average
    :type ema: <class 'azureml.contrib.automl.dnn.vision.object_detection_yolo.utils.torch_utils.ModelEMA'>
    :param optimizer: Model Optimizer
    :type optimizer: Pytorch Optimizer <class 'torch.optim.sgd.SGD'>
    :param scheduler: Learning Rate Scheduler wrapper.
    :type scheduler: <class 'torch.optim.lr_scheduler.LambdaLR'>
    :param train_loader: Data loader for training data
    :type train_loader: Pytorch data loader
    :param epoch: Current training epoch
    :type epoch: int
    :param device: Target device
    :type device: Pytorch device
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter: SystemMeter
    :param print_freq: How often you want to print the output
    :type print_freq: int
    :param tb_writer: Tensorboard writer
    :type tb_writer: <class 'torch.utils.tensorboard.writer.SummaryWriter'>
    :returns: mean losses for tensorboard writer
    :rtype: <class 'torch.Tensor'>
    """

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    nb = len(train_loader)
    mloss = torch.zeros(4, device=device)  # mean losses (lbox, lobj, lcls, loss)

    model.train()

    end = time.time()
    for i, (imgs, targets, _) in enumerate(utils._data_exception_safe_iterator(iter(train_loader))):
        # measure data loading time
        data_time.update(time.time() - end)

        ni = i + nb * epoch  # number integrated batches (since train start)
        imgs = imgs.to(device).float() / 255.0  # uint8 to float32, 0 - 255 to 0.0 - 1.0

        # Multi scale : need more CUDA memory for bigger image size
        if model.hyp['multi_scale']:
            imgsz = model.hyp['img_size']
            gs = model.hyp['gs']
            sz = random.randrange(imgsz * 0.5, imgsz * 1.5 + gs) // gs * gs
            sf = sz / max(imgs.shape[2:])
            if sf != 1:
                ns = [math.ceil(x * sf / gs) * gs for x in imgs.shape[2:]]  # new shape (stretched to gs-multiple)
                imgs = torch.nn.functional.interpolate(imgs, size=ns, mode='bilinear', align_corners=False)

        # Forward
        pred = model(imgs)

        # Loss
        loss, loss_items = compute_loss(pred, targets.to(device), model)
        loss.backward()

        optimizer.step()
        optimizer.zero_grad()
        ema.update(model)

        # Scheduler per step
        scheduler.step()
        # Tensorboard
        if tb_writer:
            tb_writer.add_scalar('lr', scheduler.get_last_lr()[0], ni)

        # record loss and measure elapsed time
        losses.update(loss.item(), len(imgs))
        mloss = (mloss * i + loss_items) / (i + 1)  # update mean losses
        batch_time.update(time.time() - end)
        end = time.time()

        # delete tensors which have a valid grad_fn
        del loss, pred

        if i % print_freq == 0 or i == nb - 1:
            mesg = "Epoch: [{0}][{1}/{2}]\t" "lr: {3:.5f}\t" "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t"\
                   "Data {data_time.value:.4f} ({data_time.avg:.4f})\t" "Loss {loss.value:.4f} " \
                   "({loss.avg:.4f})\t".format(epoch, i, nb, optimizer.param_groups[0]["lr"],
                                               batch_time=batch_time, data_time=data_time, loss=losses)

            mesg += system_meter.get_gpu_stats()
            logger.info(mesg)
            system_meter.log_system_stats(True)

    return mloss


def validate(model, validation_loader, device, system_meter, conf_thres, iou_thres, print_freq=100):
    """Gets model results on validation set.

    :param model: Model to score
    :type mode: Pytorch nn.Module
    :param validation_loader: Data loader for validation data
    :type validation_loader: Pytorch Data Loader
    :param device: Target device
    :type device: Pytorch device
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter
    :param conf_thres: Confidence threshold
    :type conf_thres: float
    :param iou_thres: IOU threshold
    :type iou_thres: float
    :param print_freq: How often you want to print the output
    :type print_freq: int
    :return: metric scores
    :rtype: tuple of (mean Precision, mean Recall, mean AP@0.5, mean AP@0.5:0.95)
    and <class 'numpy.ndarray'> of (per-class AP@0.5:0.95)
    """

    batch_time = AverageMeter()

    nc = len(model.names)   # number of classes
    nb = len(validation_loader)
    mAP = MeanAP(device, nc=nc, nb=nb)

    model.eval()

    end = time.time()
    for i, (imgs, targets, _) in enumerate(utils._data_exception_safe_iterator(iter(validation_loader))):
        imgs = imgs.to(device).float() / 255.0
        targets = targets.to(device)

        with torch.no_grad():
            # inference and training outputs
            inf_out, _ = model(imgs)

            # TODO: expose multi_label as arg to enable multi labels per box
            # Run NMS
            output = non_max_suppression(inf_out, conf_thres, iou_thres, multi_label=False)

        # TODO: use val_vocmap like faster-rcnn or vice versa?
        mAP.compute_stats(imgs.shape, output, targets)

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0 or i == nb - 1:
            mesg = "Test: [{0}/{1}]\t" \
                   "Time {batch_time.value:.4f} ({batch_time.avg:.4f})\t".format(i, nb,
                                                                                 batch_time=batch_time)
            mesg += system_meter.get_gpu_stats()
            logger.info(mesg)
            system_meter.log_system_stats(True)

    return mAP.get_scores()


def train(model, ema, optimizer, scheduler, train_loader, validation_loader, tb_writer=None, azureml_run=None,
          log_verbsose_metrics=False):
    """Train a model

    :param model: Model to train
    :type model: <class 'azureml.contrib.automl.dnn.vision.object_detection_yolo.models.yolo.Model'>
    :param ema: Model Exponential Moving Average
    :type ema: <class 'azureml.contrib.automl.dnn.vision.object_detection_yolo.utils.torch_utils.ModelEMA'>
    :param optimizer: Model Optimizer
    :type optimizer: Pytorch Optimizer <class 'torch.optim.sgd.SGD'>
    :param scheduler: Learning Rate Scheduler wrapper.
    :type scheduler: <class 'torch.optim.lr_scheduler.LambdaLR'>
    :param train_loader: Data loader with training data
    :type train_loader: Pytorch data loader
    :param validation_loader: Data loader with validation data
    :type validation_loader: Pytorch data loader
    :param tb_writer: Tensorboard writer
    :type tb_writer: <class 'torch.utils.tensorboard.writer.SummaryWriter'>
    :param azureml_run: azureml run object
    :type azureml_run: azureml.core.run.Run
    :param log_verbsose_metrics: Whether to log verbose metrics to Run History
    :type log_verbsose_metrics: bool
    """

    epoch_time = AverageMeter()

    base_model = model
    base_model.to(model.device)

    best_score = 0.0
    best_model = copy.deepcopy(base_model.state_dict())

    no_progress_counter = 0
    device = model.device
    epochs = model.hyp[TrainingLiterals.NUMBER_OF_EPOCHS]
    primary_metric = model.hyp[TrainingLiterals.PRIMARY_METRIC]
    max_patience_iterations = model.hyp[TrainingLiterals.MAX_PATIENCE_ITERATIONS]
    conf_thres = model.hyp[YoloLiterals.BOX_SCORE_THRESH]
    iou_thres = model.hyp[YoloLiterals.BOX_IOU_THRESH]

    epoch_end = time.time()
    train_start = time.time()
    train_sys_meter = SystemMeter()
    valid_sys_meter = SystemMeter()

    for epoch in range(epochs):

        mloss = train_one_epoch(base_model, ema, optimizer, scheduler, train_loader, epoch, device,
                                system_meter=train_sys_meter, tb_writer=tb_writer)

        ema.update_attr(model)

        final_epoch = epoch + 1 == epochs
        if epoch % 5 == 0 or final_epoch:
            results, maps = validate(ema.ema, validation_loader, device, valid_sys_meter, conf_thres, iou_thres)
            map50 = results[2]
            # TODO: expose all the metrics (P, R, AP@0.5, AP@0.5:0.95) and per-class AP
            logger.info("[MAP@0.5] score: {}".format(round(map50, 3)))

            # update early stopping counter
            no_progress_counter += 1
            if map50 >= best_score:
                best_model = copy.deepcopy(ema.ema.state_dict())
            if map50 > best_score:
                best_score = map50
                no_progress_counter = 0

            if azureml_run is not None:
                azureml_run.log("average_precision_score_macro", round(map50, 3))  # for backwards compatibility
                azureml_run.log(primary_metric, round(map50, 3))

        # Tensorboard
        if tb_writer:
            tags = ['train/giou_loss', 'train/obj_loss', 'train/cls_loss',
                    'metrics/precision', 'metrics/recall', 'metrics/mAP_0.5', 'metrics/mAP']
            for x, tag in zip(list(mloss[:-1]) + list(results), tags):
                tb_writer.add_scalar(tag, x, epoch)

        # measure elapsed time
        epoch_time.update(time.time() - epoch_end)
        epoch_end = time.time()
        mesg = "Epoch-level: [{0}]\t" \
               "Epoch-level Time {epoch_time.value:.4f} ({epoch_time.avg:.4f})".format(epoch, epoch_time=epoch_time)
        logger.info(mesg)

        if no_progress_counter > max_patience_iterations:
            break

    # measure total training time
    train_time = time.time() - train_start
    utils.log_end_training_stats(train_time, epoch_time, train_sys_meter, valid_sys_meter)

    if log_verbsose_metrics:
        utils.log_verbose_metrics_to_rh(train_time, epoch_time, train_sys_meter, valid_sys_meter, azureml_run)

    base_model.load_state_dict(best_model)
    # make sure it's not in training mode
    base_model.eval()

    logger.info("[MAP@0.5] BEST score: {}".format(round(best_score, 3)))
    if azureml_run is not None:
        utils._add_run_properties(azureml_run, best_score)
