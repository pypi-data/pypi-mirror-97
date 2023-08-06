# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" Calculate mAP for evaluating model performance """

import torch
import numpy as np

from ..utils.utils import clip_coords, xywh2xyxy, box_iou, ap_per_class


class MeanAP:
    """
    Class that calculates mAP for object detection
    Note: This code is mainly adapted from https://github.com/ultralytics/yolov5/blob/master/test.py
    """
    def __init__(self, device, nc, nb):
        """
        :param device: device type ('cpu' or 'cuda:0' etc)
        :type device: string
        :param nc: number of classes
        :type nc: int
        :param nb: number of batches
        :type nb: int
        """
        self.device = device
        self.nc = nc
        self.nb = nb
        self.iouv = torch.linspace(0.5, 0.95, 10).to(device)  # iou vector for mAP@0.5:0.95
        self.niou = self.iouv.numel()
        self.stats = []

    def compute_stats(self, img_shape, output, targets):
        """ Compute
        :param img_shape: input image shapes in [batch, channel, height, width]
        :type img_shape: <class 'torch.Size'>
        :param output: detections from non_max_suppression in nx6 (x1, y1, x2, y2, conf, cls)
        :type output: <class 'list'>
        :param targets: ground-truth in mx6 (image index, target class, x center, y center, w, h)
        :type targets: <class 'torch.Tensor'>
        """
        _, _, height, width = img_shape  # batch size, channels, height, width
        whwh = torch.Tensor([width, height, width, height]).to(self.device)

        # Statistics per image
        for si, pred in enumerate(output):
            labels = targets[targets[:, 0] == si, 1:]
            nl = len(labels)
            tcls = labels[:, 0].tolist() if nl else []  # target class

            if pred is None:
                if nl:
                    self.stats.append((torch.zeros(0, self.niou, dtype=torch.bool),
                                       torch.Tensor(), torch.Tensor(), tcls))
                continue

            # Clip boxes to image bounds
            clip_coords(pred, (height, width))

            # Assign all predictions as incorrect
            correct = torch.zeros(pred.shape[0], self.niou, dtype=torch.bool, device=self.device)
            if nl:
                detected = []  # target indices
                tcls_tensor = labels[:, 0]

                # target boxes
                tbox = xywh2xyxy(labels[:, 1:5]) * whwh

                # Per target class
                for cls in torch.unique(tcls_tensor):
                    ti = (cls == tcls_tensor).nonzero().view(-1)  # prediction indices
                    pi = (cls == pred[:, 5]).nonzero().view(-1)  # target indices

                    # Search for detections
                    if pi.shape[0]:
                        # Prediction to target ious
                        ious, idx = box_iou(pred[pi, :4], tbox[ti]).max(1)  # best ious, indices

                        # Append detections
                        for j in (ious > self.iouv[0]).nonzero():
                            d = ti[idx[j]]  # detected target
                            if d not in detected:
                                detected.append(d)
                                correct[pi[j]] = ious[j] > self.iouv  # iou_thres is 1xn
                                if len(detected) == nl:  # all targets already located in image
                                    break

            # Append statistics (correct, conf, pcls, tcls)
            self.stats.append((correct.cpu(), pred[:, 4].cpu(), pred[:, 5].cpu(), tcls))

    def get_scores(self):
        """
        :return: metric scores
        :rtype: tuple of (mean Precision, mean Recall, mean AP@0.5, mean AP@0.5:0.95)
        and <class 'numpy.ndarray'> of (per-class AP@0.5:0.95)
        """
        # Compute scores from the statistics of all images
        stats = [np.concatenate(x, 0) for x in zip(*self.stats)]  # to numpy
        if len(stats):
            p, r, ap, f1, ap_class = ap_per_class(*stats)
            p, r, ap50, ap = p[:, 0], r[:, 0], ap[:, 0], ap.mean(1)  # [P, R, AP@0.5, AP@0.5:0.95]
            mp, mr, map50, map = p.mean(), r.mean(), ap50.mean(), ap.mean()

        # Return results
        maps = np.zeros(self.nc) + map
        for i, c in enumerate(ap_class):
            maps[c] = ap[i]
        return (mp, mr, map50, map), maps
