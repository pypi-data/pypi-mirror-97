import os
import pytest
import tempfile
import pandas as pd

from azureml.contrib.automl.dnn.vision.common.prediction_dataset import PredictionDataset
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException
from .aml_dataset_mock import AmlDatasetMock, WorkspaceMock, DataflowMock, DataflowStreamMock


@pytest.mark.usefixtures('new_clean_dir')
class TestPredictionDataset:

    @staticmethod
    def _create_image_list_file(tmp_output_dir, lines):
        image_file = 'image_list_file.txt'
        image_list_file = os.path.join(tmp_output_dir, image_file)
        with open(image_list_file, 'w') as f:
            for line in lines:
                f.write(line + '\n')
        return image_list_file

    def test_prediction_dataset(self):
        test_dataset_id = 'e7c014ec-474a-49f4-8ae3-09049c701913'
        test_file0 = 'e7c014ec-474a-49f4-8ae3-09049c701913-1.txt'
        test_file1 = 'e7c014ec-474a-49f4-8ae3-09049c701913-2.txt'
        test_files = [test_file0, test_file1]
        test_files_full_path = [os.path.join(AmlLabeledDatasetHelper.get_data_dir(),
                                             test_file) for test_file in test_files]
        properties = {}
        label_dataset_data = {
            'Path': ['/' + f for f in test_files]
        }
        dataframe = pd.DataFrame(label_dataset_data)

        mockdataflowstream = DataflowStreamMock(test_files_full_path)
        mockdataflow = DataflowMock(dataframe, mockdataflowstream, 'Path')
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        mockworkspace = WorkspaceMock(mockdataset)

        try:
            datasetwrapper = PredictionDataset(input_dataset_id=test_dataset_id, ws=mockworkspace,
                                               datasetclass=AmlDatasetMock)

            file_names = datasetwrapper._files
            file_names.sort()
            assert file_names == test_files, "File Names"
            assert len(datasetwrapper) == len(test_files), "len"

            for test_file in test_files_full_path:
                assert os.path.exists(test_file)

        finally:
            for test_file in test_files_full_path:
                os.remove(test_file)

    def test_prediction_dataset_with_image_file(self):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            file_content = ['test.txt', ' whitespace.txt ']
            image_list_file = self._create_image_list_file(tmp_output_dir, file_content)

            pred_dataset = PredictionDataset(image_list_file=image_list_file)

            filenames = pred_dataset._files
            filenames.sort()
            assert filenames == ['test.txt', 'whitespace.txt']

    def test_prediction_dataset_with_labeled_image_file(self):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            file_content = ['test.txt testlabel', ' whitespace.txt testlabel ']
            image_list_file = self._create_image_list_file(tmp_output_dir, file_content)

            pred_dataset = PredictionDataset(image_list_file=image_list_file)

            filenames = pred_dataset._files
            filenames.sort()
            assert filenames == ['test.txt', 'whitespace.txt']

    def test_prediction_dataset_with_invalid_row(self):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            file_content = ['test.txt', ' ']
            image_list_file = self._create_image_list_file(tmp_output_dir, file_content)

            pred_dataset = PredictionDataset(image_list_file=image_list_file)
            assert pred_dataset._files == ['test.txt']

    def test_prediction_dataset_invalid_without_ignore(self):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            file_content = ['test.txt', ' ']
            image_list_file = self._create_image_list_file(tmp_output_dir, file_content)
            with pytest.raises(AutoMLVisionDataException):
                PredictionDataset(image_list_file=image_list_file, ignore_data_errors=False)

    def test_prediction_dataset_with_json_file(self):
        with tempfile.TemporaryDirectory() as tmp_output_dir:
            file_content = ['{"imageUrl": "test.png", "imageDetails": {}}',
                            '{"imageUrl": " ws.png ", "imageDetails": {}}']
            image_list_file = self._create_image_list_file(tmp_output_dir, file_content)

            pred_dataset = PredictionDataset(image_list_file=image_list_file)
            assert pred_dataset._files == ['test.png', 'ws.png']
