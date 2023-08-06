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
"""Functions to convert weights from Keras to Akida.

"""
from collections import namedtuple
import numpy as np
import tensorflow as tf
import tensorflow.keras.layers as layers
from akida import LayerType

KerasLayerParams = namedtuple('KerasLayerParams', [
    'bias', 'act_threshold', 'act_step', 'gamma_bn', 'sigma_bn', 'beta_bn',
    'mu_bn', 'global_avg_pool_factor'
])


def set_weights_thresholds(model_map, model_ak, input_scaling):
    """Converts and sets weights, fire thresholds and threshold steps to
    an Akida model from a model map.

    Args:
        model_map (ModelMapping): a model map that represents the Akida layers
            mapped to a Keras model
        model_ak (:obj:`akida.Model`): an Akida model that has been generated from the
            corresponding model map
        input_scaling (2-element tuple): the input factor and shift

    """
    layers_keras = model_map.model_keras.layers

    # Loop over the Akida layers
    current_input_scaling = input_scaling
    for i in range(len(model_map.layer_maps)):
        layer_map = model_map.layer_maps[i]
        layer_ak = model_ak.get_layer(i)

        if layer_map.layer_type == LayerType.InputData:
            continue

        # Convert and set weights
        layer_k = layers_keras[layer_map.index_neural]
        weights, weights_scale_factor = \
            convert_layer_weights(layer_map.layer_type, layer_k,
                                  layer_ak.input_dims)

        # Convert and set fire thresholds and steps
        th_fire, th_step = convert_layer_thresholds(layer_map, layers_keras,
                                                    current_input_scaling,
                                                    weights_scale_factor,
                                                    weights)

        # Handle negative BN gammas by multiplying weights and thresholds by -1
        neg_gammas = (th_step < 0)
        if np.any(neg_gammas):
            if layer_map.layer_type == LayerType.SeparableConvolutional:
                weights[1][..., neg_gammas] = -weights[1][..., neg_gammas]
            else:
                weights[..., neg_gammas] = -weights[..., neg_gammas]
            th_fire[neg_gammas] = -th_fire[neg_gammas]
            th_step[neg_gammas] = -th_step[neg_gammas]

        if layer_map.layer_type == LayerType.SeparableConvolutional:
            layer_ak.set_variable('weights', weights[0])
            layer_ak.set_variable('weights_pw', weights[1])
        else:
            layer_ak.set_variable('weights', weights)

        layer_ak.set_variable('threshold_fire', th_fire)
        layer_ak.set_variable("threshold_fire_step", th_step)
        if layer_map.index_activation:
            current_input_scaling = (1 / \
                layers_keras[layer_map.index_activation].step_height.numpy(), 0)


def convert_layer_weights(layer_type, layer_k, input_dims=None):
    """Converts weights for an Akida layer.

    This function returns the converted weights for any Akida layer,
    according to the Akida layer type and the Keras neural layer.

    Args:
        layer_type (str): type of the layer Akida.
        layer_k (:obj:`tf.keras.Layer`): the Keras layer from which the weights
            will be converted.
        input_dims (tuple): input dimensions of the Keras layer. This argument
            is only required for a fullyConnected Akida layer.

    Returns:
        tuple: the converted weights and the weights scale factor from
            quantization.

    """
    if layer_type == LayerType.InputConvolutional:
        return _convert_conv_weights(layer_k, input_conv=True)
    if layer_type == LayerType.Convolutional:
        return _convert_conv_weights(layer_k)
    if layer_type == LayerType.SeparableConvolutional:
        return _convert_separable_conv_weights(layer_k)
    if layer_type == LayerType.FullyConnected:
        return _convert_dense_weights(layer_k, input_dims)
    assert False, "The layer type is unmanaged."
    return tuple()


def _convert_conv_weights(layer, input_conv=False):
    # Quantize weights
    weights = layer.get_weights()[0]
    wq, delta = quantize_weights(layer.quantizer, weights)

    # Transpose weights to get from Keras HWCN to Akida WHCN
    # and multiply by the weights scale factor.
    wq_akida = wq.transpose((1, 0, 2, 3)) * delta
    wq_akida = np.round(wq_akida).astype(np.int8)

    # Flip W and H dimensions for conv. kernels (not input conv.)
    if not input_conv:
        wq_akida = np.flip(wq_akida, axis=[0, 1])

    return wq_akida, delta


def _convert_separable_conv_weights(layer):
    # Quantize depthwise weights
    weights = layer.get_weights()[0]
    wq_dw, delta_dw = quantize_weights(layer.quantizer_dw, weights)
    w_ak_dw = wq_dw.transpose((1, 0, 2, 3)) * delta_dw
    w_ak_dw = np.round(w_ak_dw).astype(np.int8)
    w_ak_dw = np.flip(w_ak_dw, axis=[0, 1])

    # Quantize pointwise weights
    weights_pw = layer.get_weights()[1]
    wq_pw, delta_pw = quantize_weights(layer.quantizer, weights_pw)
    # Pointwise weights in Keras have HWCN format and H = W = 1. This
    # makes the conversion to Akida's NCHW trivial.
    w_ak_pw = wq_pw * delta_pw
    w_ak_pw = np.round(w_ak_pw).astype(np.int8)

    # For separable, the weights scale factor can be seen as the product of the
    # DW and PW scale factors.
    delta = delta_dw * delta_pw
    return (w_ak_dw, w_ak_pw), delta


def _convert_dense_weights(layer, input_dims):
    # Quantize weights
    weights = layer.get_weights()[0]
    wq, delta = quantize_weights(layer.quantizer, weights)

    # retrieve input dimensions from Akida's layer
    inwidth, inheight, inchans = input_dims
    # Kernels in the fully connected are in the (HxWxC,N) format, more
    # specifically in each neuron data is laid out in the H,W,C format. In
    # Akida we expect a kernel in the (N,CxHxW,1,1), where the data in each
    # neuron is laid out in the W,H,C format as the input dimensions are
    # set.
    # So the operations done in order to obtain the akida fully connected
    # kernel are:
    # 1. reshape to H,W,C,N to split data across dimensions
    # 2. transpose dimensions to obtain C,H,W,N
    # 3. reshape to: 1,1,CxHxW,N
    #
    wq_akida = wq.reshape(inheight, inwidth, inchans, layer.units) \
        .transpose(2, 0, 1, 3) \
        .reshape(1, 1, inchans * inheight * inwidth, layer.units)
    # Multiply by delta, round and cast to int
    wq_akida = wq_akida * delta
    wq_akida = np.round(wq_akida).astype(np.int8)

    return wq_akida, delta


def _prepare_threshold_calculations(layer_map, layers_keras):
    """Retrieves required variables to calculate Akida fire threshold and
    step.

    This function returns a dictionary with variables required for threshold
    calculations of the given Akida layer map: bias in the Keras neural layer,
    parameters of the activation layer, batch norm parameters and global
    average pooling factor.

    Args:
        layer_map (LayerMapping): the given Akida layer map.
        layers_keras: the list of Keras layers (tf.keras.model.layers)
            corresponding to the given layer map.

    Returns:
        dict: required variables to calculate Akida fire threshold and step.
    """

    layer_neural = layers_keras[layer_map.index_neural]

    # Initialize variables to their default values
    threshold_shape = layer_neural.output_shape[-1]
    bias = np.zeros(threshold_shape)
    thresh_keras = np.zeros(threshold_shape)
    step_keras = np.ones(threshold_shape)
    gamma_bn = np.ones(threshold_shape)
    sigma_bn = np.ones(threshold_shape)
    beta_bn = np.zeros(threshold_shape)
    mu_bn = np.zeros(threshold_shape)
    global_avg_pool_factor = 1

    # Get bias if present
    if layer_neural.use_bias:
        if layer_map.layer_type == LayerType.SeparableConvolutional:
            bias = layer_neural.get_weights()[2]
        else:
            bias = layer_neural.get_weights()[1]

    # Get parameters from the discrete ReLU activation (threshold and step)
    if layer_map.index_activation:
        act_layer = layers_keras[layer_map.index_activation]
        thresh_keras = act_layer.threshold.numpy() * np.ones(threshold_shape)
        step_keras = (act_layer.step_width.numpy() * 2.**act_layer.bitwidth /
                      16) * np.ones(threshold_shape)

    # Get batchnorm parameters
    if layer_map.index_batchnorm:
        (gamma_bn, beta_bn, mu_bn,
         var_bn) = layers_keras[layer_map.index_batchnorm].get_weights()
        sigma_bn = np.sqrt(var_bn +
                           layers_keras[layer_map.index_batchnorm].epsilon)

    # Get global average pooling factor
    if layer_map.index_pool and isinstance(layers_keras[layer_map.index_pool],
                                           layers.GlobalAveragePooling2D):
        global_avg_pool_factor = np.prod(
            layers_keras[layer_map.index_pool].input_shape[1:3])

    return KerasLayerParams(bias, thresh_keras, step_keras, gamma_bn, sigma_bn,
                            beta_bn, mu_bn, global_avg_pool_factor)


def convert_layer_thresholds(layer_map, layers_keras, input_scaling,
                             weights_scale_factor, weights_ak):
    """Returns the fire thresholds and threshold steps for a given Akida layer.

    This function computes the fire thresholds and steps for a given Akida layer
    (defined by the layer map) from the corresponding Keras layers. Other
    arguments are required to compute these variables.

    Args:
        layer_map (LayerMapping): the given Akida layer map
        layers_keras: the list of Keras layers (tf.keras.model.layers)
            corresponding to the given layer map
        input_scaling (2-element tuple): the input scaling of the current layer.
        weights_scale_factor (float): the weights scale factor of the current
            Akida layer. This is given by the 'convert_layer_weights' function.
        weights_ak (np.ndarray): the Akida weights of the current Akida layer.

    Returns:
        tuple: the fire thresholds and steps.

    """

    input_scale, input_shift = input_scaling
    p = _prepare_threshold_calculations(layer_map, layers_keras)

    # Compute threshold fires and steps
    th_fire = (input_scale * weights_scale_factor *
               (p.sigma_bn / p.gamma_bn *
                (p.act_threshold - p.beta_bn) + p.mu_bn - p.bias))
    th_step = (input_scale * weights_scale_factor * p.sigma_bn / p.gamma_bn *
               p.act_step).astype(np.float32)

    # If there is an InputConv layer, update th_fire with input shift
    if layer_map.layer_type == LayerType.InputConvolutional:
        th_fire += np.sum(weights_ak, axis=(0, 1, 2)) * input_shift

    th_fire *= p.global_avg_pool_factor
    th_step *= p.global_avg_pool_factor

    th_fire = np.floor(th_fire).astype(np.int32)

    return th_fire, th_step


def quantize_weights(quantizer, w):
    """Returns quantized weights and delta as numpy arrays.

    Internally, it uses a tf.function that wraps calls to the quantizer in
    a graph, allowing the weights to be quantized eagerly.

    Args:
        quantizer (:obj:`WeightQuantizer`): the quantizer object.
        w (:obj:`np.ndarray`): the weights to quantize.

    Retruns:
        :obj:`np.ndarray`: the quantized weights `np.ndarray` and the scale
            factor scalar.

    """

    w_tf = tf.constant(w)
    wq = quantizer.quantize(w_tf)
    scale_factor = quantizer.scale_factor(w_tf)
    return wq.numpy(), scale_factor.numpy()
