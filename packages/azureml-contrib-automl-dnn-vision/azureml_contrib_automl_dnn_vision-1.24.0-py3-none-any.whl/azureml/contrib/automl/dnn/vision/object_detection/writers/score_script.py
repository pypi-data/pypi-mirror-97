# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Score images from model produced by another run."""

import argparse

from azureml.contrib.automl.dnn.vision.common import utils
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.constants import ScoringLiterals, SettingsLiterals
from azureml.contrib.automl.dnn.vision.object_detection.writers.score import score
from azureml.contrib.automl.dnn.vision.object_detection.common.constants import ScoringParameters, \
    FasterRCNNParameters, FasterRCNNLiterals

logger = get_logger(__name__)


TASK_TYPE = "%%TASK_TYPE%%"


@utils._exception_handler
def main(raw_args=None):
    """Wrapper method to execute script only when called and not when imported.

    :param raw_args: a list of arguments to pass to argparse. If None, the command line arguments are parsed.
                     Useful for testing this method.
    :type raw_args: list
    """

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
                        help='image object detection files list')
    parser.add_argument(utils._make_arg(ScoringLiterals.BATCH_SIZE),
                        help='batch_size for inference', type=int,
                        default=ScoringParameters.DEFAULT_SCORING_BATCH_SIZE)
    parser.add_argument(utils._make_arg(SettingsLiterals.OUTPUT_DATASET_TARGET_PATH),
                        help='datastore target path for output dataset files')
    parser.add_argument(utils._make_arg(ScoringLiterals.INPUT_DATASET_ID),
                        help='input_dataset_id')
    parser.add_argument(utils._make_arg(ScoringLiterals.VALIDATE_SCORE),
                        help='validate score if ground truth given in dataset',
                        type=bool, default=False)
    parser.add_argument(utils._make_arg(ScoringLiterals.LOG_OUTPUT_FILE_INFO),
                        help='log output file debug info', type=bool, default=False)

    # Faster-rcnn Settings
    parser.add_argument(utils._make_arg(FasterRCNNLiterals.MIN_SIZE), type=int,
                        help="minimum size of the image to be rescaled before feeding it to the backbone",
                        default=FasterRCNNParameters.DEFAULT_MIN_SIZE)
    parser.add_argument(utils._make_arg(FasterRCNNLiterals.BOX_SCORE_THRESH), type=float,
                        help="during inference, only return proposals with a classification score \
                        greater than box_score_thresh",
                        default=FasterRCNNParameters.DEFAULT_BOX_SCORE_THRESH)
    parser.add_argument(utils._make_arg(FasterRCNNLiterals.BOX_NMS_THRESH), type=float,
                        help="NMS threshold for the prediction head. Used during inference",
                        default=FasterRCNNParameters.DEFAULT_BOX_NMS_THRESH)
    parser.add_argument(utils._make_arg(FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG), type=int,
                        help="maximum number of detections per image, for all classes.",
                        default=FasterRCNNParameters.DEFAULT_BOX_DETECTIONS_PER_IMG)

    args, unknown = parser.parse_known_args()

    # Set up logging
    task_type = TASK_TYPE
    utils._set_logging_parameters(task_type, args)

    # TODO JEDI
    # When we expose the package to customers we need to revisit. We should not log any unknown
    # args when the customers send their hp space.
    if unknown:
        logger.info("Got unknown args, will ignore them: {}".format(unknown))

    fasterrcnn_settings = {
        FasterRCNNLiterals.MIN_SIZE: args.min_size,
        FasterRCNNLiterals.BOX_SCORE_THRESH: args.box_score_thresh,
        FasterRCNNLiterals.BOX_NMS_THRESH: args.box_nms_thresh,
        FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG: args.box_detections_per_img
    }

    device = utils._get_default_device()

    score(args.run_id, device=device,
          experiment_name=args.experiment_name,
          output_file=args.output_file, root_dir=args.root_dir,
          image_list_file=args.image_list_file,
          batch_size=args.batch_size,
          output_dataset_target_path=args.output_dataset_target_path,
          input_dataset_id=args.input_dataset_id,
          validate_score=args.validate_score,
          log_output_file_info=args.log_output_file_info,
          **fasterrcnn_settings)


if __name__ == "__main__":
    # execute only if run as a script
    main()
