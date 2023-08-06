# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Tools for using using pycocotools for evaluating model performance."""

from .utils import prepare_dataset_for_eval
from ...common.logging_utils import get_logger

logger = get_logger(__name__)

coco_supported = False
try:
    from pycocotools.coco import COCO
    from pycocotools.cocoeval import COCOeval
    coco_supported = True
except ImportError:
    logger.warning("Pycocotools import failed. Coco Map score computation is not supported.")
    coco_supported = False


def create_coco_index(dataset):
    """Creates a cocotools index from a dataset

    :param dataset: Dataset for evaluations
    :type dataset: CommonObjectDetectionDatasetWrapper object (see object_detection.data.datasets)
    :return: Index created from dataset
    :rtype: cocotools index object
    """
    if not coco_supported:
        logger.warning("Pycocotools import failed. Returning None for coco_index")
        return None

    coco_dataset = COCO()
    coco_dataset.dataset = prepare_dataset_for_eval(dataset)
    coco_dataset.createIndex()

    return coco_dataset


def score_from_index(coco_index, boxes, task='bbox'):
    """Scores the a set of bounding box records from an index created from a set of ground truth bounding boxes.

    :param coco_index: Ground truth index
    :type coco_index: cocotools index object
    :param boxes: Detections for a set of images
    :type boxes: List of ImageBoxes (see object_detection.common.boundingbox)
    :param task: Task - either bbox or segm, depending on which scoring task for pycocotools
    :type: str
    :returns: List of scores - [CocoMAP (all sizes),
        MAP@IoU0.5 (all sizes),
        MAP@IoU0.75 (all sizes),
        CocoMAP (small),
        CocoMAP (medium),
        CocoMAP (large),
        CocoAR (all sizes, max detections 1),
        CocoAR (all sizes, max detections 10),
        CocoAR (all sizes, max detections 100),
        CocoAR (small, max detections 100),
        CocoAR (medium, max detections 100),
        CocoAR (large, max detections 100)]
        please refer to the coco challenge: cocodataset.org for detailed description of these metrics.
    :rtype: List of floats
    """
    if not coco_supported:
        logger.warning("Pycocotools import failed. Returning 0 for coco map scores.")
        return [0.] * 12

    # No detections
    if len(boxes) == 0:
        return [0.] * 12

    coco_detections = coco_index.loadRes(boxes)
    cocoEval = COCOeval(coco_index, coco_detections, task)
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()

    return cocoEval.stats


def score(dataset, boxes, task="bbox"):
    """Scores the a set of bounding box records from a set of ground truth bounding boxes.

    :param dataset: Dataset with ground truth data used for evaluation
    :type dataset: CommonObjectDetectionDatasetWrapper object (see object_detection.data.datasets)
    :param boxes: Detections for a set of images
    :type boxes: List of ImageBoxes (see object_detection.common.boundingbox)
    :param task: Task - either bbox or segm, depending on which scoring task for pycocotools
    :type: str
    :returns: List of scores - [CocoMAP (all sizes),
        MAP@IoU0.5 (all sizes),
        MAP@IoU0.75 (all sizes),
        CocoMAP (small),
        CocoMAP (medium),
        CocoMAP (large),
        CocoAR (all sizes, max detections 1),
        CocoAR (all sizes, max detections 10),
        CocoAR (all sizes, max detections 100),
        CocoAR (small, max detections 100),
        CocoAR (medium, max detections 100),
        CocoAR (large, max detections 100)]
        please refer to the coco challenge: cocodataset.org for detailed description of these metrics.
    :rtype: List of floats
    """
    if not coco_supported:
        logger.warning("Pycocotools import failed. Returning 0 for coco map scores.")
        return [0.] * 12

    coco_dataset = COCO()
    coco_dataset.dataset = prepare_dataset_for_eval(dataset)
    coco_dataset.createIndex()
    coco_detections = coco_dataset.loadRes(boxes)
    cocoEval = COCOeval(coco_dataset, coco_detections, task)
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()

    return cocoEval.stats
