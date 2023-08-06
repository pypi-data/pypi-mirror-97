#!/usr/bin/env python
# ******************************************************************************
# Copyright 2021 Brainchip Holdings Ltd.
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
"""Transformation utilities for Keras/CNN2SNN Sequential models.

These transformations are designed for a specific stage in the CNN2SNN
conversion workflow. They must not be used as a generic tool to transform any
Sequential models.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras import Model, Sequential, Input
from tensorflow.keras.layers import (Conv2D, SeparableConv2D, Dense, MaxPool2D,
                                     GlobalAvgPool2D, ReLU, BatchNormalization,
                                     Dropout, Concatenate, InputLayer)

from ..cnn2snn_objects import cnn2snn_objects
from ..quantization_ops import ScaleFactorQuantizer
from ..quantization_layers import (QuantizedConv2D, QuantizedSeparableConv2D,
                                   QuantizedDense, QuantizedActivation)


def _clone_layer(layer):
    return layer.__class__.from_config(layer.get_config())


def _clone_layer_and_add_to_model(layer, model):
    layer_clone = _clone_layer(layer)
    model.add(layer_clone)
    layer_clone.set_weights(layer.get_weights())
    return layer_clone


def sequential_remove_useless_layers(model):
    """Removes useless layers in a Sequential model.

    Useless layers are:
    - Dropout

    Args:
        model (:obj:`tf.keras.Model`): a Sequential Keras model.
    Returns:
        :obj:`tf.keras.Model`: a Sequential Keras model.
    """

    _raise_error_if_model_not_sequential(model)

    useless_layers = (Dropout,)

    new_model = Sequential()
    new_model.add(Input(model.input_shape[1:]))
    for layer in model.layers:
        if isinstance(layer, useless_layers):
            continue
        _clone_layer_and_add_to_model(layer, new_model)

    return new_model


def sequential_invert_pooling_activation(model):
    """Invert activation and MaxPool2D layer in a Sequential model to have
    MaxPool2D before the activation.

    Having activation->MaxPool2D or MaxPool2D->activation is equivalent only if
    the activation is increasing (ok for ReLU and QuantizedActivation).
    Note that GlobalAvgPool2D cannot be inverted with an activation because
    there is no equivalence between activation->GAP and GAP->activation.

    Args:
        model (:obj:`tf.keras.Model`): a Sequential Keras model.
    Returns:
        :obj:`tf.keras.Model`: a Sequential Keras model.
    """

    _raise_error_if_model_not_sequential(model)

    new_model = Sequential()
    new_model.add(Input(model.input_shape[1:]))
    i = 0
    while i < len(model.layers) - 1:
        layer = model.layers[i]
        next_layer = model.layers[i + 1]
        if (isinstance(layer, (ReLU, QuantizedActivation)) and
                isinstance(next_layer, MaxPool2D)):
            _clone_layer_and_add_to_model(next_layer, new_model)
            _clone_layer_and_add_to_model(layer, new_model)
            i = i + 2
        else:
            _clone_layer_and_add_to_model(layer, new_model)
            i = i + 1

    if i < len(model.layers):
        _clone_layer_and_add_to_model(model.layers[-1], new_model)

    return new_model


def sequential_invert_batchnorm_pooling(model):
    """Inverts pooling and BatchNormalization layers in a Sequential model to
    have BN layer before pooling.

    Having pool->BN or BN->pool is equivalent only if BN layer has no negative
    gammas.

    Args:
        model (:obj:`tf.keras.Model`): a Sequential Keras model.
    Returns:
        :obj:`tf.keras.Model`: a Sequential Keras model.
    """

    _raise_error_if_model_not_sequential(model)

    new_model = Sequential()
    new_model.add(Input(model.input_shape[1:]))
    i = 0
    while i < len(model.layers) - 1:
        layer = model.layers[i]
        next_layer = model.layers[i + 1]
        if (isinstance(layer, (MaxPool2D, GlobalAvgPool2D)) and
                isinstance(next_layer, BatchNormalization)):
            gammas = next_layer.get_weights()[0]
            if np.any(gammas <= 0):
                # NB: negative gammas are only a problem for max pooling, not
                # for avg pooling
                raise RuntimeError(f"There are {np.sum(gammas <= 0)} negative "
                                   "gammas in the batch norm layer "
                                   f"{next_layer.name}. Negative gammas are "
                                   "not supported.")
            # GlobalAveragePooling2D brings a change on axis for the batch norm.
            if isinstance(layer, GlobalAvgPool2D):
                bn_config = next_layer.get_config()
                bn_config['axis'] = [-1]
                bn_layer_clone = BatchNormalization.from_config(bn_config)
            else:
                bn_layer_clone = _clone_layer(next_layer)
            new_model.add(bn_layer_clone)
            bn_layer_clone.set_weights(next_layer.get_weights())
            _clone_layer_and_add_to_model(layer, new_model)
            i = i + 2
        else:
            _clone_layer_and_add_to_model(layer, new_model)
            i = i + 1

    if i < len(model.layers):
        _clone_layer_and_add_to_model(model.layers[-1], new_model)

    return new_model


def sequential_freeze_quantizers(model):
    """Freezes weight quantizers in quantized neural layers.

    Freezing weight quantizers consists in replacing any quantizer with a
    custom quantizer that directly stores the scale factors, instead of
    computing them depending on the weights. After freezing quantizers,
    the neural weights must not be modified anymore.
    Doing this allows to prepare any model for BatchNormalization folding,
    which is not compatible with all quantizers.

    Note that this operation is irreversible and must only be used in the
    conversion workflow.
    """

    _raise_error_if_model_not_sequential(model)

    neural_quantized_layers = (QuantizedConv2D, QuantizedSeparableConv2D,
                               QuantizedDense)

    new_model = Sequential()
    new_model.add(Input(model.input_shape[1:]))
    for layer in model.layers:
        layer_clone = _clone_layer_and_add_to_model(layer, new_model)
        if type(layer) in neural_quantized_layers:
            # Get bitwidth and weights scale factors
            bitwidth = layer.quantizer.bitwidth
            shift_for_sepconv = isinstance(layer, QuantizedSeparableConv2D)
            w = layer.get_weights()[0 + shift_for_sepconv]
            scale_factors = layer.quantizer.scale_factor(tf.constant(w))

            # Freeze quantizer by replacing with ScaleFactorQuantizer
            layer_clone.quantizer = ScaleFactorQuantizer(
                bitwidth, scale_factors)

    return new_model


def sequential_fold_BN(model):
    """Folds BatchNormalization layers into the preceding neural layers of
    a Sequential model.

    Args:
        model (:obj:`tf.keras.Model`): a Sequential Keras model.
    Returns:
        :obj:`tf.keras.Model`: a Sequential Keras model.
    """

    _raise_error_if_model_not_sequential(model)

    neural_layers = (Conv2D, SeparableConv2D, Dense, QuantizedConv2D,
                     QuantizedSeparableConv2D, QuantizedDense)

    new_model = Sequential()
    new_model.add(Input(model.input_shape[1:]))
    i = 0
    while i < len(model.layers) - 1:
        layer = model.layers[i]
        next_layer = model.layers[i + 1]
        if (isinstance(layer, neural_layers) and
                isinstance(next_layer, BatchNormalization)):

            # Add new neural layer with bias
            config = layer.get_config()
            config['use_bias'] = True
            new_layer = layer.__class__.from_config(config)
            new_model.add(new_layer)
            new_weights, scale_BN = compute_BN_folded_weights(layer, next_layer)
            new_layer.set_weights(new_weights)

            # If the quantizer is ScaleFactorQuantizer, we must also update
            # the scale factors with the factor introduced by the BN
            if (hasattr(new_layer, 'quantizer') and
                    isinstance(new_layer.quantizer, ScaleFactorQuantizer)):
                new_layer.quantizer.scale_factors /= scale_BN
            i = i + 2
        else:
            _clone_layer_and_add_to_model(layer, new_model)
            i = i + 1

    if i < len(model.layers):
        _clone_layer_and_add_to_model(model.layers[-1], new_model)

    return new_model


def compute_BN_folded_weights(neural_layer, bn_layer):
    """Computes the new weights of a neural layer after folding BN layer.

    Args:
        neural_layer (:obj:`tf.keras.Layer`): a neural layer where BN will be
            folded.
        bn_layer (:obj:`tf.keras.Layer`): the BatchNormalization layer to fold
            into the neural layer.
    Returns:
        list: a list of the new weights to set in the new folded neural layer.
        list: a list of scale factors introduced by the folding.

    """

    # Get kernel and bias weights of the neural layer
    if type(neural_layer) in (SeparableConv2D, QuantizedSeparableConv2D):
        kernel_position = 1
        bias_position = 2
    else:
        kernel_position = 0
        bias_position = 1
    weights = neural_layer.get_weights()
    kernel = weights[kernel_position]
    bias = weights[bias_position] if neural_layer.use_bias else 0

    # Get BN weights
    gamma, beta, mean, var = bn_layer.get_weights()
    scale_BN = gamma / np.sqrt(var + bn_layer.epsilon)

    # Compute new folded kernel and bias
    new_kernel = kernel * scale_BN
    new_bias = beta + (bias - mean) * scale_BN

    # Return all weights with modified ones
    new_weights = weights
    new_weights[kernel_position] = new_kernel
    if neural_layer.use_bias:
        new_weights[bias_position] = new_bias
    else:
        new_weights.insert(bias_position, new_bias)

    return new_weights, scale_BN


def _clone_model_with_weights(model):
    """Clones the model and copy weights into the cloned model.

    The cloned model is identical to the input model, but cloning removes the
    shared layers that can cause problems at inference.

    Args:
        model (:obj:`tf.keras.Model`): a Sequential Keras model.
    Returns:
        :obj:`tf.keras.Model`: a Sequential Keras model.
    """

    with tf.keras.utils.custom_object_scope(cnn2snn_objects):
        model_clone = tf.keras.models.clone_model(model)
    model_clone.set_weights(model.get_weights())
    return model_clone


def _raise_error_if_model_not_sequential(model):
    """Raises a ValueError if model is not a Sequential Keras model.
    """
    if not isinstance(model, Sequential):
        raise ValueError(f"Model is expected to be Sequential. Receives type "
                         f"{model.__class__.__name__}.")


def cut_model_to_sequentials(model):
    """Cut a Keras model into Sequential sub-models and Concatenate layers.

    This function returns an equivalent model where all linear branches are
    replaced by a Sequential sub-model.

    Args:
        model (:obj:`tf.keras.Model`): a Keras model

    Returns:
        :obj:`tf.keras.Model`: a Keras model with Sequential sub-models
    """

    # Clone model to avoid shared layers
    model_clone = _clone_model_with_weights(model)

    if isinstance(model_clone, Sequential):
        return model_clone

    def parse_layer(layer, visited_layers, current_branch, output_tensors):
        """Go through a TensorFlow/Keras graph by recursively looking at
        outbound layers.

        Each linear branch is detected and converted to a Sequential sub-model.
        A linear branch ends if:
          - the current layer has multiple outbounds (split connections)
          - the current layer has no outbound (output layer of the model)
          - the next layer is a Concatenate layer
        """

        if layer in visited_layers:
            raise RuntimeError(f"Layer {layer.name} already visited.")

        # Do not visit this layer if all inbound layers were not visited yet
        # (e.g. for Concatenate inbounds)
        inbound_layers = [n.layer for n in layer.inbound_nodes[0].parent_nodes]
        if set(inbound_layers).difference(visited_layers):
            return
        visited_layers.append(layer)

        # Add layer to graph if layer is Concatenate
        if isinstance(layer, Concatenate):
            # Get input tensors of Concatenate layer
            concat_input_tensors = [output_tensors[l] for l in inbound_layers]
            # Add Concatenate layer to the graph
            output_tensors[layer] = layer(concat_input_tensors)

        else:
            # Add current layer to current branch
            current_branch.append(layer)

            # End current branch and add it to the graph if:
            # - current layer has multiple outbounds (split connections)
            # - current layer has no outbound (output layer of the model)
            # - next layer is Concatenate
            if (len(layer.outbound_nodes) != 1 or
                    isinstance(layer.outbound_nodes[0].layer, Concatenate)):

                parent_nodes = current_branch[0].inbound_nodes[0].parent_nodes
                if parent_nodes:  # Get input tensor of current branch
                    input_tensor = output_tensors[parent_nodes[0].layer]
                else:  # If branch is the first one, there is no input branch
                    input_tensor = current_branch[0].input

                # Create sub-model for current branch and add it to the graph
                submodel = Sequential(current_branch)
                output_tensors[layer] = submodel(input_tensor)
                current_branch.clear()

        # Go to next layer
        for next_layer in [node.layer for node in layer.outbound_nodes]:
            parse_layer(next_layer, visited_layers, current_branch,
                        output_tensors)

    # Go through model layers to detect Sequential branches
    input_layer = model_clone.get_layer(model_clone.input_names[0])
    output_layer = model_clone.get_layer(model_clone.output_names[0])
    output_tensors = {}
    parse_layer(input_layer,
                visited_layers=[],
                current_branch=[],
                output_tensors=output_tensors)

    # Create new model with Sequential sub-models
    model_cut = Model(model_clone.input, output_tensors[output_layer])

    # Clone model to avoid shared layers
    model_cut = _clone_model_with_weights(model_cut)

    return model_cut


def transform_submodels(model):
    """Transforms all Sequential submodels of a functional model.

    The input model must be composed of Sequential submodels and Concatenate
    layers. This function will apply transformations on every Sequential
    submodel and returns an equivalent functional model with transformed
    submodels.

    Args:
        model (:obj:`tf.keras.Model`): a Keras model with Sequential submodels.

    Returns:
        :obj:`tf.keras.Model`: a Keras model with transformed Sequential
            submodels.
    """

    def transform_sequential(submodel):
        submodel = sequential_remove_useless_layers(submodel)
        submodel = sequential_invert_pooling_activation(submodel)
        submodel = sequential_invert_batchnorm_pooling(submodel)
        submodel = sequential_freeze_quantizers(submodel)
        submodel = sequential_fold_BN(submodel)
        return submodel

    if isinstance(model, Sequential):
        return transform_sequential(model)

    def parse_submodel(layer, visited_layers, output_tensors):
        if layer in visited_layers:
            raise RuntimeError(f"Layer {layer.name} already visited.")

        # Do not visit this layer if all inbound layers were not visited yet
        # (e.g. for Concatenate inbounds)
        inbound_layers = [n.layer for n in layer.inbound_nodes[0].parent_nodes]
        if set(inbound_layers).difference(visited_layers):
            return
        visited_layers.append(layer)

        # Add layer to graph if layer is InputLayer or Concatenate
        if isinstance(layer, InputLayer):
            input_clone = _clone_layer(layer)
            output_tensors[layer] = input_clone.output
        elif isinstance(layer, Concatenate):
            # Get input tensors of Concatenate layer
            concat_input_tensors = [output_tensors[l] for l in inbound_layers]
            # Add Concatenate layer to the graph
            concat_clone = _clone_layer(layer)
            output_tensors[layer] = concat_clone(concat_input_tensors)
        elif isinstance(layer, Sequential):
            # Get input tensors of submodel
            parent_nodes = layer.inbound_nodes[0].parent_nodes
            input_tensor = output_tensors[parent_nodes[0].layer]
            # Transform submodel and add it to the graph
            new_submodel = transform_sequential(layer)
            output_tensors[layer] = new_submodel(input_tensor)
        else:
            raise RuntimeError(f"Layer {layer.name} of type "
                               f"{layer.__class__.__name__} is not supported "
                               f"here.")

        # Go to next layer
        for next_layer in [node.layer for node in layer.outbound_nodes]:
            parse_submodel(next_layer, visited_layers, output_tensors)

    # Go through model layers to transform Sequential branches
    input_layer = model.get_layer(model.input_names[0])
    output_tensors = {}
    parse_submodel(input_layer,
                   visited_layers=[],
                   output_tensors=output_tensors)

    # Create new model with transformed Sequential sub-models
    output_layer = model.get_layer(model.output_names[0])
    return Model(output_tensors[input_layer], output_tensors[output_layer])
