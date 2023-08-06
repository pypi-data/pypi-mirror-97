import os
import tempfile
import pytest
import sys

from azureml.train.automl import constants
from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals

import azureml.contrib.automl.dnn.vision.classification.runner as runner
import azureml.contrib.automl.dnn.vision.classification.io.write.modelsaver as modelsaver
from azureml.contrib.automl.dnn.vision.classification.models import ModelFactory
from azureml.contrib.automl.dnn.vision.classification.inference.inference_model_wrapper import InferenceModelWrapper

from tests.common.run_mock import RunMock, ExperimentMock, WorkspaceMock, DatastoreMock
from tests.common.utils import mock_prepare_model_export


data_folder = 'classification_data/images'
labels_root = 'classification_data/'


def _get_settings(csv_file):
    return {
        'data_folder': data_folder,
        'deterministic': True,
        'images_folder': '.',
        'labels_file': csv_file,
        'labels_file_root': labels_root,
        'log_verbose_metrics': True,
        'num_workers': 0,
        'output_scoring': True,
        'print_local_package_versions': True,
        'seed': 47,
        'validation_labels_file': 'valid_labels.csv'
    }


@pytest.mark.usefixtures('new_clean_dir')
def test_score_validation_data(monkeypatch):
    def mock_score(inference_model_wrapper, run, target_path, device,
                   output_file, root_dir, image_list_file,
                   batch_size, ignore_data_errors, input_dataset_id,
                   num_workers, log_output_file_info):
        assert target_path.startswith('automl/datasets/')
        assert batch_size == 20
        assert input_dataset_id == val_dataset_id
        assert num_workers == 8
        assert device == 'cpu'
        assert log_output_file_info

        data_folder = os.path.join(tmp_output_dir, 'cracks')
        expected_root_dir = os.path.join(data_folder, '.')
        assert root_dir == expected_root_dir

        with open(image_list_file, 'w') as f:
            f.write('testcontent')

    with tempfile.TemporaryDirectory() as tmp_output_dir:
        ds_mock = DatastoreMock('datastore_mock')
        ws_mock = WorkspaceMock(ds_mock)
        experiment_mock = ExperimentMock(ws_mock)
        run_mock = RunMock(experiment_mock)

        model_wrapper = ModelFactory().get_model_wrapper('seresnext', 10)
        classes = ['A'] * 10
        test_inference_model_wrapper = InferenceModelWrapper(model_wrapper, labels=classes, device='cpu')
        val_dataset_id = '123'
        image_folder = '.'
        settings = {
            'validation_batch_size': 20,
            'batch_size': 40,
            'validation_labels_file': 'test.csv',
            'labels_file_root': tmp_output_dir,
            'data_folder': os.path.join(tmp_output_dir, 'cracks'),
            'num_workers': 8,
            'log_scoring_file_info': True
        }

        with monkeypatch.context() as m:
            m.setattr(runner, '_score_with_model', mock_score)
            runner.score_validation_data(inference_model_wrapper=test_inference_model_wrapper,
                                         azureml_run=run_mock, ignore_data_errors=True,
                                         val_dataset_id=val_dataset_id,
                                         image_folder=image_folder,
                                         device='cpu',
                                         settings=settings)
            expected_val_labels_file = os.path.join(tmp_output_dir, 'test.csv')
            assert os.path.exists(expected_val_labels_file)


@pytest.mark.usefixtures('new_clean_dir')
def test_binary_classification_local_run(monkeypatch):
    _test_classification_local_run(monkeypatch, 'binary_classification.csv')


@pytest.mark.usefixtures('new_clean_dir')
def test_multiclassification_local_run(monkeypatch):
    _test_classification_local_run(monkeypatch, 'multiclass.csv')


@pytest.mark.usefixtures('new_clean_dir')
def test_multilabel_local_run(monkeypatch):
    _test_classification_local_run(monkeypatch, 'multilabel.csv')


@pytest.mark.usefixtures('new_clean_dir')
def test_classification_local_run_invalid_images(monkeypatch):
    csv_file = 'multiclass_invalid_image.csv'
    settings = _get_settings(csv_file)
    settings.update({
        "validation_labels_file": 'valid_labels_invalid_image.csv',
        "batch_size": 1,
        "validation_batch_size": 1
    })
    _test_classification_local_run(monkeypatch, 'multiclass_invalid_image.csv', settings)


def _test_classification_local_run(monkeypatch, csv_file, settings=None):
    if settings is None:
        settings = _get_settings(csv_file)

    def mock_score_validation_data(inference_model_wrapper, azureml_run, ignore_data_errors,
                                   val_dataset_id, image_folder, device, settings):
        # Ensures score_validation_data is called
        test_output_dir = settings['output_dir']
        predictions_file = os.path.join(test_output_dir, 'predictions.txt')
        with open(predictions_file, 'w') as f:
            f.write('test content')

    with monkeypatch.context() as m:
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            m.setattr(sys, 'argv', ['runner.py', '--data-folder', data_folder, '--labels-file-root', labels_root])
            m.setattr(runner, 'score_validation_data', mock_score_validation_data)
            m.setattr(modelsaver, 'prepare_model_export', mock_prepare_model_export)

            settings['output_dir'] = tmp_output_dir
            settings['task_type'] = constants.Tasks.IMAGE_MULTI_LABEL_CLASSIFICATION
            settings['validation_output_file'] = os.path.join(tmp_output_dir, 'predictions.txt')

            runner.run(settings, multilabel=True)

            expected_output = os.path.join(tmp_output_dir, ArtifactLiterals.MODEL_WRAPPER_PKL)
            expected_validation_output = os.path.join(tmp_output_dir, 'predictions.txt')

            assert os.path.exists(expected_output)
            assert os.path.exists(expected_validation_output)
