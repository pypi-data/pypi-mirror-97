# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Dataset for prediction."""

import json
import os
from torch.utils.data import Dataset
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.utils import _read_image
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.object_detection.common.constants import DatasetFieldLabels
from azureml.core import Dataset as AmlDataset

from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException

logger = get_logger(__name__)


class PredictionDataset(Dataset):
    """Dataset file so that score.py can process images in batches.

    """
    def __init__(self, root_dir=None, image_list_file=None, transforms=None, ignore_data_errors=True,
                 input_dataset_id=None, ws=None, datasetclass=AmlDataset):
        """
        :param root_dir: prefix to be added to the paths contained in image_list_file
        :type root_dir: str
        :param image_list_file: path to file containing list of images
        :type image_list_file: str
        :param transforms: function that takes in a pillow image and can generate tensor
        :type transforms: function
        :param ignore_data_errors: boolean flag on whether to ignore input data errors
        :type ignore_data_errors: bool
        :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
        :type input_dataset_id: str
        :param ws: The Azure ML Workspace
        :type ws: Workspace
        :param datasetclass: The Azure ML Datset class
        :type datasetclass: Dataset

        """
        self._files = []

        if input_dataset_id is not None:
            dataset_helper = AmlLabeledDatasetHelper(input_dataset_id, ws, ignore_data_errors,
                                                     image_column_name=AmlLabeledDatasetHelper.PATH_COLUMN_NAME,
                                                     datasetclass=datasetclass)
            self._files = dataset_helper.get_file_name_list()
            self._files = [f.strip("/") for f in self._files]
            self._root_dir = dataset_helper._data_dir
        else:
            self._files = self._get_files_from_image_list_file(image_list_file, ignore_data_errors)

            # Size of image list file before removing blank strings
            logger.info('Image list file contains {} lines before removing blank '
                        'strings'.format(len(self._files)))

            # Remove blank strings
            self._files = [f for f in self._files if f]
            self._root_dir = root_dir

        # Length of final dataset
        logger.info('Size of dataset: {}'.format(len(self._files)))
        self._transform = transforms
        self._ignore_data_errors = ignore_data_errors

    def __len__(self):
        """Size of the dataset."""
        return len(self._files)

    @staticmethod
    def collate_function(batch):
        """Collate function for the dataset"""
        return tuple(zip(*batch))

    def __getitem__(self, idx):
        """
        :param idx: index
        :type idx: int
        :return: item and label at index idx
        :rtype: tuple[str, image]
        """
        filename, full_path = self.get_image_full_path(idx)

        image = _read_image(self._ignore_data_errors, full_path)
        if image is not None:
            if self._transform:
                image = self._transform(image)

        return filename, image

    def get_image_full_path(self, idx):
        """Returns the filename and full file path for the given index.

        :param idx: index of the file to return
        :type idx: int
        :return: a tuple filename, full file path
        :rtype: tuple
        """
        filename = self._files[idx]
        if self._root_dir and filename:
            filename = filename.lstrip('/')
        full_path = os.path.join(self._root_dir, filename)
        return filename, full_path

    def _get_files_from_image_list_file(self, image_list_file, ignore_data_errors=True):
        files = []
        with open(image_list_file) as fp:
            lines = fp.readlines()
            parse_as_json_file = True
            if len(lines) > 0:
                try:
                    json.loads(lines[0])
                    logger.info("Parsing image list file as a JSON file")
                except json.JSONDecodeError:
                    parse_as_json_file = False

            if parse_as_json_file:
                files = self._parse_image_file_as_json(lines, ignore_data_errors)
            else:
                for row in lines:
                    file_data = row.split()
                    if not file_data:
                        if not ignore_data_errors:
                            raise AutoMLVisionDataException('Input image file contains empty row', has_pii=False)
                        continue
                    files.append(file_data[0])

        return files

    def _parse_image_file_as_json(self, lines, ignore_data_errors):
        files = []
        for row in lines:
            try:
                annotation = json.loads(row)
                if DatasetFieldLabels.IMAGE_URL not in annotation:
                    missing_required_fields_message = "Missing required fields in annotation"
                    if not ignore_data_errors:
                        raise AutoMLVisionDataException(missing_required_fields_message, has_pii=False)
                    continue
                filename = annotation[DatasetFieldLabels.IMAGE_URL]
                files.append(filename.strip())
            except json.JSONDecodeError:
                if not ignore_data_errors:
                    raise AutoMLVisionDataException("Invalid JSON object detected in file", has_pii=False)
                continue
        return files
