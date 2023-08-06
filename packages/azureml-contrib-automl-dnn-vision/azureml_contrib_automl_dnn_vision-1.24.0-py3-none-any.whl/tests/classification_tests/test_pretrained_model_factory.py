import importlib
import pytest
import torch
import torchvision
from azureml.contrib.automl.dnn.vision.common.constants import PretrainedModelNames, PretrainedModelUrls
from azureml.contrib.automl.dnn.vision.common.pretrained_model_utilities import PretrainedModelFactory
from unittest.mock import Mock


def _mock_load_state_dict_from_url(num_exceptions=0, real_state_dict=None):
    count = 0

    def fn(*args, **kwargs):
        nonlocal count
        count += 1
        if count <= num_exceptions:
            raise ConnectionResetError
        else:
            return real_state_dict
    return fn


@pytest.mark.usefixtures('new_clean_dir')
def test_get_pretrained_models():
    mdl = PretrainedModelFactory.resnet18(pretrained=True)
    assert mdl is not None
    mdl = PretrainedModelFactory.resnet50(pretrained=True)
    assert mdl is not None
    mdl = PretrainedModelFactory.mobilenet_v2(pretrained=True)
    assert mdl is not None
    mdl = PretrainedModelFactory.se_resnext50_32x4d(pretrained=True)
    assert mdl is not None
    mdl = PretrainedModelFactory.fasterrcnn_resnet50_fpn(pretrained=True)
    assert mdl is not None
    mdl = PretrainedModelFactory.resnet_fpn_backbone(PretrainedModelNames.RESNET18, pretrained=True)
    assert mdl is not None
    mdl = PretrainedModelFactory.maskrcnn_resnet50_fpn(pretrained=True)
    assert mdl is not None


@pytest.mark.usefixtures('new_clean_dir')
def test_get_pretrained_models_yolo():
    ckpt = PretrainedModelFactory._load_state_dict_from_url_with_retry(
        PretrainedModelUrls.MODEL_URLS[PretrainedModelNames.YOLOV5_SMALL], map_location=torch.device("cpu"))
    assert ckpt is not None
    ckpt = PretrainedModelFactory._load_state_dict_from_url_with_retry(
        PretrainedModelUrls.MODEL_URLS[PretrainedModelNames.YOLOV5_MEDIUM], map_location=torch.device("cpu"))
    assert ckpt is not None
    ckpt = PretrainedModelFactory._load_state_dict_from_url_with_retry(
        PretrainedModelUrls.MODEL_URLS[PretrainedModelNames.YOLOV5_LARGE], map_location=torch.device("cpu"))
    assert ckpt is not None
    ckpt = PretrainedModelFactory._load_state_dict_from_url_with_retry(
        PretrainedModelUrls.MODEL_URLS[PretrainedModelNames.YOLOV5_XLARGE], map_location=torch.device("cpu"))
    assert ckpt is not None


@pytest.mark.usefixtures('new_clean_dir')
def test_load_state_dict_from_url_with_retry(monkeypatch):
    with monkeypatch.context() as m:
        state_dict = PretrainedModelFactory.resnet18(pretrained=True).state_dict()
        import azureml.contrib.automl.dnn.vision.common.pretrained_model_utilities as model_utils
        mock_fn = Mock(side_effect=_mock_load_state_dict_from_url(num_exceptions=0, real_state_dict=state_dict))
        m.setattr(torchvision.models.utils, 'load_state_dict_from_url', mock_fn)
        # since PretrainedModelFactory is already imported, we need to reload it. Just importing will reuse already
        # imported modules.
        importlib.reload(model_utils)
        model_utils.PretrainedModelFactory.resnet18(pretrained=True)
        assert mock_fn.call_count == 1

    with monkeypatch.context() as m:
        state_dict = PretrainedModelFactory.resnet18(pretrained=True).state_dict()
        mock_fn = Mock(side_effect=_mock_load_state_dict_from_url(num_exceptions=1, real_state_dict=state_dict))
        m.setattr(torchvision.models.utils, 'load_state_dict_from_url', mock_fn)
        importlib.reload(model_utils)
        model_utils.PretrainedModelFactory.resnet18(pretrained=True)
        assert mock_fn.call_count == 2

    # Reload it here so that tests (which use pretrained_model_utilities)
    # run after this one will not use mock anymore
    importlib.reload(model_utils)
