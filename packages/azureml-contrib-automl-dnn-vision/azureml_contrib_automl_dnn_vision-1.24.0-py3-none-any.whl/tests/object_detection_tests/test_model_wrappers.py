import json
import os
import pytest
import tempfile
import torch
import torchvision.transforms.functional as functional

from azureml.contrib.automl.dnn.vision.common.constants import SettingsLiterals
from azureml.contrib.automl.dnn.vision.object_detection.common.boundingbox import BoundingBox
from azureml.contrib.automl.dnn.vision.object_detection.common.constants import training_settings_defaults
from azureml.contrib.automl.dnn.vision.object_detection.writers.score import _score_with_model
from azureml.contrib.automl.dnn.vision.object_detection.models.object_detection_model_wrappers \
    import FasterRCNNResnet50FPNWrapper
from azureml.contrib.automl.dnn.vision.object_detection.models.instance_segmentation_model_wrappers \
    import MaskRCNNResnet50FPNWrapper
from pathlib import Path
from PIL import Image

from .utils import CocoBaseModelWrapper
from ..common.run_mock import RunMock, ExperimentMock, WorkspaceMock, DatastoreMock, LabeledDatasetFactoryMock
from ..common.utils import check_exported_onnx_od_model


@pytest.mark.usefixtures('new_clean_dir')
class TestModelWrappers:
    def test_inference_base_model_wrapper(self, data_root):
        model_wrapper = CocoBaseModelWrapper()
        # TODO: Both of the following lines should be removed once this moves to initialization
        model_wrapper.classes = ['A'] * 91
        model_wrapper.to_device('cpu')
        im = Image.open(os.path.join(data_root, 'coco_classes_image.jpg'))
        bounding_boxes = model_wrapper.predict([im, im])
        assert len(bounding_boxes) == 2

        for box in bounding_boxes[0]:
            assert isinstance(box, BoundingBox)
            assert box.label == 'A'

    def test_wrappers_export_onnx(self, data_root):
        # right now only initialization and making sure that the model is working
        device = training_settings_defaults[SettingsLiterals.DEVICE]
        image = Image.open(os.path.join(data_root, 'coco_classes_image.jpg')).convert('RGB')
        image_tensor = functional.to_tensor(image).unsqueeze(0).to(device=device)
        resized_image = torch.nn.functional.interpolate(image_tensor, size=(600, 800),
                                                        mode='bilinear', align_corners=False)

        def get_model_output(wrapper, input, device):
            wrapper.to_device(device=device)
            wrapper.model.eval()
            return wrapper.model(input)

        # Inference with onnx model fails in torch 1.7.1 as box_score_thresh is interpreted as float64 and
        # float64 is not supported in one of the nodes(Greater). Explicitly passing it here so that
        # FasterRCNNResnet50FPNWrapper takes care of converting it to float tensor to solve the issue.
        r50 = FasterRCNNResnet50FPNWrapper(box_score_thresh=0.05)
        r50_file = 'FasterRCNNResnet50FPNWrapper.onnx'
        r50.export_onnx_model(file_path=r50_file, device=device)
        check_exported_onnx_od_model(r50_file, r50, resized_image, device, get_model_output)

        # export onnx w/ normalization
        r50n_file = 'FasterRCNNResnet50FPNWrapperNorm.onnx'
        r50.export_onnx_model(file_path=r50n_file, device=device, enable_norm=True)
        check_exported_onnx_od_model(r50n_file, r50, resized_image, device, get_model_output, is_norm=True)

        m50 = MaskRCNNResnet50FPNWrapper(box_score_thresh=0.05)
        m50_file = 'MaskRCNNResnet50FPNWrapper.onnx'
        m50.export_onnx_model(file_path=m50_file, device=device)
        check_exported_onnx_od_model(m50_file, m50, resized_image, device, get_model_output)

        # TODO: also test exported model for FasterRCNNResnet18FPNWrapper, FasterRCNNMobilenetV2Wrapper
        # Currently, export_onnx_model fails for them with "size mismatch" problem

    def test_score(self, data_root, image_list_file_name):
        image_dir = os.path.join(data_root, 'images')
        image_od_list_file_path = os.path.join(data_root, image_list_file_name)
        with open(image_od_list_file_path) as fp:
            expected_score_file_length = len(fp.readlines())
        # batch_size 1
        self._scoring_test(image_dir, image_od_list_file_path, 1, expected_score_file_length)
        # batch_size 2
        self._scoring_test(image_dir, image_od_list_file_path, 2, expected_score_file_length)

    def test_score_invalid_image_file(self, data_root, image_list_file_name):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            image_dir = os.path.join(data_root, 'images')
            temp_image_od_list_file_path = os.path.join(tmp_output_dir, image_list_file_name)
            # copy list from src_image_od_list_file.txt and add one extra file.
            image_od_list_file_path = os.path.join(data_root, image_list_file_name)
            with open(image_od_list_file_path) as input_fp:
                lines = input_fp.readlines()
                with open(temp_image_od_list_file_path, 'w') as fp:
                    fp.writelines(lines)
                    fp.write("\n")
                    fp.write("invalid_image_file.jpg" + "\n")

            with open(temp_image_od_list_file_path) as fp:
                expected_score_file_length = len(fp.readlines()) - 1  # One invalid image file in the images folder.

            self._scoring_test(image_dir, temp_image_od_list_file_path, 1, expected_score_file_length)
            self._scoring_test(image_dir, temp_image_od_list_file_path, 3, expected_score_file_length)

    @staticmethod
    def _scoring_test(image_dir, image_od_list_file_path, batch_size, expected_score_file_length):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            model_wrapper = CocoBaseModelWrapper()
            # TODO: Both of the following lines should be removed once this moves to initialization
            model_wrapper.classes = ['A'] * 91
            model_wrapper.to_device('cpu')

            # run predictions
            predictions_file = 'predictions_od.txt'
            predictions_output_file = os.path.join(tmp_output_dir, predictions_file)

            datastore_name = "TestDatastoreName"
            datastore_mock = DatastoreMock(datastore_name)
            workspace_mock = WorkspaceMock(datastore_mock)
            experiment_mock = ExperimentMock(workspace_mock)
            run_mock = RunMock(experiment_mock)
            test_dataset_id = 'b2458938-7966-4ca0-b4ba-a97d89d4eb2b'
            labeled_dataset_factory_mock = LabeledDatasetFactoryMock(test_dataset_id)
            test_target_path = "TestTargetPath"
            labeled_dataset_file = os.path.join(tmp_output_dir, "labeled_dataset.json")

            Path(predictions_output_file).touch()
            Path(labeled_dataset_file).touch()

            _score_with_model(model_wrapper, run_mock, test_target_path,
                              root_dir=image_dir, output_file=predictions_output_file,
                              image_list_file=image_od_list_file_path,
                              device='cpu', batch_size=batch_size,
                              labeled_dataset_factory=labeled_dataset_factory_mock,
                              always_create_dataset=True,
                              num_workers=0,
                              labeled_dataset_file=labeled_dataset_file)

            with open(predictions_output_file) as fp:
                for line in fp:
                    obj = json.loads(line.strip())
                    assert 'filename' in obj
                    assert 'boxes' in obj
                    assert len(obj['boxes']) > 0
                    assert 'box' in obj['boxes'][0]
                    assert 'label' in obj['boxes'][0]
                    assert 'score' in obj['boxes'][0]
            with open(predictions_output_file) as fp:
                lines = fp.readlines()
            assert len(lines) == expected_score_file_length

            assert labeled_dataset_factory_mock.task == 'ObjectDetection'
            expected_path = test_target_path + "/labeled_dataset.json"
            assert labeled_dataset_factory_mock.path == expected_path

            assert len(datastore_mock.files) == 1

            (files, root_dir, target_path, overwrite) = datastore_mock.files[0]
            assert len(files) == 1
            assert root_dir == tmp_output_dir
            assert target_path == test_target_path
            assert overwrite

            assert len(datastore_mock.dataset_file_content) == expected_score_file_length

            for line in datastore_mock.dataset_file_content:
                line_contents = json.loads(line)
                assert line_contents['image_url'].startswith('AmlDatastore://')
                assert 'label' in line_contents
                assert 'label_confidence' in line_contents

            assert run_mock.properties['labeled_dataset_id'] == test_dataset_id
