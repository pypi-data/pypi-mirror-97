import os
import onnx
import onnxruntime as ort
import pickle
import torch
import torchvision.transforms as transforms

from azureml.contrib.automl.dnn.vision.common.constants import ArtifactLiterals


def _to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


def check_exported_onnx_model(onnx_model_path, wrapper, input, device, get_torch_outputs_fn,
                              is_norm=False, check_output_parity=True):
    onnx_model = onnx.load(onnx_model_path)
    onnx.checker.check_model(onnx_model)

    ort_session = ort.InferenceSession(onnx_model_path)

    ort_img = input
    torch_img = input
    if is_norm:
        ort_img = input * 255.
        torch_img = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(input.squeeze(0))
        torch_img = torch_img.unsqueeze(0)

    ort_inputs = {ort_session.get_inputs()[0].name: _to_numpy(ort_img)}
    ort_outs = ort_session.run(None, ort_inputs)
    torch_outs = get_torch_outputs_fn(wrapper, torch_img, device)

    # compare ONNX Runtime and PyTorch results
    if check_output_parity:
        try:
            torch.testing.assert_allclose(_to_numpy(torch_outs), ort_outs[0], rtol=1e-03, atol=1e-05)
        except AssertionError as error:
            raise


def check_exported_onnx_od_model(onnx_model_path, wrapper, input, device, get_torch_outputs_fn,
                                 is_norm=False, check_output_parity=True):
    onnx_model = onnx.load(onnx_model_path)
    onnx.checker.check_model(onnx_model)

    ort_session = ort.InferenceSession(onnx_model_path)

    ort_img = input
    torch_img = input
    if is_norm:
        ort_img = input * 255.

    ort_inputs = {ort_session.get_inputs()[0].name: _to_numpy(ort_img)}
    ort_outs = ort_session.run(None, ort_inputs)
    torch_outs = get_torch_outputs_fn(wrapper, torch_img, device)

    # compare ONNX Runtime and PyTorch results
    if check_output_parity:
        outputs, _ = torch.jit._flatten(torch_outs)
        outputs = list(map(_to_numpy, outputs))
        for i in range(0, len(outputs)):
            try:
                torch.testing.assert_allclose(outputs[i], ort_outs[i], rtol=1e-03, atol=1e-05)
            except AssertionError as error:
                raise


def mock_prepare_model_export(run, model_wrapper, model_weights, output_dir, task_type=""):
    # Ensures prepare_model_export is called
    model_wrapper_location = os.path.join(output_dir, ArtifactLiterals.MODEL_WRAPPER_PKL)
    model_weights_location = os.path.join(output_dir, ArtifactLiterals.MODEL_FILE_NAME)
    with open(model_wrapper_location, 'wb') as pickle_file:
        pickle.dump(model_wrapper, pickle_file)
    torch.save(model_weights, model_weights_location)
