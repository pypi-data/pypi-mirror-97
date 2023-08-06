# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Tests for model export utils methods."""
import os
import json
import pytest
import tempfile
import unittest.mock as mock

from azureml.train.automl import constants
from azureml.automl.core.inference import inference

import azureml.automl.core.shared.constants as shared_constants

from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals
import azureml.contrib.automl.dnn.vision.common.model_export_utils as model_utils

from tests.common.run_mock import RunMock, ExperimentMock, WorkspaceMock, DatastoreMock


class TestModelExportUtils:

    @staticmethod
    def _setup_mock_run():
        ds_mock = DatastoreMock("test_dataset_name")
        ws_mock = WorkspaceMock(ds_mock)
        exp_mock = ExperimentMock(ws_mock)
        return RunMock(exp_mock)

    @mock.patch(model_utils.__name__ + '.AzureAutoMLRunContext._get_artifact_id')
    @mock.patch(model_utils.__name__ + '.AzureAutoMLRunContext.batch_save_artifacts')
    @mock.patch(model_utils.__name__ + '._get_scoring_file')
    @mock.patch(model_utils.__name__ + '._create_conda_env_file_content')
    def test_prepare_model_export(self, mock_conda_env_file, mock_get_scoring,
                                  mock_batch_save, mock_get_artifacts):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            run_mock = self._setup_mock_run()
            score_file_path = os.path.join('test_artifacts', shared_constants.SCORING_FILE_PATH)
            conda_file_path = os.path.join('test_artifacts', shared_constants.SCORING_FILE_PATH)
            model_path = os.path.join('test_artifacts', ArtifactLiterals.MODEL_FILE_NAME)

            # set up mocked methods' return values
            mock_conda_env_file.return_value = "test_conda_env"
            mock_get_scoring.return_value = "test_score_content"
            mock_get_artifacts.side_effect = [score_file_path, conda_file_path, model_path]

            # call method
            model_utils.prepare_model_export(run_mock, model_wrapper={},
                                             model_weights={},
                                             output_dir=tmp_output_dir,
                                             task_type=constants.Tasks.IMAGE_OBJECT_DETECTION)

            # Assert methods called
            mock_conda_env_file.assert_called_once_with(run_mock)
            mock_get_scoring.assert_called_once_with(task_type=constants.Tasks.IMAGE_OBJECT_DETECTION,
                                                     model_settings={},
                                                     is_yolo=False)
            mock_batch_save.assert_called_once()
            mock_get_artifacts.assert_called()

            # Assert properties added to run
            expected_properties = {
                inference.AutoMLInferenceArtifactIDs.ScoringDataLocation: score_file_path,
                inference.AutoMLInferenceArtifactIDs.CondaEnvDataLocation: conda_file_path,
                inference.AutoMLInferenceArtifactIDs.ModelDataLocation: 'test_artifacts'
            }
            assert run_mock.properties == expected_properties

    def test_create_conda_env_file_content(self):
        run_mock = self._setup_mock_run()
        conda_file_content = model_utils._create_conda_env_file_content(run_mock)
        for package in inference.AutoMLVisionCondaPackagesList:
            assert package in conda_file_content

    @pytest.mark.parametrize('is_yolo', [True, False])
    @pytest.mark.parametrize('task_type', constants.Tasks.ALL_IMAGE)
    def test_get_scoring_file_od(self, is_yolo, task_type):
        model_settings = {'test_settings': 'test_val'}

        score_file_content = model_utils._get_scoring_file(task_type, model_settings, is_yolo)
        assert task_type in score_file_content
        assert json.dumps(model_settings) in score_file_content

        if task_type in constants.Tasks.ALL_IMAGE_CLASSIFICATION:
            assert 'classification.inference' in score_file_content
        elif is_yolo:
            assert 'object_detection_yolo.writers' in score_file_content
        else:
            assert 'object_detection.writers' in score_file_content

    @mock.patch(model_utils.__name__ + '.InferenceModelWrapper.load_serialized_inference_model_wrapper')
    @mock.patch(model_utils.__name__ + '._load_model_wrapper')
    @pytest.mark.parametrize('task_type', constants.Tasks.ALL_IMAGE)
    def test_load_model(self, mock_load_wrapper, mock_load_inference_wrapper, task_type):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            model_settings = {'test_settings': 'test_val'}

            mock_load_inference_wrapper.return_value = 'inference_model_wrapper'
            mock_load_wrapper.return_value = 'object_detection_model_wrapper'

            load_output = model_utils.load_model(task_type, tmp_output_dir, **model_settings)

            pkl_path = os.path.join(tmp_output_dir, ArtifactLiterals.MODEL_WRAPPER_PKL)

            if task_type in constants.Tasks.ALL_IMAGE_CLASSIFICATION:
                mock_load_inference_wrapper.assert_called_once_with(pkl_path)
                mock_load_wrapper.assert_not_called()
                assert load_output == 'inference_model_wrapper'
            else:
                mock_load_wrapper.assert_called_once()
                mock_load_inference_wrapper.assert_not_called()
                assert load_output == 'object_detection_model_wrapper'
