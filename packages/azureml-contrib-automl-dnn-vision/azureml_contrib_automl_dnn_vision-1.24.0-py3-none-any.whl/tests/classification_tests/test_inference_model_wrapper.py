import json
import os
import tempfile
from pathlib import Path

import pytest

from PIL import Image

from azureml.core.run import _OfflineRun
from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals
from azureml.contrib.automl.dnn.vision.common.utils import _get_default_device
from azureml.contrib.automl.dnn.vision.classification.common.transforms import _get_common_valid_transforms
from azureml.contrib.automl.dnn.vision.classification.inference import InferenceModelWrapper
from azureml.contrib.automl.dnn.vision.classification.inference.score import _featurize_with_model, _score_with_model
from azureml.contrib.automl.dnn.vision.classification.models import ModelFactory

from tests.common.run_mock import RunMock, ExperimentMock, WorkspaceMock, DatastoreMock, LabeledDatasetFactoryMock
from tests.common.utils import mock_prepare_model_export


@pytest.mark.usefixtures('new_clean_dir')
class TestInferenceModelWrapper:
    def test_inference_cpu(self, image_dir):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            model_wrapper = ModelFactory().get_model_wrapper('seresnext', 10)
            classes = ['A'] * 10
            inference_model_wrapper = InferenceModelWrapper(model_wrapper, labels=classes, device='cpu')
            # save the model wrapper
            mock_prepare_model_export(run=_OfflineRun, model_wrapper=inference_model_wrapper,
                                      model_weights=model_wrapper.get_state_dict(), output_dir=tmp_output_dir)

            model_wrapper_pkl = os.path.join(tmp_output_dir, ArtifactLiterals.MODEL_WRAPPER_PKL)
            inference_model = InferenceModelWrapper.load_serialized_inference_model_wrapper(model_wrapper_pkl)
            inference_model.to_device('cpu')

            image_path = os.path.join(image_dir, 'crack_1.jpg')
            im = Image.open(image_path)
            assert inference_model.labels == classes
            inference_model.predict([im])
            assert inference_model.predict_proba([im]).shape[1] == len(classes)
            assert inference_model.featurize([im]).shape[0] == 1

    def test_featurization(self, root_dir, image_dir, src_image_list_file_name):
        image_class_list_file_path = os.path.join(root_dir, src_image_list_file_name)
        batch_size_list = range(1, 3)
        self._featurization_test(root_dir, image_dir, image_class_list_file_path, batch_size_list, 4)

    @staticmethod
    def _write_image_list_to_file(image_dir, image_class_list_file_path):
        Path(image_class_list_file_path).touch()
        with open(image_class_list_file_path, mode="w") as fp:
            for image_file in os.listdir(image_dir):
                fp.write(image_file + "\n")

    def test_featurization_invalid_image_file(self, root_dir, image_dir, image_list_file_name):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            temp_image_class_list_file_path = os.path.join(tmp_output_dir, image_list_file_name)
            self._write_image_list_to_file(image_dir, temp_image_class_list_file_path)
            expected_feature_file_length = 4  # Should not include invalid image.
            self._featurization_test(root_dir, image_dir, temp_image_class_list_file_path, [3],
                                     expected_feature_file_length)
            self._featurization_test(root_dir, image_dir, temp_image_class_list_file_path, [1],
                                     expected_feature_file_length)

    @staticmethod
    def _featurization_test(root_dir, image_dir, image_class_list_file_path,
                            batch_size_list, expected_feature_file_length):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            model_wrapper = ModelFactory().get_model_wrapper('seresnext', 10)
            classes = ['A'] * 10

            device = _get_default_device()

            inference_model_wrapper = InferenceModelWrapper(model_wrapper, labels=classes, device=device)

            # run featurizations
            featurization_file = 'features.txt'
            features_output_file = os.path.join(tmp_output_dir, featurization_file)

            Path(features_output_file).touch()

            inference_model_wrapper.model_wrapper.transforms = _get_common_valid_transforms(
                resize_to=model_wrapper.resize_to_size,
                crop_size=model_wrapper.crop_size
            )

            for batch_size in batch_size_list:
                TestInferenceModelWrapper._featurization_batch_test(features_output_file, image_dir,
                                                                    image_class_list_file_path,
                                                                    inference_model_wrapper, batch_size,
                                                                    expected_feature_file_length)

    @staticmethod
    def _featurization_batch_test(features_output_file, image_dir,
                                  image_class_list_file_path, inference_model_wrapper, batch_size,
                                  expected_feature_file_length):

        datastore_name = "TestDatastoreName"
        datastore_mock = DatastoreMock(datastore_name)
        workspace_mock = WorkspaceMock(datastore_mock)
        experiment_mock = ExperimentMock(workspace_mock)
        run_mock = RunMock(experiment_mock)

        _featurize_with_model(inference_model_wrapper, run_mock, root_dir=image_dir,
                              output_file=features_output_file,
                              image_list_file=image_class_list_file_path,
                              device=_get_default_device(),
                              batch_size=batch_size, num_workers=0)

        with open(features_output_file) as fp:
            for line in fp:
                obj = json.loads(line.strip())
                assert 'filename' in obj
                assert 'feature_vector' in obj
                assert len(obj['feature_vector']) > 0
        with open(features_output_file) as fp:
            lines = fp.readlines()
        assert len(lines) == expected_feature_file_length

    def test_score(self, root_dir, image_dir, src_image_list_file_name):
        image_class_list_file_path = os.path.join(root_dir, src_image_list_file_name)
        self._score_test(root_dir, image_dir, image_class_list_file_path, 4, 10)

    def test_score_invalid_image_file(self, root_dir, image_dir, image_list_file_name):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            temp_image_class_list_file_path = os.path.join(tmp_output_dir, image_list_file_name)
            self._write_image_list_to_file(image_dir, temp_image_class_list_file_path)
            expected_score_file_length = 4  # Should not include invalid image.
            self._score_test(root_dir, image_dir, temp_image_class_list_file_path,
                             expected_score_file_length, 10)
            self._score_test(root_dir, image_dir, temp_image_class_list_file_path,
                             expected_score_file_length, 1)

    @staticmethod
    def _score_test(root_dir, image_dir, image_class_list_file_path, expected_score_file_length, batch_size):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            model_wrapper = ModelFactory().get_model_wrapper('seresnext', 10)
            classes = ['A'] * 10

            device = _get_default_device()

            inference_model_wrapper = InferenceModelWrapper(model_wrapper, labels=classes, device=device)

            # run predictions
            predictions_file = 'predictions.txt'
            predictions_output_file = os.path.join(tmp_output_dir, predictions_file)

            datastore_name = "TestDatastoreName"
            datastore_mock = DatastoreMock(datastore_name)
            workspace_mock = WorkspaceMock(datastore_mock)
            experiment_mock = ExperimentMock(workspace_mock)
            run_mock = RunMock(experiment_mock)
            test_dataset_id = 'a2458938-7966-4ca0-b4ba-a97d89d4eb2b'
            labeled_dataset_factory_mock = LabeledDatasetFactoryMock(test_dataset_id)
            test_target_path = "TestTargetPath"
            labeled_dataset_file = os.path.join(tmp_output_dir, 'labeled_dataset.json')

            Path(predictions_output_file).touch()
            Path(labeled_dataset_file).touch()

            inference_model_wrapper.model_wrapper.transforms = _get_common_valid_transforms(
                resize_to=model_wrapper.resize_to_size,
                crop_size=model_wrapper.crop_size
            )

            _score_with_model(inference_model_wrapper, run_mock, test_target_path,
                              root_dir=image_dir,
                              output_file=predictions_output_file,
                              image_list_file=image_class_list_file_path,
                              device=device,
                              labeled_dataset_factory=labeled_dataset_factory_mock,
                              always_create_dataset=True,
                              num_workers=0,
                              labeled_dataset_file=labeled_dataset_file,
                              batch_size=batch_size)

            with open(predictions_output_file) as fp:
                for line in fp:
                    obj = json.loads(line.strip())
                    assert 'filename' in obj
                    assert 'probs' in obj
                    assert len(obj['probs']) > 0
            with open(predictions_output_file) as fp:
                lines = fp.readlines()
            assert len(lines) == expected_score_file_length

            assert labeled_dataset_factory_mock.task == "ImageClassification"
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
