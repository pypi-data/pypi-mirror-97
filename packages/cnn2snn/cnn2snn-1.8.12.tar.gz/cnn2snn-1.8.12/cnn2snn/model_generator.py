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
"""Parsing functions that are able to generate an Akida model from a keras model.

"""
import tensorflow.keras.layers as layers
from akida import (Model, Convolutional, FullyConnected, SeparableConvolutional,
                   InputData, InputConvolutional, ConvolutionMode, PoolingType,
                   LayerType)
from . import quantization_layers as qlayers


def _get_convolution_mode(str_conv_mode):
    if str_conv_mode == 'same':
        return ConvolutionMode.Same
    return ConvolutionMode.Valid


def _parse_input_data(layer, params):
    params["input_height"] = int(layer.input_shape[1])
    params["input_width"] = int(layer.input_shape[2])
    params["input_channels"] = int(layer.input_shape[3])
    params['name'] = layer.name + "_input"


def _parse_input_conv(layer, params, input_shift):
    if not isinstance(layer, qlayers.QuantizedConv2D):
        raise TypeError(f"First layer {layer.name} must be QuantizedConv2D "
                        "when input_is_image=True. Received layer of type "
                        f"{layer.__class__.__name__}")
    params["input_height"] = int(layer.input_shape[1])
    params["input_width"] = int(layer.input_shape[2])
    params["convolution_mode"] = _get_convolution_mode(layer.padding)
    params["kernel_height"] = layer.kernel_size[0]
    params["kernel_width"] = layer.kernel_size[1]
    params["num_neurons"] = int(layer.kernel.shape[3])
    params["weights_bits"] = layer.quantizer.bitwidth
    params["input_channels"] = int(layer.input_shape[3])
    params["stride_x"] = layer.strides[1]
    params["stride_y"] = layer.strides[0]
    params["name"] = layer.name
    params["padding_value"] = int(input_shift)


def _parse_conv(layer, params):
    if not isinstance(layer, qlayers.QuantizedConv2D):
        raise TypeError(f"Layer {layer.name} was expected to be "
                        "QuantizedConv2D")
    params["convolution_mode"] = _get_convolution_mode(layer.padding)
    params["kernel_height"] = layer.kernel_size[0]
    params["kernel_width"] = layer.kernel_size[1]
    params["num_neurons"] = int(layer.kernel.shape[3])
    params["weights_bits"] = layer.quantizer.bitwidth
    params["stride_x"] = layer.strides[1]
    params["stride_y"] = layer.strides[0]
    params["name"] = layer.name


def _parse_separable_conv(layer, params):
    if not isinstance(layer, qlayers.QuantizedSeparableConv2D):
        raise TypeError(f"Layer {layer.name} was expected to be "
                        "QuantizedSeparableConv2D")
    if layer.quantizer_dw.bitwidth != layer.quantizer.bitwidth:
        raise ValueError(f"Quantized layer {layer.name} must have the same "
                         f"bitwidth for depthwise and pointwise quantizers.")
    params["convolution_mode"] = _get_convolution_mode(layer.padding)
    params["kernel_height"] = layer.kernel_size[0]
    params["kernel_width"] = layer.kernel_size[1]
    # num neurons is set to the number of filters of the depthwise
    params["num_neurons"] = int(layer.pointwise_kernel.shape[3])
    params["weights_bits"] = layer.quantizer.bitwidth
    params["stride_x"] = layer.strides[1]
    params["stride_y"] = layer.strides[0]
    params["name"] = layer.name


def _parse_dense(layer, params):
    if not isinstance(layer, qlayers.QuantizedDense):
        raise TypeError(f"Layer {layer.name} was expected to be "
                        "QuantizedDense")
    params["num_neurons"] = layer.units
    params["weights_bits"] = layer.quantizer.bitwidth
    params["name"] = layer.name


def _parse_max_pooling(layer, params):
    if not isinstance(layer, layers.MaxPooling2D):
        raise TypeError(f"Layer {layer.name} was expected to be MaxPooling2D")
    params["pooling_type"] = PoolingType.Max
    params["pooling_height"] = layer.pool_size[0]
    params["pooling_width"] = layer.pool_size[1]
    params["pooling_stride_y"] = layer.strides[0]
    params["pooling_stride_x"] = layer.strides[1]


def _parse_global_average_pooling(layer, params):
    if not isinstance(layer, layers.GlobalAveragePooling2D):
        raise TypeError(f"Layer {layer.name} was expected to be "
                        "GlobalAveragePooling2D")
    params["pooling_type"] = PoolingType.Average


def _create_akida_layer(layer_type, params):
    """Returns an Akida layer based on the input dictionary containing the
    parameters.

    """
    if layer_type == LayerType.InputData:
        layer_ak = InputData(**params)
    elif layer_type == LayerType.InputConvolutional:
        layer_ak = InputConvolutional(**params)
    elif layer_type == LayerType.Convolutional:
        layer_ak = Convolutional(**params)
    elif layer_type == LayerType.SeparableConvolutional:
        layer_ak = SeparableConvolutional(**params)
    elif layer_type == LayerType.FullyConnected:
        layer_ak = FullyConnected(**params)

    return layer_ak


def generate_model(model_map, input_scaling):
    """Generates an Akida model.

    This function creates an Akida model from the model map: for each Akida
    layer, the Keras parameters are retrieved from the neural, pooling and
    activation layers, and these parameters are then used to instantiate the
    Akida layer.
    Note that this function generates the model but doesn't set weights, fire
    thresholds and fire threshold steps.

    Notes:
        The relationship between Keras and Akida inputs is:
        input_akida = input_factor * input_keras + input_shift
        with input_scaling = (input_factor, input_shift)

    Args:
        model_map (ModelMapping): a model map with the Keras model and the list
            of layer maps.
        input_scaling (2-element tuple): the input factor and shift.

    Returns:
        :obj:`akida.Model`: the generated Akida model.

    """
    layers_keras = model_map.model_keras.layers
    _, input_shift = input_scaling

    model_ak = Model()
    for layer_map in model_map.layer_maps:
        # Get layer params
        layer_type = layer_map.layer_type
        layer = layers_keras[layer_map.index_neural]
        params = {}
        if layer_type == LayerType.InputData:
            _parse_input_data(layer, params)
        elif layer_type == LayerType.InputConvolutional:
            _parse_input_conv(layer, params, input_shift)
        elif layer_type == LayerType.Convolutional:
            _parse_conv(layer, params)
        elif layer_type == LayerType.SeparableConvolutional:
            _parse_separable_conv(layer, params)
        elif layer_type == LayerType.FullyConnected:
            _parse_dense(layer, params)

        # Add pooling params
        if layer_map.index_pool:
            pooling_layer = layers_keras[layer_map.index_pool]
            if isinstance(pooling_layer, layers.MaxPooling2D):
                _parse_max_pooling(pooling_layer, params)
            elif isinstance(pooling_layer, layers.GlobalAveragePooling2D):
                _parse_global_average_pooling(pooling_layer, params)

        # Add activation params
        if layer_map.index_activation:
            activation = layers_keras[layer_map.index_activation]
            if activation.bitwidth not in range(1, 5):
                raise ValueError("Activation bitwidth must be an integer "
                                 "between 1 and 4. Receives bitwidth "
                                 f"{activation.bitwidth} in layer "
                                 f"{activation.name}.")
            params["threshold_fire_bits"] = activation.bitwidth
        elif layer_type != LayerType.InputData:
            params["activations_enabled"] = False

        # Create layer and add it to the Akida model
        layer_ak = _create_akida_layer(layer_type, params)
        model_ak.add(layer_ak)

    return model_ak
