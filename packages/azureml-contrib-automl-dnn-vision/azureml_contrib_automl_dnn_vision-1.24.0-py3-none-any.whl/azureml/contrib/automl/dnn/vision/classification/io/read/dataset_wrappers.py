# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines dataset wrapper class. To add a new dataset, implement the BaseDatasetWrapper interface."""

from abc import ABC, abstractmethod
import csv
import itertools
import os

from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.utils import _read_image, _pad
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from sklearn.model_selection import train_test_split

try:
    from torch.utils.data import Dataset
    from torchvision.datasets import ImageFolder
except ImportError:
    print('ImportError: torch not installed. If on windows, install torch, pretrainedmodels, torchvision and '
          'pytorch-ignite separately before running the package.')
from azureml.core import Dataset as AmlDataset
from azureml.automl.core.shared import logging_utilities

from azureml.contrib.automl.dnn.vision.common.exceptions import AutoMLVisionDataException
from azureml.contrib.automl.dnn.vision.common.aml_dataset_base_wrapper import AmlDatasetBaseWrapper


logger = get_logger(__name__)


class BaseDatasetWrapper(ABC, Dataset):
    """A wrapper class that provides exposes string labels and number of classes for a torch.utils.Dataset.

    Inheriting classes should call the base constructor.
    """

    def __init__(self, labels=None, multilabel=False):
        """Constructor

        :param labels: list of labels
        :type labels: typing.List[str]
        """
        self.reset_labels(labels)
        self.__multilabel = multilabel

    @abstractmethod
    def __len__(self):
        """
        :return: number of items in dataset
        :rtype: int
        """
        pass

    @abstractmethod
    def pad(self, padding_factor):
        """Pad the dataset so that its length can be evenly divided by padding_factor

        :param padding_factor: padding factor
        :type padding_factor: int
        """
        pass

    @abstractmethod
    def item_at_index(self, index):
        """Return image at index.

        :param index: index
        :type index: int
        :return: pillow image object
        :rtype: Image
        """
        pass

    @abstractmethod
    def label_at_index(self, index):
        """Return label at index.

        :param index: index
        :type index: int
        :return: string label or list of string labels if multilabel
        :rtype: typing.Union[str, typing.List[str]]
        """
        pass

    def __getitem__(self, index):
        """Get item at index from the dataset.

        :param index: index in the dataset
        :type index: int
        :return: Tuple (tensor, label) where label is an int or list of ints for multilabel
        :rtype: tuple[torch.Tensor, typing.Union[int, typing.List[int]]]
        """
        integer_labels = None
        if self.__multilabel:
            integer_labels = [self.label_to_index_map[i] for i in self.label_at_index(index)]
        else:
            integer_labels = self.label_to_index_map[self.label_at_index(index)]
        return (self.item_at_index(index), integer_labels)

    @property
    def index_to_label(self):
        """List of labels."""
        return self.__labels

    @property
    def label_to_index_map(self):
        """Dictionary from string labels to integers."""
        return self.__labels_to_num

    @property
    def labels(self):
        """Return list of string labels."""
        return self.__labels

    @property
    def multilabel(self):
        """Boolean flag indicating whether this is a multilabel dataset."""
        return self.__multilabel

    @property
    def num_classes(self):
        """
        :return: number of classes
        :rtype: int
        """
        return len(self.__labels_to_num)

    def reset_labels(self, labels):
        """
        :param labels: list of labels
        :type labels: typing.List[str]
        """
        sorted_labels = sorted(labels, reverse=False)
        self.__labels_to_num = dict([(label_name, i) for i, label_name in enumerate(sorted_labels)])
        self.__labels = sorted_labels


class _CommonImageDatasetWrapper(BaseDatasetWrapper):
    """Utility class for getting the DatasetWrapper class once the image files, labels and whether this is multilabel
    dataset are known.

    """

    def __init__(self, files_to_labels_dict=None, all_labels=None, multilabel=False, ignore_data_errors=True):
        """
        :param files_to_labels_dict: dictionary of file names to labels
        :type files_to_labels_dict: dict
        :param all_labels: list of all labels if there are more labels than those that are in files_to_labels_dict
        :type all_labels: typing.List[str]
        :param multilabel: boolean flag on whether this is multilabel task
        :type multilabel: bool
        :param ignore_data_errors: boolean flag on whether to ignore input data errors
        :type ignore_data_errors: bool
        """
        files_to_labels_dict = self._validate_and_fix_inputs(files_to_labels_dict,
                                                             ignore_data_errors=ignore_data_errors)
        self.__files_to_labels_dict = files_to_labels_dict
        self.__files = list(files_to_labels_dict.keys())
        uniq_labels = all_labels if all_labels is not None else self.__get_uniq_labels(files_to_labels_dict)

        self._ignore_data_errors = ignore_data_errors

        super().__init__(labels=list(uniq_labels), multilabel=multilabel)

    def __len__(self):
        return len(self.__files)

    def pad(self, padding_factor):
        """Pad the dataset so that its length can be evenly divided by padding_factor

        :param padding_factor: padding factor
        :type padding_factor: int
        """
        self.__files = _pad(self.__files, padding_factor)

    def _validate_and_fix_inputs(self, files_to_labels_dict=None, ignore_data_errors=True):
        """
        :param files_to_labels_dict: dictionary of file paths to labels
        :type files_to_labels_dict: typing.Dict[str, str]
        :param ignore_data_errors: boolean flag on whether to ignore input data errors
        :type ignore_data_errors: bool
        :return: dictionary of file paths to labels with only file paths that exist on disk
        :rtype: typing.Dict[str, str]
        """
        missing_files = []
        for file_path in files_to_labels_dict.keys():
            if not os.path.exists(file_path):
                mesg = 'File not found.'
                if ignore_data_errors:
                    missing_files.append(file_path)
                    extra_mesg = 'Since ignore_data_errors is True, file will be ignored'
                    logger.warning(mesg + extra_mesg)
                else:
                    raise AutoMLVisionDataException(mesg, has_pii=False)

        for file_path in missing_files:
            del files_to_labels_dict[file_path]

        if not files_to_labels_dict:
            raise AutoMLVisionDataException("No valid datapoints found to initialize dataset.",
                                            has_pii=False)

        return files_to_labels_dict

    def __get_uniq_labels(self, files_to_labels_dict):
        if isinstance(next(iter(files_to_labels_dict.values())), list):
            return list(set(list(itertools.chain.from_iterable(files_to_labels_dict.values()))))
        else:
            return list(set(files_to_labels_dict.values()))

    def item_at_index(self, index):
        filename = self.__files[index]
        image = _read_image(self._ignore_data_errors, filename)

        return image

    def label_at_index(self, index):
        filename = self.__files[index]
        return self.__files_to_labels_dict[filename]


class ImageFolderDatasetWrapper(_CommonImageDatasetWrapper):
    """DatasetWrapper for image folders.

    """

    def __init__(self, root_dir=None, all_labels=None):
        """
        :param root_dir: Root directory below which there are subdirectories per label.
        :type root_dir: str
        :param all_labels: list of all labels provided if the list of labels is different from those in input_file
        :type all_labels: typing.List[str]
        """
        _, labels = self._generate_labels_files_from_imagefolder(root_dir)
        super().__init__(files_to_labels_dict=labels, all_labels=all_labels)

    def _generate_labels_files_from_imagefolder(self, root_dir):
        folder = ImageFolder(root_dir, loader=lambda x: x)
        files = []
        labels = {}
        for i in range(len(folder)):
            file_path, label = folder[i]
            files.append(file_path)
            labels[file_path] = folder.classes[label]

        return files, labels


class ImageFolderLabelFileDatasetWrapper(_CommonImageDatasetWrapper):
    """DatasetWrapper for folder plus labels file.

    """
    column_separator = '\t'
    label_separator = ','

    def __init__(self, root_dir=None, input_file=None, all_labels=None, multilabel=False, ignore_data_errors=True):
        """
        The constructor.

        :param root_dir: root directory containing all images
        :type root_dir: str
        :param input_file: path to label file containing name of the image and list of labels
        :type input_file: str
        :param all_labels: list of all labels provided if the list of labels is different from those in input_file
        :type all_labels: typing.List[str]
        :param multilabel: flag for multilabel
        :type multilabel: bool
        :param ignore_data_errors: boolean flag on whether to ignore input data errors
        :type ignore_data_errors: bool
        """
        labels_dict = self._get_files_to_labels_dict(root_dir=root_dir, input_file=input_file, multilabel=multilabel,
                                                     ignore_data_errors=ignore_data_errors)

        # add missing labels in labels_list to this list
        augmented_all_labels = None if all_labels is None else list(all_labels)
        if all_labels is not None:
            # if there is a label in labels_dict not in labels, then error out
            if multilabel:
                set_found_labels = set(list(itertools.chain.from_iterable(labels_dict.values())))
            else:
                set_found_labels = set(labels_dict.values())

            set_all_labels = set(all_labels)
            new_labels = set_found_labels.difference(set_all_labels)
            if len(new_labels):
                augmented_all_labels.extend([label for label in new_labels])

        super().__init__(files_to_labels_dict=labels_dict, all_labels=augmented_all_labels,
                         multilabel=multilabel, ignore_data_errors=ignore_data_errors)

    def _get_files_to_labels_dict(self, root_dir=None, input_file=None, multilabel=False, ignore_data_errors=True):
        files_to_labels_dict = {}
        with open(input_file, newline='') as csvfile:
            try:
                csv_reader = csv.reader(csvfile, delimiter=ImageFolderLabelFileDatasetWrapper.column_separator,
                                        skipinitialspace=True)
            except csv.Error:
                raise AutoMLVisionDataException('Error reading input csv file', has_pii=False)
            for row in csv_reader:
                try:
                    if not row:
                        # skip empty lines
                        continue
                    if len(row) != 2:
                        raise AutoMLVisionDataException('More than 2 columns encountered in the input.',
                                                        has_pii=False)
                    filename, file_labels = row
                    full_path = os.path.join(root_dir, filename)
                    files_to_labels_dict[full_path] = self._get_labels_from_label_str(file_labels, multilabel)
                except AutoMLVisionDataException as ex:
                    if ignore_data_errors:
                        logging_utilities.log_traceback(ex, logger)
                    else:
                        raise

        return files_to_labels_dict

    def _get_labels_from_label_str(self, label_str, multilabel=False):
        """
        Get labels from the label part of the line in labels file.

        :param label_str: string of comma separated labels
        :type label_str: str
        :param multilabel: boolean flag indicating if it is a multilabel problem
        :type multilabel: bool
        :return: list of strings or string depending on whether this is a multilabel problem or not
        :rtype: typing.Union[typing.List[str], str]
        """
        try:
            files_labels_as_list = [
                x
                for x in list(csv.reader([label_str],
                                         delimiter=ImageFolderLabelFileDatasetWrapper.label_separator,
                                         quotechar='\'',
                                         skipinitialspace=True))[0]
            ]
        except csv.Error:
            raise AutoMLVisionDataException('Error reading labels', has_pii=False)

        if multilabel:
            labels = files_labels_as_list
        else:
            if len(files_labels_as_list) > 1:
                raise AutoMLVisionDataException('Encountered multi-label line in non multi-label input data',
                                                has_pii=False)
            else:
                labels = files_labels_as_list[0]

        return labels


class AmlDatasetWrapper(_CommonImageDatasetWrapper, AmlDatasetBaseWrapper):
    """DatasetWrapper for AzureML labeled dataset.
    """

    def __init__(self, dataset_id=None, multilabel=False, workspace=None,
                 ignore_data_errors=False, datasetclass=AmlDataset,
                 images_df=None, label_column_name=None, data_dir=None,
                 download_files=True):
        """Constructor - This reads the labeled dataset and downloads the images that it contains.
        :param dataset_id: dataset id
        :type dataset_id: str
        :param multilabel: Indicates that each image can have multiple labels.
        :type multilabel: bool
        :param workspace: workspace object
        :type workspace: azureml.core.Workspace
        :param ignore_data_errors: Setting this ignores and files in the labeled dataset that fail to download.
        :type ignore_data_errors: bool
        :param datasetclass: The source dataset class.
        :type datasetclass: class
        :param images_df: Labeled dataset dataframe.
        :type images_df: pandas DataFrame
        :param label_column_name: Label column name.
        :type label_column_name: str
        :param data_dir: Folder for downloaded images.
        :type data_dir: str
        :param download_files: Flag to download files or not.
        :type download_files: bool
        """

        if images_df is not None:
            if label_column_name is None:
                raise AutoMLVisionDataException('label_column_name cannot be None if image_df is specified',
                                                has_pii=False)

            if data_dir is None:
                raise AutoMLVisionDataException('data_dir cannot be None if image_df is specified',
                                                has_pii=False)

            self._images_df = images_df.reset_index(drop=True)
            self._label_column_name = label_column_name
            self._data_dir = data_dir
        else:
            labeled_dataset_helper = AmlLabeledDatasetHelper(dataset_id, workspace, ignore_data_errors, datasetclass,
                                                             image_column_name=self.DATASET_IMAGE_COLUMN_NAME,
                                                             download_files=download_files)

            self._label_column_name = labeled_dataset_helper.label_column_name
            self._images_df = labeled_dataset_helper.images_df
            self._data_dir = labeled_dataset_helper._data_dir

        self._ignore_data_errors = ignore_data_errors
        self._multilabel = multilabel

        if self._label_column_name not in self._images_df:
            raise AutoMLVisionDataException("No labels found to initialize dataset.", has_pii=False)

        labels = self._get_labels(self._images_df[self._label_column_name].tolist(), multilabel=multilabel)
        files_to_labels_dict = self._get_files_to_labels_dict(self._images_df, ignore_data_errors)

        super().__init__(files_to_labels_dict, labels, multilabel=multilabel, ignore_data_errors=ignore_data_errors)

    def _get_files_to_labels_dict(self, images_df, ignore_data_errors=True):

        files_to_labels_dict = {}

        for index, label in enumerate(images_df[self._label_column_name]):

            full_path = self.get_image_full_path(index)

            files_to_labels_dict[full_path] = label

        return files_to_labels_dict

    def get_image_full_path(self, index):
        """Return the full local path for an image.

        :param index: index
        :type index: int
        :return: Full path for the local image file
        :rtype: str
        """
        return AmlLabeledDatasetHelper.get_full_path(index, self._images_df, self._data_dir)

    def _get_labels(self, labels_list, multilabel):
        """
        :param labels_list: list of labels. list of lists of string when its multilabel otherwise list of strings
        :type labels_list: typing.Union[typing.List[typing.List[str]], typing.List[str]]
        :param multilabel: boolean flag for whether this is multilabel problem
        :type multilabel: bool
        :return: flat list of unique labels
        :rtype: typing.List[str]
        """
        if multilabel:
            return list(set(itertools.chain.from_iterable(labels_list)))
        else:
            return list(set(labels_list))

    def train_val_split(self, test_size=0.2):
        """Split a dataset into two parts for train and validation.

        :param test_size: The fraction of the data for the second (test) dataset.
        :type test_size: float
        :return: Two AmlDatasetWrapper objects containing the split data.
        :rtype: AmlDatasetWrapper, AmlDatasetWrapper
        """
        train, test = train_test_split(self._images_df, test_size=test_size)
        return self.clone_dataset(train), self.clone_dataset(test)

    def clone_dataset(self, images_df):
        """Create a copy of a dataset but with the specified image dataframe.

        :param images_df: Labeled dataset DataFrame.
        :type images_df: pandas.DataFrame
        :return: The copy of the AmlDatasetWrapper.
        :rtype: AmlDatasetWrapper
        """
        return AmlDatasetWrapper(images_df=images_df,
                                 label_column_name=self._label_column_name,
                                 ignore_data_errors=self._ignore_data_errors,
                                 data_dir=self._data_dir,
                                 multilabel=self._multilabel)


class OverSamplingDatasetWrapper(BaseDatasetWrapper):
    """Takes a datasetwrapper and oversamples to make sure the class sizes are balanced."""

    def __init__(self, dataset_wrapper):
        """
        :param dataset_wrapper: datasetwrapper object implementing BaseDatasetWrapper
        :type dataset_wrapper: azureml.contrib.automl.dnn.vision.classification.io.read.BaseDatasetWrapper
        """
        label_to_indices_dict = self._get_samples_by_classes(dataset_wrapper)
        oversampling_ratios = self._get_oversampling_ratios(label_to_indices_dict, dataset_wrapper)
        num_labels = len(oversampling_ratios)
        label_sizes = [len(label_to_indices_dict[i]) for i in range(num_labels)]

        # generate new indices
        self._indices = []
        self._labels = []

        for i in range(num_labels):
            self._indices.extend(label_to_indices_dict[i] * oversampling_ratios[i])
            self._labels.extend([dataset_wrapper.labels[i]] * label_sizes[i] * oversampling_ratios[i])

        self._dataset_wrapper = dataset_wrapper

    def _get_samples_by_classes(self, dataset_wrapper):
        """
        :param dataset_wrapper: datasetwrapper object implementing BaseDatasetWrapper
        :type dataset_wrapper: azureml.contrib.automl.dnn.vision.classification.io.read.BaseDatasetWrapper
        :return: dictionary of labels to list of indices
        :rtype: typing.Dict[int, typing.List[int]]
        """
        label_to_indices_dict = {}
        label_str_to_index = {}
        for i, label in enumerate(dataset_wrapper.labels):
            label_to_indices_dict[i] = []
            label_str_to_index[label] = i

        for i in range(len(dataset_wrapper)):
            label_to_indices_dict[label_str_to_index[dataset_wrapper.label_at_index(i)]].append(i)

        return label_to_indices_dict

    def _get_oversampling_ratios(self, label_to_indices_dict, dataset_wrapper):
        """
        :param label_to_indices_dict: dictionary of labels to list of indices
        :type label_to_indices_dict: typing.Dict[int, typing.List[int]]
        :param dataset_wrapper: object of type BaseDatasetWrapper
        :type dataset_wrapper: azureml.contrib.automl.dnn.vision.classification.io.read.BaseDatasetWrapper
        :return: list of oversampling ratios by label
        :rtype: typing.List[int]
        """
        num_labels = len(dataset_wrapper.labels)

        label_sizes = []
        for i in range(num_labels):
            label_sizes.append(len(label_to_indices_dict[i]))

        max_label_size = max(label_sizes)

        over_sampling_ratios = [0] * num_labels

        # now oversample other classes
        for i in range(num_labels):
            if label_sizes[i] != 0:
                over_sampling_ratios[i] = int(max_label_size / label_sizes[i])

        return over_sampling_ratios

    def __len__(self):
        """
        :return: number of items in dataset
        :rtype: int
        """
        return len(self._indices)

    def pad(self, padding_factor):
        """Pad the dataset so that its length can be evenly divided by padding_factor

        :param padding_factor: padding factor
        :type padding_factor: int
        """
        self._indices = _pad(self._indices, padding_factor)

    def item_at_index(self, index):
        """Return image at index.

        :param index: index
        :type index: int
        :return: pillow image object
        :rtype: Image
        """
        return self._dataset_wrapper.item_at_index(self._indices[index])

    def label_at_index(self, index):
        """Return label at index.

        :param index: index
        :type index: int
        :return: string label or list of string labels if multilabel
        :rtype: typing.Union[str, typing.List[str]]
        """
        return self._dataset_wrapper.label_at_index(self._indices[index])
