import os
import numpy as np
import pytest
import torch
import unittest.mock as mock

from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionSystemException
from azureml.contrib.automl.dnn.vision.object_detection.common import masktools
from azureml.contrib.automl.dnn.vision.object_detection.data.datasets import FileObjectDetectionDatasetWrapper
from azureml.contrib.automl.dnn.vision.object_detection.eval.vocmap import _map_score_voc_11_point_metric, \
    _map_score_voc_auc, VocMap

from pycocotools import mask as pycoco_mask


class TestVocMap:
    @staticmethod
    def _setup_vocmap_object():
        data_root = "object_detection_data"
        image_root = os.path.join(data_root, "images")
        annotation_file = os.path.join(data_root, "missing_image_annotations.json")
        dataset = FileObjectDetectionDatasetWrapper(annotations_file=annotation_file,
                                                    image_folder=image_root,
                                                    ignore_data_errors=True)
        return VocMap(dataset)

    @staticmethod
    def _rle_mask_from_bbox(bbox, height, width):
        x1, y1, x2, y2 = bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]
        polygon = [[x1, y1, x2, y1, x2, y2, x1, y2, x1, y1]]
        rle_masks = masktools.convert_polygon_to_rle_masks(polygon, height, width)
        return rle_masks[0]

    @staticmethod
    def _create_annotation(task, image_id, bbox, label, iscrowd, height, width):
        result = {"image_id": image_id, "bbox": bbox, "category_id": label, "iscrowd": iscrowd}
        if task == "segm":
            result.update({"segmentation": TestVocMap._rle_mask_from_bbox(bbox, height, width)})
        return result

    @staticmethod
    def _create_prediction(task, image_id, bbox, label, score, height, width):
        result = {"image_id": image_id, "bbox": bbox, "category_id": label, "score": score}
        if task == "segm":
            result.update({"segmentation": TestVocMap._rle_mask_from_bbox(bbox, height, width)})
        return result

    def test_map_using_11_point_metric(self):
        # Precision list and recall list should be of equal size.
        precision_list = torch.rand(10, dtype=torch.float)
        recall_list = torch.rand(5, dtype=torch.float)
        with pytest.raises(AutoMLVisionSystemException):
            _map_score_voc_11_point_metric(precision_list, recall_list)

        # Empty lists should succeed.
        precision_list = torch.tensor([], dtype=torch.float)
        recall_list = torch.tensor([], dtype=torch.float)
        _map_score_voc_11_point_metric(precision_list, recall_list)

        precision_list = torch.rand(10, dtype=torch.float)
        recall_list = torch.rand(10, dtype=torch.float)
        map_score = _map_score_voc_11_point_metric(precision_list, recall_list)
        assert map_score.ndim == 0  # Scalar value

        # recall list with duplicate values.
        recall_list = torch.arange(0.0, 1.1, 0.1, dtype=torch.float)
        recall_list, _ = torch.sort(torch.cat((recall_list, recall_list, recall_list)))
        orig_precision_list = torch.rand(11, dtype=torch.float)
        precision_list, _ = torch.sort(torch.cat((orig_precision_list, orig_precision_list, orig_precision_list)),
                                       descending=True)
        map_score = _map_score_voc_11_point_metric(precision_list, recall_list)
        # Since precision list is sorted, max precision at 11 recall points corresponding entry in orig_precision_list.
        # map score would be the average of the orig_precision_list.
        expected_map_score = orig_precision_list.sum() / orig_precision_list.nelement()
        assert round(map_score.item(), 3) == round(expected_map_score.item(), 3)

    def test_map_using_auc_metric(self):
        # Precision list and recall list should be of same shape
        precision_list = torch.rand(10, dtype=torch.float)
        recall_list = torch.rand(5, dtype=torch.float)
        with pytest.raises(AutoMLVisionSystemException):
            _map_score_voc_auc(precision_list, recall_list)

        # Recall list should be sorted in ascending order.
        precision_list = torch.rand(10, dtype=torch.float)
        recall_list = torch.arange(1.0, 0.0, -0.1, dtype=torch.float)
        with pytest.raises(AutoMLVisionSystemException):
            _map_score_voc_auc(precision_list, recall_list)

        # Empty precision and recall list
        _map_score_voc_auc(torch.tensor([]), torch.tensor([]))

        recall_list, _ = torch.sort(torch.rand(10, dtype=torch.float))
        map_score = _map_score_voc_auc(precision_list, recall_list)
        assert map_score.ndim == 0

        # Check with single recall value to verify unique recall list logic.
        recall_list = torch.zeros(10, dtype=torch.float)
        map_score = _map_score_voc_auc(precision_list, recall_list)
        assert map_score.ndim == 0

        # recall_list with duplicate values.
        recall_list = torch.arange(0.1, 1.1, 0.1, dtype=torch.float)
        recall_list, _ = torch.sort(torch.cat((recall_list, recall_list, recall_list)))
        orig_precision_list = torch.rand(10, dtype=torch.float)
        precision_list, _ = torch.sort(torch.cat((orig_precision_list, orig_precision_list, orig_precision_list)),
                                       descending=True)
        map_score = _map_score_voc_auc(precision_list, recall_list)
        assert map_score.ndim == 0
        expected_map_score = torch.sum(orig_precision_list) * 0.1
        assert round(map_score.item(), 3) == round(expected_map_score.item(), 3)

    @pytest.mark.usefixtures("new_clean_dir")
    @pytest.mark.parametrize("task", ["bbox", "segm"])
    @mock.patch(pycoco_mask.__name__ + ".iou")
    def test_categorize_prediction_iou_type(self, mock_mask, task):
        vocmap = self._setup_vocmap_object()
        height = 600
        width = 900

        mock_mask.return_value = np.array([[1.0]])
        bbox = [0, 0, 299, 199]
        rle_mask = self._rle_mask_from_bbox(bbox, height, width)

        gts = [self._create_annotation(task, "1", bbox, "label1", False, height, width)]
        detected_gts = torch.zeros(len(gts), dtype=torch.uint8)
        prediction = self._create_prediction(task, "1", bbox, "label1", 0.5, height, width)
        vocmap._categorize_prediction(prediction, gts, detected_gts, task)

        if task == "bbox":
            mock_mask.assert_called_once_with([bbox], [bbox], [0])
        else:
            mock_mask.assert_called_once_with([rle_mask], [rle_mask], [0])

    @pytest.mark.usefixtures("new_clean_dir")
    @pytest.mark.parametrize("task", ["bbox", "segm"])
    def test_categorize_prediction(self, task):
        vocmap = self._setup_vocmap_object()
        height = 600
        width = 900

        gts = [self._create_annotation(task, "1", [0, 0, 299, 199], "label1", False, height, width),
               self._create_annotation(task, "2", [0, 0, 299, 199], "label1", False, height, width),
               self._create_annotation(task, "1", [300, 200, 299, 199], "label1", False, height, width),
               self._create_annotation(task, "1", [600, 400, 299, 199], "label1", True, height, width)]
        detected_gts = torch.zeros(len(gts), dtype=torch.uint8)

        # No image gts should return false positive.
        prediction = self._create_prediction(task, "3", [0, 0, 299, 199], "label1", 0.5, height, width)
        result = vocmap._categorize_prediction(prediction, gts, detected_gts, task)
        assert result == 0

        # Prediction should match with gts from same image.
        prediction = self._create_prediction(task, "2", [0, 0, 299, 199], "label1", 0.5, height, width)
        result = vocmap._categorize_prediction(prediction, gts, detected_gts, task)
        assert result == 1
        assert detected_gts[1] == 1
        prediction = self._create_prediction(task, "1", [0, 0, 299, 199], "label1", 0.5, height, width)
        result = vocmap._categorize_prediction(prediction, gts, detected_gts, task)
        assert result == 1
        assert detected_gts[0] == 1

        # Prediction matching a new gt.
        prediction = self._create_prediction(task, "1", [300, 200, 299, 199], "label1", 0.5, height, width)
        result = vocmap._categorize_prediction(prediction, gts, detected_gts, task)
        assert result == 1
        assert detected_gts[2] == 1
        # Prediction matching an already detected gt should return false positive.
        result = vocmap._categorize_prediction(prediction, gts, detected_gts, task)
        assert result == 0

        # Prediction matching "iscrowd" should return neither false positive nor true positive
        prediction = self._create_prediction(task, "1", [600, 400, 299, 199], "label1", 0.5, height, width)
        result = vocmap._categorize_prediction(prediction, gts, detected_gts, task)
        assert result == 2

        # Prediction whose best iou match < iou threshold should return false positive
        prediction = self._create_prediction(task, "1", [0, 0, 149, 99], "label1", 0.5, height, width)
        result = vocmap._categorize_prediction(prediction, gts, detected_gts, task)
        assert result == 0

    @pytest.mark.usefixtures("new_clean_dir")
    @pytest.mark.parametrize("task", ["bbox", "segm"])
    def test_precision_recall_curve(self, task):
        vocmap = self._setup_vocmap_object()
        height = 600
        width = 900

        # Mock vocmap._label_gts and vocmap._labels
        label1 = "label1"
        label2 = "label2"
        vocmap._labels.extend([label1, label2])
        vocmap._label_gts[label1] = [
            self._create_annotation(task, "1", [0, 0, 299, 199], label1, False, height, width),
            self._create_annotation(task, "2", [0, 0, 299, 199], label1, False, height, width),
            self._create_annotation(task, "1", [600, 400, 299, 199], label1, True, height, width)
        ]
        # label 2 with only "iscrowd" gts.
        vocmap._label_gts[label2] = [
            self._create_annotation(task, "1", [0, 0, 299, 199], label2, True, height, width),
            self._create_annotation(task, "2", [0, 0, 299, 199], label2, True, height, width)
        ]

        # Empty list of predictions
        predictions = []
        precision_list, recall_list = vocmap._precision_recall_curve(predictions, label1, task)
        assert precision_list.nelement() == 0
        assert recall_list.nelement() == 0

        # If there are no non crowd gts, return None
        predictions = [
            self._create_prediction(task, "1", [0, 0, 299, 199], label2, 0.5, height, width)
        ]
        precision_list, recall_list = vocmap._precision_recall_curve(predictions, label2, task)
        assert precision_list is None
        assert recall_list is None

        # Should not fail due to division by 0 when true positive and false positives are zero
        predictions = [
            self._create_prediction(task, "1", [600, 400, 299, 199], label1, 0.5, height, width)  # matches "iscrowd"
        ]
        precision_list, recall_list = vocmap._precision_recall_curve(predictions, label1, task)
        assert torch.all(torch.eq(precision_list, torch.tensor([0], dtype=torch.float)))
        assert torch.all(torch.eq(recall_list, torch.tensor([0], dtype=torch.float)))

        # List of predictions unsorted by score
        predictions = [
            self._create_prediction(task, "1", [0, 0, 299, 199], label1, 0.8, height, width),  # tp
            self._create_prediction(task, "2", [0, 0, 299, 199], label1, 0.5, height, width),  # tp
            self._create_prediction(task, "3", [0, 0, 299, 199], label1, 0.7, height, width),  # fp due to no gts
            self._create_prediction(task, "1", [0, 0, 149, 99], label1, 0.4, height, width),  # fp due to low iou
            # fp because prediction with higher score matched the same gt.
            self._create_prediction(task, "1", [0, 0, 299, 199], label1, 0.6, height, width),
            self._create_prediction(task, "1", [600, 400, 299, 199], label1, 0.9, height, width)  # matches "iscrowd"
        ]
        # Expected results corresponding to prediction categories sorted by score
        expected_recall_list = torch.tensor([0, 0.5, 0.5, 0.5, 1, 1], dtype=torch.float)
        expected_precision_list = torch.tensor([0, 1, 0.5, 1 / 3, 0.5, 0.4], dtype=torch.float)
        precision_list, recall_list = vocmap._precision_recall_curve(predictions, label1, task)
        assert torch.all(torch.eq(precision_list, expected_precision_list))
        assert torch.all(torch.eq(recall_list, expected_recall_list))

    @pytest.mark.usefixtures("new_clean_dir")
    @pytest.mark.parametrize("task", ["bbox", "segm"])
    def test_map_precision_recall(self, task):
        vocmap = self._setup_vocmap_object()
        height = 600
        width = 900

        # Mock vocmap._label_gts and vocmap._labels
        label1 = "label1"
        label2 = "label2"
        label3 = "label3"
        vocmap._labels.extend([label1, label2, label3])
        vocmap._label_gts[label1] = [
            self._create_annotation(task, "1", [0, 0, 299, 199], label1, False, height, width),
            self._create_annotation(task, "2", [0, 0, 299, 199], label1, False, height, width),
            self._create_annotation(task, "1", [600, 400, 299, 199], label1, True, height, width)
        ]
        # label 2 with only "iscrowd" gts.
        vocmap._label_gts[label2] = [
            self._create_annotation(task, "1", [0, 0, 299, 199], label2, True, height, width),
            self._create_annotation(task, "2", [0, 0, 299, 199], label2, True, height, width)
        ]
        # label 3 with no gts.
        vocmap._label_gts[label3] = []

        # No gts, no predictions
        label_score = vocmap._map_precision_recall([], label3, task)
        assert label_score[VocMap.PRECISION] == -1.0
        assert label_score[VocMap.RECALL] == -1.0
        assert label_score[VocMap.AVERAGE_PRECISION] == -1.0
        # No non crowd gts, no predictions
        label_score = vocmap._map_precision_recall([], label2, task)
        assert label_score[VocMap.PRECISION] == -1.0
        assert label_score[VocMap.RECALL] == -1.0
        assert label_score[VocMap.AVERAGE_PRECISION] == -1.0

        # No gts, some predictions
        predictions = [
            self._create_prediction(task, "1", [0, 0, 299, 199], label3, 0.5, height, width)
        ]
        label_score = vocmap._map_precision_recall(predictions, label3, task)
        assert label_score[VocMap.PRECISION] == 0.0
        assert label_score[VocMap.RECALL] == -1.0
        assert label_score[VocMap.AVERAGE_PRECISION] == -1.0
        # No non crowd gts, some predictions
        predictions = [
            self._create_prediction(task, "1", [0, 0, 299, 199], label2, 0.5, height, width)
        ]
        label_score = vocmap._map_precision_recall(predictions, label2, task)
        assert label_score[VocMap.PRECISION] == 0.0
        assert label_score[VocMap.RECALL] == -1.0
        assert label_score[VocMap.AVERAGE_PRECISION] == -1.0

        # Has Non crowd gts, no predictions
        label_score = vocmap._map_precision_recall([], label1, task)
        assert label_score[VocMap.PRECISION] == -1.0
        assert label_score[VocMap.RECALL] == 0.0
        assert label_score[VocMap.AVERAGE_PRECISION] == 0.0

        # Has non crowd gts, some predictions
        predictions = [
            self._create_prediction(task, "1", [0, 0, 299, 199], label1, 0.8, height, width),  # tp
            self._create_prediction(task, "2", [0, 0, 299, 199], label1, 0.5, height, width),  # tp
            self._create_prediction(task, "3", [0, 0, 299, 199], label1, 0.7, height, width),  # fp due to no gts
        ]
        label_score = vocmap._map_precision_recall(predictions, label1, task)
        assert label_score[VocMap.PRECISION].ndim == 0  # Scalar
        assert label_score[VocMap.PRECISION] != -1
        assert label_score[VocMap.RECALL].ndim == 0  # Scalar
        assert label_score[VocMap.RECALL] != -1
        assert label_score[VocMap.AVERAGE_PRECISION].ndim == 0  # Scalar
        assert label_score[VocMap.AVERAGE_PRECISION] != -1
