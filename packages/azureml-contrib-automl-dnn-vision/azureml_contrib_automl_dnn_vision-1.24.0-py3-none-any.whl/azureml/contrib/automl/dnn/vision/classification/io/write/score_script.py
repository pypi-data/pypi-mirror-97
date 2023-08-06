# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Score images from model produced by another run."""

import argparse

from azureml.train.automl import constants
from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.constants import ScoringLiterals, SettingsLiterals
from azureml.contrib.automl.dnn.vision.classification.inference.score import score

logger = get_logger(__name__)


@utils._exception_handler
def main():
    """Wrapper method to execute script only when called and not when imported."""
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument(utils._make_arg(ScoringLiterals.RUN_ID),
                        help='run id of the experiment that generated the model')
    parser.add_argument(utils._make_arg(ScoringLiterals.EXPERIMENT_NAME),
                        help='experiment that ran the run which generated the model')
    parser.add_argument(utils._make_arg(ScoringLiterals.OUTPUT_FILE),
                        help='path to output file')
    parser.add_argument(utils._make_arg(ScoringLiterals.ROOT_DIR),
                        help='path to root dir for files listed in image_list_file')
    parser.add_argument(utils._make_arg(ScoringLiterals.IMAGE_LIST_FILE),
                        help='image files list')
    parser.add_argument(utils._make_arg(SettingsLiterals.OUTPUT_DATASET_TARGET_PATH),
                        help='datastore target path for output dataset files')
    parser.add_argument(utils._make_arg(ScoringLiterals.INPUT_DATASET_ID),
                        help='input_dataset_id')
    parser.add_argument(utils._make_arg(ScoringLiterals.OUTPUT_FEATURIZATION),
                        help='run featurization and output feature vectors',
                        type=bool, default=False)
    parser.add_argument(utils._make_arg(ScoringLiterals.FEATURIZATION_OUTPUT_FILE),
                        help='path to featurization output file')
    parser.add_argument(utils._make_arg(ScoringLiterals.LOG_OUTPUT_FILE_INFO),
                        help='log output file debug info', type=bool, default=False)

    args, unknown = parser.parse_known_args()

    # Set up logging
    task_type = constants.Tasks.IMAGE_CLASSIFICATION
    utils._set_logging_parameters(task_type, args)

    # TODO JEDI
    # When we expose the package to customers we need to revisit. We should not log any unknown
    # args when the customers send their hp space.
    if unknown:
        logger.info("Got unknown args, will ignore them: {}".format(unknown))

    device = utils._get_default_device()

    score(args.run_id, device=device,
          experiment_name=args.experiment_name,
          output_file=args.output_file, root_dir=args.root_dir,
          image_list_file=args.image_list_file,
          output_dataset_target_path=args.output_dataset_target_path,
          input_dataset_id=args.input_dataset_id,
          output_featurization=args.output_featurization,
          featurization_output_file=args.featurization_output_file,
          log_output_file_info=args.log_output_file_info)


if __name__ == "__main__":
    # execute only if run as a script
    main()
