import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.transforms import (
    CenterCrop,
    Compose,
    RandomResizedCrop,
    Resize,
    ToTensor,
    v2,
)


def _test_dataset(example_dataset, DogsCatsData):
    assert isinstance(
        example_dataset, DogsCatsData
    ), "The dataset is not an instance of DogsCatsData."
    assert isinstance(
        example_dataset.transform, (Compose, ToTensor, v2.Compose, v2.ToTensor)
    ), "You have not included the transform."


def test_number_of_samples(
    example_dataset, number_of_samples, DogsCatsData, verbose=True
):
    _test_dataset(example_dataset, DogsCatsData)
    assert number_of_samples == 1750, "The number of samples is incorrect."
    if verbose:
        print("Test passed")


def test_label(example_dataset, label, DogsCatsData, verbose=True):
    _test_dataset(example_dataset, DogsCatsData)
    assert label == 0, "The label is incorrect"
    if verbose:
        print("Test passed")


def test_dataloader(dataloader, verbose=True):
    assert isinstance(
        dataloader, DataLoader
    ), "The dataloader is not an instance of torch.utils.data.Dataloader."
    assert isinstance(
        dataloader.dataset.transform, (Compose, v2.Compose)
    ), "The dataset should have transform as Compose(...)."
    transforms = dataloader.dataset.transform.transforms
    assert (
        sum(
            [
                isinstance(
                    t,
                    (
                        Resize,
                        CenterCrop,
                        RandomResizedCrop,
                        v2.Resize,
                        v2.CenterCrop,
                        v2.RandomResizedCrop,
                    ),
                )
                for t in transforms
            ]
        )
        >= 1
    ), "The dataset's transform should include a transformation that resizes images to the same size."
    assert (
        sum([isinstance(t, (ToTensor, v2.ToTensor)) for t in transforms]) >= 1
        or sum([isinstance(t, (v2.ToImage, v2.ToDtype)) for t in transforms]) >= 2
    ), "The dataset's transform should include ToTensor() or v2.Compose([v2.ToImage(), v2.ToDtype(torch.float32, scale=True)])."
    if verbose:
        print("Test passed")


def test_model(model_class, verbose=True):
    assert issubclass(
        model_class, nn.Module
    ), "Model class should inherit from torch.nn.Module"

    assert (
        getattr(model_class, "forward", None) is not None
    ), "Model class should have a 'forward' method"

    _test_output(model_class, some_img_size=224, some_batch_size=64)
    _test_output(model_class, some_img_size=32, some_batch_size=8)
    if verbose:
        print("Test passed.")


def _test_output(model_class, some_img_size, some_batch_size):
    random_input = torch.rand(some_batch_size, 3, some_img_size, some_img_size)
    model_instance = model_class(img_size=some_img_size)
    output = model_instance.forward(random_input)
    output_shape = list(output.shape)
    assert output_shape == [
        some_batch_size
    ], f"Expected output size [{some_batch_size}], got {output_shape}"


def _flatten_model(modules):
    def _flatten_list(_2d_list):
        flat_list = []
        # Iterate through the outer list
        for element in _2d_list:
            if isinstance(element, list):
                # If the element is of isinstance list, iterate through the sublist
                for item in element:
                    flat_list.append(item)
            else:
                flat_list.append(element)
        return flat_list

    ret = []
    try:
        for _, n in modules:
            ret.append(_flatten_model(n))
    except:
        try:
            if str(modules._modules.items()) == "odict_items([])":
                ret.append(modules)
            else:
                for _, n in modules._modules.items():
                    ret.append(_flatten_model(n))
        except:
            ret.append(modules)
    return _flatten_list(ret)


def test_architecture(FirstCnn, verbose=True):
    layers = np.array(_flatten_model(FirstCnn(64)))

    layers_checks = np.vstack(
        [
            np.array(
                [
                    isinstance(layer, nn.Conv2d)
                    and layer.in_channels == 3
                    and layer.out_channels == 10
                    and layer.kernel_size == (3, 3)
                    and layer.stride == (1, 1)
                    and layer.padding == (0, 0)
                    for layer in layers
                ]
            ),
            np.array(
                [
                    isinstance(layer, nn.Conv2d)
                    and layer.in_channels == 10
                    and layer.out_channels == 10
                    and layer.kernel_size == (3, 3)
                    and layer.stride == (1, 1)
                    and layer.padding == (0, 0)
                    for layer in layers
                ]
            ),
            np.array([isinstance(layer, nn.Linear) for layer in layers]),
            np.array([isinstance(layer, (nn.Sigmoid, nn.Softmax)) for layer in layers]),
        ]
    )

    conv0 = layers[layers_checks[0]]
    conv1 = layers[layers_checks[1]]
    linears = layers[layers_checks[2]]
    activations = layers[layers_checks[3]]
    assert (
        len(conv0) == 1
    ), 'There should be defined exactly one convolution of the first "type" specified in the task description. Please make sure that you define it in the __init__(...) function of your class and use it in the forward(...) function accordingly.'
    assert (
        len(conv1) == 1
    ), 'There should be defined exactly one convolution of the second "type" specified in the task description. Please make sure that you define it in the __init__(...) function of your class and use it in the forward(...) function accordingly.'
    assert (
        len(linears) == 1
    ), "There should be defined exactly one fully connected layer specified in the task description. Please make sure that you define it in the __init__(...) function of your class and use it in the forward(...) function accordingly."
    assert (
        len(activations) == 1
    ), "There should be defined exactly one final activation. Please make sure that you define it in the __init__(...) function of your class and use it in the forward(...) function accordingly."
    assert any(
        [
            isinstance(
                layer,
                (
                    nn.ReLU,
                    nn.SiLU,
                    nn.SELU,
                    nn.Tanh,
                    nn.CELU,
                    nn.ELU,
                    nn.RReLU,
                    nn.LeakyReLU,
                    nn.PReLU,
                    nn.LeakyReLU,
                    nn.GELU,
                ),
            )
            for layer in layers
        ]
    ), "There is no intermediate activation function defined in the class attributes. Please add, e.g., `self.relu = nn.ReLU()` in the __init__(...) function of your class, and use it in the forward(...) function after each convolution."

    linear_layer = linears[0]
    activation_layer = activations[0]
    if linear_layer.out_features == 1:
        assert isinstance(
            activation_layer, nn.Sigmoid
        ), "The final activation is expected to be sigmoid."
    else:
        assert (
            linear_layer.out_features == 2
        ), "The fully connected layer's output dimension should be either 2 or 1. However, 1 is preferred. (why?)"
        print(
            "WARNING: the fully connected layer's output dimension 2 is not preferred. (why?)"
        )
        assert (
            isinstance(activation_layer, nn.Softmax) and activation_layer.dim == 2
        ), "You chose the output dimension of the fully connected layer to be 2, but then the final activation should be softmax."

    if verbose:
        print("Test passed")


def test_output_to_label(fn, verbose=True):
    batch_size = torch.randint(1, 64, (1,))
    random_logits = torch.rand(batch_size)
    random_probs = random_logits / random_logits.sum()
    labels = fn(random_probs)
    assert (
        labels.shape == random_logits.shape
    ), "The element-wise function should preserve the shape"
    assert (
        labels.dtype == random_probs.dtype
    ), f"Incorrect datatype, should be the same as the input datatype."
    fixed_logits = torch.tensor([0.1, 0.9, 0.51, 0.49, 0.7])
    fixed_labels = torch.tensor([0, 1, 1, 0, 1], dtype=fixed_logits.dtype)
    assert all(fixed_labels == fn(fixed_logits)), "Incorrect fixed output"
    assert (
        fixed_logits.device == fixed_labels.device
    ), "Make sure that the output tensor is on the same device"
    if verbose:
        print("Test passed")


def test_TL_head(head, base_model, verbose=True):
    layers = np.array(_flatten_model(head))

    linears_check = np.array([isinstance(layer, nn.Linear) for layer in layers])
    activation_check = np.array(
        [isinstance(layer, (nn.Sigmoid, nn.Softmax)) for layer in layers]
    )

    first_linear = layers[linears_check][0]
    last_linear_layer = layers[linears_check][-1]
    assert (
        first_linear.in_features == base_model.classifier[1].in_features
    ), "The head's input feature dimensionality does not match the base model output feature (backbone) dimensionality. If it does, please make sure that the layers in the __init__(...) function are defined in the right order."

    activations = layers[activation_check]
    assert (
        len(activations) == 1
    ), "There should be defined exactly one final activation. Please make sure that you define it in the __init__(...) function of your class and use it in the forward(...) function accordingly."
    activation_layer = activations[0]
    if last_linear_layer.out_features == 1:
        assert isinstance(
            activation_layer, nn.Sigmoid
        ), "The final activation is expected to be sigmoid."
    else:
        assert (
            last_linear_layer.out_features == 2
        ), "The fully connected layer's output dimension should be either 2 or 1. However, 1 is preferred. (why?)"
        print(
            "WARNING: the fully connected layer's output dimension 2 is not preferred. (why?)"
        )
        assert (
            isinstance(activation_layer, nn.Softmax) and activation_layer.dim == 2
        ), "You chose the output dimension of the fully connected layer to be 2, but then the final activation should be softmax."
    if verbose:
        print("Test passed")


def test_TL_model_1(TL_model, head, verbose=True):
    layers = _flatten_model(TL_model)
    layers_head = _flatten_model(head)
    assert all(
        [
            isinstance(l1, type(l2))
            for l1, l2 in zip(layers[-1::-1], layers_head[-1::-1])
        ]
    ), "The head should be attached in the end after the base model features (backbone)."
    if verbose:
        print("Test passed")


def test_TL_model_2(TL_model, head, verbose=True):
    layers_features = _flatten_model(TL_model.features)
    layers = _flatten_model(TL_model)
    layers_head = _flatten_model(head)
    assert all(
        [
            isinstance(l1, type(l2))
            for l1, l2 in zip(layers[len(layers_features) :], layers_head)
        ]
    ), "The whole base model head should be substituted with the new head."
    if verbose:
        print("Test passed")


def test_TL_model_parameters_for_transfer_learning(TL_model, verbose=True):
    for param in TL_model.features.parameters():
        assert (
            param.requires_grad is False
        ), "The backbone feature parameters have not been frozen."
    if verbose:
        print("Test passed")


def _test_image_sizes(dataloader):
    img_height, img_width = next(iter(dataloader))[0].shape[2:4]
    assert img_height == 224, "Image height is not suitable for the backbone model."
    assert img_width == 224, "Image width is not suitable for the backbone model."


def test_dataloader_for_transfer_learning(dataloader, verbose=True):
    assert isinstance(
        dataloader, DataLoader
    ), "The dataloader is not an instance of torch.utils.data.Dataloader."
    assert (
        sum(
            [
                isinstance(t, (ToTensor, v2.ToTensor))
                for t in dataloader.dataset.transform.transforms
            ]
        )
        >= 1
    ), "The dataset's transform should include ToTensor()."
    _test_image_sizes(dataloader)
    if verbose:
        print("Test passed")


def test_TL_model_parameters_for_fine_tuning(backbone_model, verbose=True):
    for param in backbone_model.features.parameters():
        assert (
            param.requires_grad is True
        ), "The backbone feature parameters have not been unfrozen."
    if verbose:
        print("Test passed")


def test_learning_rate(learning_rate, verbose=True):
    assert learning_rate <= 0.0005, "Learning rate is too high."
    if verbose:
        print("Test passed")


def test_dataloaders_for_final_training(
    full_train_dataloader, full_val_dataloader, verbose=True
):
    assert (
        len(full_train_dataloader.dataset) + len(full_val_dataloader.dataset) == 12500
    ), "You did not load full data."
    if verbose:
        print("Test passed")
