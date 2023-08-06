#!/usr/bin/env python
# ******************************************************************************
# Copyright 2019 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""Parsing function to generate layers mapping between Keras and Akida.
Two data classes store the mapping: LayerMapping and ModelMapping.

"""
import tensorflow.keras.layers as layers
from akida import LayerType
from . import quantization_layers as qlayers


class LayerMapping:
    """ Creates a layer map of a single Akida layer from Keras layers.

    This data class stores the indices of Keras layers that represent a
    single Akida layer. For example, a 'Convolutional' Akida layer corresponds
    to multiple Keras layers:
    - a Conv2D/QuantizedConv2D layer
    - an optional batch normalization layer
    - an optional pooling layer
    - a ReLU or discrete ReLU activation (optional if last layer)

    Args:
        layer_type (:obj:`akida.LayerType`): the type of the Akida layer.
        index_neural (int): the index of the corresponding Keras
            neural layer.

    """

    def __init__(self, layer_type, index_neural):
        self.layer_type = layer_type
        self.index_neural = index_neural
        self.index_pool = None
        self.index_batchnorm = None
        self.index_activation = None


class ModelMapping:
    """This data class maps a Keras model to a future Akida model (not built yet).

    When an instance of ModelMapping is created, it will generate a list of
    LayerMapping objects mapping the Keras model with a succession of Akida
    layers.
    A check is then performed to ensure that the Keras model is compatible with
    Akida.

    Note:
        Note that no Akida model is generated at this step: only a mapping is
        created.

    """

    def __init__(self, model_keras, layer_maps):
        self.model_keras = model_keras
        self.layer_maps = layer_maps


def _check_layers_data_format(model):
    """Asserts that all layers in the model are 'channels_last'.

    Args:
        model (tf.keras.model): the Keras model to check.
    """

    # Error if 'data_format' is 'channels_first'
    for layer in model.layers:
        if hasattr(layer, 'data_format'):
            if layer.data_format == "channels_first":
                raise RuntimeError("unsupported data format channels_first")


def _check_model_input_output(model):
    """Asserts that model inputs/outputs are supported for conversion.

    The Keras model must have only one input layer and one output layer. The
    input shape must 4-D (N, H, W, C).

    Args:
        model (tf.keras.model): the Keras model to check.
    """

    # Error if multiple inputs
    if len(model.input_names) > 1:
        raise RuntimeError("Model must have only one input layer. Receives "
                           f"inputs {model.input_names}.")

    # Error if multiple outputs
    if len(model.output_names) > 1:
        raise RuntimeError("Model must have only one output layer. Receives "
                           f"outputs {model.output_names}.")

    # Error if input shape is not 4D, i.e. (N, H, W, C)
    input_shape = model.input_shape
    if len(input_shape) != 4:
        err_msg = ("Input shape of model must be 4-D (batch size + 3-D "
                   f"tensors). Receives input shape {input_shape}. ")
        if len(input_shape) == 2:
            err_msg += (
                "If your model begins with a Dense layer, you must "
                "start your model with a Flatten layer and an input shape of "
                f" (1, 1, {input_shape[1]}) instead of {(input_shape[1],)}.")
        raise RuntimeError(err_msg)


def _map_first_layer(model, input_is_image):
    """Map the first layers of the Keras model to an Akida layer.

    To be Akida-compatible, the first layers of the quantized Keras model must
    be:

    - an optional InputLayer.
    - an optional Rescaling layer
    - the first neural layer. If input is image, this layer must be a Conv2D
        with 1 or 3 channels.

    Depending on input_is_image, an InputData or an InputConvolutional is
    returned. The index of the next layer to process is also returned.

    Args:
        model (tf.keras model): the model to parse.
        input_is_image (bool): True if input is an image (8-bit input with 1 or
            3 channels) followed by QuantizedConv2D. Akida model input will be
            InputConvolutional. If False, Akida model input will be InputData.

    Returns:
       :obj:`LayerMapping`: a layer map corresponding to the first Akida layer.
       int: the index of the next layer to process.

    """

    next_layer = 0
    # If first layer is input layer, skip it
    if isinstance(model.layers[0], layers.InputLayer):
        next_layer = 1

    # If next layer is Rescaling layer, skip it
    if isinstance(model.layers[next_layer],
                  layers.experimental.preprocessing.Rescaling):
        next_layer += 1

    # Get first Akida layer
    if not input_is_image:
        layer_ak = LayerMapping(LayerType.InputData, next_layer)
    else:
        # Error if input_is_image=True and first layer is not a Conv2D
        # or input channels is not 1 or 3.
        if (not isinstance(model.layers[next_layer], layers.Conv2D) or
                not model.layers[next_layer].input_shape[-1] in (1, 3)):
            err_msg = (f"With input_is_image=True, first layer "
                       f"'{model.layers[next_layer].name}' must be"
                       f" Conv2D and input shape must have 1 or 3 channels. "
                       f"Receives layer of type "
                       f"{model.layers[next_layer].__class__.__name__} with "
                       f"{model.layers[next_layer].input_shape[-1]} channels.")
            raise RuntimeError(err_msg)
        layer_ak = LayerMapping(LayerType.InputConvolutional, next_layer)
        next_layer += 1

    return layer_ak, next_layer


def _get_akida_layer_type(layer):
    """Returns Akida layer type of a Keras neural layer

    Args:
        layer (:obj:`tf.keras.layers.Layer`): a Keras layer.
    """
    if type(layer) in (layers.Conv2D, qlayers.QuantizedConv2D):
        return LayerType.Convolutional
    if type(layer) in (layers.SeparableConv2D,
                       qlayers.QuantizedSeparableConv2D):
        return LayerType.SeparableConvolutional
    if type(layer) in (layers.Dense, qlayers.QuantizedDense):
        return LayerType.FullyConnected
    return None


def _fill_akida_layer_map(layer_ak, layers_keras, index_layer):
    """Fill Akida layer map with pooling/batchnorm/activation layers.

    This function modifies and fills the `layer_ak` map, that corresponds to
    a block of a neural layer + optional pooling/batchnorm/activation layers.
    For instance, if the `index_layer` of Keras layers (i.e.
    `layers_keras[index_layer]` is a BatchNormalization layer, the Akida layer
    map will keep this index in `layer_ak.index_batchnorm`. This is needed
    later when creating the Akida model and computing the fire thresholds and
    steps.

    Args:
        layer_ak (:obj:`LayerMapping`): the Akida layer map which will be
            filled with pooling/batchnorm/activation Keras layers.
        layers_keras (list): list of Keras layers of the model.
        index_layer (int): index of the Keras layer to read.
    """

    err_msg = ("Two {0} layers were detected related to {1}: {2} and {3}. Only "
               "one {0} layer is supported.")
    layer = layers_keras[index_layer]

    if type(layer) in (layers.MaxPooling2D, layers.GlobalAveragePooling2D):
        if layer_ak.index_pool:
            raise RuntimeError(
                err_msg.format("pooling",
                               layers_keras[layer_ak.index_neural].name,
                               layers_keras[layer_ak.index_pool].name,
                               layer.name))
        layer_ak.index_pool = index_layer
    elif (isinstance(layer, layers.BatchNormalization) or
          layer.__class__.__name__ == "BatchNormalization"):
        if layer_ak.index_batchnorm:
            raise RuntimeError(
                err_msg.format("BatchNormalization",
                               layers_keras[layer_ak.index_neural].name,
                               layers_keras[layer_ak.index_batchnorm].name,
                               layer.name))
        layer_ak.index_batchnorm = index_layer
    elif isinstance(layer, (qlayers.QuantizedActivation, layers.ReLU)):
        if layer_ak.index_activation:
            raise RuntimeError(
                err_msg.format("activation",
                               layers_keras[layer_ak.index_neural].name,
                               layers_keras[layer_ak.index_activation].name,
                               layer.name))
        layer_ak.index_activation = index_layer


def _check_flatten_layer(layers_keras, flatten_index):
    """Asserts that the Flatten layer is supported for conversion.

    A Flatten layer is supported if it is followed by a Dense layer or if it
    is the last layer of the model.

    Args:
        layers_keras (list): the model's Keras layers.
        flatten_index (int): the index of the Flatten layer in the list of
            layers.
    """

    try:
        if type(layers_keras[flatten_index + 1]) in (layers.Dense,
                                                     qlayers.QuantizedDense):
            return
    except IndexError:
        pass
    raise RuntimeError("Flatten layer only supported before a Dense one")


def _check_unsupported_activations(index_unsupported_activations,
                                   last_neural_index, layers_keras):
    """Asserts that unsupported activations are after the last Akida layer.

    Akida does not support other activations than ReLU/QuantizedActivation. The
    only exception is if an unsupported activation is placed after the last
    neural layer. For example, a Sigmoid/Softmax at the end of the model. In
    this case, the conversion is performed but the unsupported activation is
    discarded.

    Args:
        index_unsupported_activations (list): the indices of the unsupported
            activation layers.
        last_neural_index (int): the index of the last neural layer in the
            model.
        layers_keras (list): the model's Keras layers.
    """

    # Check if the unsupported activation is after the last neural layer (i.e.
    # in the last Akida layer
    for i in index_unsupported_activations:
        if i < last_neural_index:
            raise RuntimeError(
                "Activation layers other than ReLU and quantized "
                "activations are not supported before the last "
                "neural layer. Receives activation layer "
                f"'{layers_keras[i].name}' before the last neural"
                f" layer '{layers_keras[last_neural_index].name}'")

        print(f"Warning: the activation layer '{layers_keras[i].name}' "
              "will be discarded at conversion. The outputs of the Akida "
              "model will be the potentials before this activation layer.")


def generate_model_mapping(model, input_is_image):
    """Generates a model map between Keras and Akida models.

    This function returns a model map from a Keras model. The model map
    corresponds to the Akida layers mapped from the Keras layers.

    Args:
        model (tf.keras model): the model to parse.
        input_is_image (bool): True if input is an image (8-bit input with 1 or
            3 channels) followed by QuantizedConv2D. Akida model input will be
            InputConvolutional. If False, Akida model input will be InputData.

    Returns:
       :obj:`ModelMapping`: a model map corresponding to the input Keras model.

    """

    _check_layers_data_format(model)
    _check_model_input_output(model)
    layer_ak, next_layer = _map_first_layer(model, input_is_image)

    # Loop on layers
    neural_layers = (layers.Conv2D, layers.SeparableConv2D, layers.Dense,
                     qlayers.QuantizedConv2D, qlayers.QuantizedSeparableConv2D,
                     qlayers.QuantizedDense)
    ignore_list = (layers.Dropout)
    activation_list = (layers.Activation, layers.Softmax)
    layer_maps = []
    index_unsupported_activations = []

    for i in range(next_layer, len(model.layers)):
        layer = model.layers[i]
        # If this layer is a neural layer, append the current Akida layer and
        # start a new one
        if type(layer) in neural_layers:
            layer_maps.append(layer_ak)
            layer_ak = LayerMapping(_get_akida_layer_type(layer), i)
            continue

        # Pooling + batchnorm + activation layers -> update akida layer map
        if (type(layer) in (layers.MaxPooling2D, layers.GlobalAveragePooling2D,
                            layers.BatchNormalization, layers.ReLU) or
                isinstance(layer, qlayers.QuantizedActivation) or
                layer.__class__.__name__ == 'BatchNormalization'):
            _fill_akida_layer_map(layer_ak, model.layers, i)
        # Allow flatten before a dense layer
        elif isinstance(layer, layers.Flatten):
            _check_flatten_layer(model.layers, i)
        # Check Reshape compatibility
        elif isinstance(layer, layers.Reshape):
            _check_reshape_layer(layer)
        # Get unsupported activation index to check compatibility later
        elif isinstance(layer, activation_list):
            index_unsupported_activations.append(i)
        # Allow some other layers useful in keras but that will be discarded
        # or ignored during conversion
        elif isinstance(layer, ignore_list):
            continue
        else:
            # If you got here it means the layer is not recognised: raise an error.
            raise RuntimeError(f"Layer {layer.name}: unsupported type "
                               f"{layer.__class__.__name__}.")

    # Append last parsed layer if any
    layer_maps.append(layer_ak)

    _check_unsupported_activations(index_unsupported_activations,
                                   layer_maps[-1].index_neural, model.layers)

    return ModelMapping(model, layer_maps)


def _check_batchnorm_compatibility(layer_map, layers_keras):
    """Asserts BatchNormalization layer is compatible for conversion.

    Four checks are performed here:
    - BN must be applied on the last axis of the input tensor.
    - gammas must not be zero.
    - gammas must be positive if a MaxPool2D layer is placed before BN.
    - BN must be placed before the activation.

    Args:
       layer_map (:obj:`LayerMapping`): the layer map to check.
       layers_keras (list): the model's Keras layers.
    """

    layer_neural = layers_keras[layer_map.index_neural]

    if layer_map.index_batchnorm:
        # Raise error if BatchNormalization 'axis' is different from the last
        # dimension. The 'axis' parameter is a list containing the axes on what
        # the batch normalization is applied.
        layer_BN = layers_keras[layer_map.index_batchnorm]
        if (len(layer_BN.axis) != 1 or
                layer_BN.axis[0] != len(layer_BN.input_shape) - 1):
            raise RuntimeError(f"The BatchNormalization layer "
                               f"{layer_BN.name} must be applied on the "
                               f"last axis. Receives {layer_BN.axis}.")
        # Raise error if a gamma is zero.
        gammas = layer_BN.get_weights()[0]
        if (gammas == 0).any():
            raise RuntimeError(
                f"The BatchNormalization layer {layer_BN.name} has at least"
                f" one gamma equal to zero. This case is not supported.")
        # Raise error if BatchNormalization has at least one negative gamma
        # and if a MaxPool2D layer is placed before it.
        if (gammas <= 0).any() and layer_map.index_pool:
            layer_pool = layers_keras[layer_map.index_pool]
            if (isinstance(layer_pool, layers.MaxPool2D) and
                    layer_map.index_pool < layer_map.index_batchnorm):
                raise RuntimeError(
                    f"The BatchNormalization layer {layer_BN.name} has at "
                    f"least one negative gamma and a MaxPool2D layer is "
                    f"placed before it. This case is not supported.")

    # Raise error if BatchNormalization is placed after the activation
    if (layer_map.index_batchnorm and layer_map.index_activation and
            layer_map.index_batchnorm > layer_map.index_activation):
        raise RuntimeError(f"In the layer {layer_neural.name}, the batch "
                           "normalization layer must be placed before "
                           "the activation.")


def _check_pooling_compatibility(layer_map, layers_keras):
    """Asserts pooling layer is compatible for conversion.

    Two checks are performed here:
    - a global average pooling must be placed before the activation layer
    - the padding of MaxPool2D must be the same as the padding of neural layer

    Args:
       layer_map (:obj:`LayerMapping`): the layer map to check.
       layers_keras (list): the model's Keras layers.
    """

    layer_neural = layers_keras[layer_map.index_neural]

    # Raise error if GlobalAvgPool2D is placed after the activation
    if (layer_map.index_pool and layer_map.index_activation and isinstance(
            layers_keras[layer_map.index_pool], layers.GlobalAvgPool2D) and
            layer_map.index_pool > layer_map.index_activation):
        raise RuntimeError(f"In the layer {layer_neural.name}, the global "
                           "average pooling layer must be placed before "
                           "the activation.")

    # Raises error if the padding of MaxPool2D is different from the padding
    # of the neural processing layer.
    if layer_map.index_pool:
        layer_pool = layers_keras[layer_map.index_pool]
        if (isinstance(layer_pool, layers.MaxPool2D) and
                layer_neural.padding != layer_pool.padding):
            raise RuntimeError(f"Pooling layer {layer_pool.name} (padding: "
                               f"{layer_pool.padding}) must have the same "
                               f"padding as {layer_neural.name} (padding: "
                               f"{layer_neural.padding}).")


def _check_dense_compatibility(layer_map, layers_keras):
    """Asserts Dense layer is compatible for conversion.

    One check is performed here:
    - input shape must be (bs, N) or (bs, 1, 1, N) (bs is the batch size).

    Args:
       layer_map (:obj:`LayerMapping`): the layer map to check.
       layers_keras (list): the model's Keras layers.
    """

    layer_neural = layers_keras[layer_map.index_neural]

    # Raises error if Dense input shape is incorrect: supported
    # shapes are (N,) and (1, 1, N). Remember input_shape has the batch
    # size as first element of tuple.
    if isinstance(layer_neural, layers.Dense):
        valid = (  # Input shape is (N,)
            len(layer_neural.input_shape) == 2 or
            # Input shape is (1, 1, N)
            (len(layer_neural.input_shape) == 4 and
             layer_neural.input_shape[1] == 1 and
             layer_neural.input_shape[2] == 1))
        if not valid:
            raise RuntimeError("The Dense layer "
                               f"{layer_neural.name} must have an input "
                               "shape of (N,). Receives "
                               f"{layer_neural.input_shape[1:]}.")


def check_mapping_compatibility(model_map):
    """Checks whether the future model will be compatible with Akida.

    This function must mainly test the incompatibities due to the Keras layers
    and the order of the layers (parameters of the quantized layers have
    already been tested at their creation).

    Args:
        :obj:`ModelMapping`: a model map corresponding to the Keras model to
            check
    """
    layers_keras = model_map.model_keras.layers

    # Error if hidden layer without activation
    for layer_map in model_map.layer_maps[:-1]:
        if layer_map.layer_type != LayerType.InputData \
                and not layer_map.index_activation:
            raise RuntimeError("No activation layer detected with layer "
                               f"{layers_keras[layer_map.index_neural].name}. "
                               "Activation is required in hidden layers.")

    for layer_map in model_map.layer_maps:
        _check_batchnorm_compatibility(layer_map, layers_keras)
        _check_pooling_compatibility(layer_map, layers_keras)
        _check_dense_compatibility(layer_map, layers_keras)


def _check_reshape_layer(layer):
    """This function checks if the reshape layer is supported.

    In the cnn2snn conversion, a Reshape layer can only be used to transform
    a tensor of shape (N,) to a tensor of shape (1, 1, N), and vice-versa.

    Note that the 'input_shape' and 'output_shape' parameters of a layer has
    the batch size as first element:
        input_shape = (batch_size,) + input_tensor_shape
    The batch size is ignored in the following function.
    """
    in_shape = layer.input_shape
    out_shape = layer.output_shape

    valid = ((  # Reshape from (1,1,N) to (N,)
        len(in_shape) == 4 and in_shape[1] == 1 and in_shape[2] == 1 and
        len(out_shape) == 2 and out_shape[1] == in_shape[3]) or
             # Reshape from (N,) to (1,1,N)
             (len(in_shape) == 2 and len(out_shape) == 4 and
              out_shape[1] == 1 and out_shape[2] == 1 and
              out_shape[3] == in_shape[1]) or
             # Useless Reshape, from X to X
             (in_shape == out_shape))

    if not valid:
        raise RuntimeError(f"The Reshape layer {layer.name} can only be used "
                           "to transform a tensor of shape (N,) to a tensor of "
                           "shape (1, 1, N), and vice-versa. Receives "
                           f"input_shape {in_shape[1:]} and output_shape "
                           f"{out_shape[1:]}.")


def check_model_compatibility(model_keras, input_is_image=True):
    r"""Checks if a Keras model is compatible for cnn2snn conversion.

    This function doesn't convert the Keras model to an Akida model
    but only checks if the model design is compatible. The checks are performed
    at two different levels:

        1. Some checks are done when the Keras model is scanned, during the
           generation of the model map.
        2. Other checks are then done based on the model map.

    Note that this function doesn't check if the quantization bitwidths (weights
    or activations) are supported by the Akida Execution Engine or by the Akida
    NSoC.

    **1. How to build a compatible Keras quantized model?**

    The following lines give details and constraints on how to build a Keras
    model compatible for the conversion to an Akida model.


    **2. General information about layers**

    An Akida layer must be seen as a block of Keras layers starting with a
    processing layer (Conv2D, SeparableConv2D,
    Dense). All blocks of Keras layers except the last block must have
    exactly one activation layer (ReLU or ActivationDiscreteRelu). Other
    optional layers can be present in a block such as a pooling layer or a
    batch normalization layer.
    Here are all the supported Keras layers for an Akida-compatible model:

    - Processing layers:

      - tf.keras Conv2D/SeparableConv2D/Dense
      - cnn2snn QuantizedConv2D/QuantizedSeparableConv2D/QuantizedDense

    - Activation layers:

      - tf.keras ReLU
      - cnn2snn ActivationDiscreteRelu
      - any increasing activation function (only for the last block of layers)
        such as softmax, sigmoid set as last layer. This layer must derive from
        tf.keras.layers.Activation, and it will be removed during conversion to
        an Akida model.

    - Pooling layers:

      - MaxPool2D
      - GlobalAvgPool2D

    - BatchNormalization
    - Dropout
    - Flatten
    - Input
    - Reshape

    Example of a block of Keras layers::

              ----------
              | Conv2D |
              ----------
                  ||
                  \/
        ----------------------
        | BatchNormalization |
        ----------------------
                  ||
                  \/
             -------------
             | MaxPool2D |
             -------------
                  ||
                  \/
       --------------------------
       | ActivationDiscreteRelu |
       --------------------------


    **3. Constraints about inputs**

    An Akida model can accept two types of inputs: sparse events or 8-bit
    images. Whatever the input type, the Keras inputs must respect the
    following relation:

        input_akida = scale * input_keras + shift

    where the Akida inputs must be positive integers, the input scale must be
    a float value and the input shift must be an integer. In other words,
    scale * input_keras must be integers.

    Depending on the input type:

    - if the inputs are events (sparse), the first layer of the Keras model can
      be any processing layer. The input shift must be zero.
    - if the inputs are images, the first layer must be a Conv2D
      layer.


    **4. Constraints about layers' parameters**

    To be Akida-compatible, the Keras layers must observe the following rules:

    - all layers with the 'data_format' parameter must be 'channels_last'
    - all processing quantized layers and ActivationDiscreteRelu must have a
      valid quantization bitwidth
    - a Dense layer must have an input shape of (N,) or (1, 1, N)
    - a BatchNormalization layer must have 'axis' set to -1 (default)
    - a BatchNormalization layer cannot have negative gammas
    - Reshape layers can only be used to transform a tensor of shape (N,) to a
      tensor of shape (1, 1, N), and vice-versa
    - only one pooling layer can be used in each block
    - a MaxPool2D layer must have the same 'padding' as the corresponding
      processing quantized layer

    **5. Constraints about the order of layers**

    To be Akida-compatible, the order of Keras layers must observe the following
    rules:

    - a block of Keras layers must start with a processing quantized layer
    - where present, a BatchNormalization/GlobalAvgPool2D layer must be placed
      before the activation
    - a Flatten layer can only be used before a Dense layer
    - an Activation layer other than ActivationDiscreteRelu can only be used
      in the last layer


    Args:
        model (tf.keras model): the model to parse.
        input_is_image (bool, optional): True if input is an image (8-bit input
            with 1 or 3 channels) followed by QuantizedConv2D. Akida model
            input will be InputConvolutional. If False, Akida model input will
            be InputData. (Default value = True)
    """
    try:
        model_map = generate_model_mapping(model_keras, input_is_image)
        check_mapping_compatibility(model_map)
        return True
    except RuntimeError as e:
        print(
            "The Keras quantized model is not compatible for a conversion "
            "to an Akida model:\n", str(e))
        return False
