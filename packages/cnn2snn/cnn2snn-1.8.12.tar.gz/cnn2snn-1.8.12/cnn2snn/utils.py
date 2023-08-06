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
"""
A set of functions to convert a Keras (tf.keras) model to a new
equivalent model with different characteristics. Then, the new model
can be quantized.

"""
from tensorflow.keras.layers import (InputLayer, Conv2D, SeparableConv2D, Dense,
                                     MaxPool2D, GlobalAveragePooling2D,
                                     BatchNormalization)
from tensorflow.keras.models import (Model, load_model, model_from_json,
                                     clone_model)
from .quantization_layers import (QuantizedConv2D, QuantizedDepthwiseConv2D,
                                  QuantizedSeparableConv2D, QuantizedDense)
from .transforms.sequential import compute_BN_folded_weights
from .cnn2snn_objects import cnn2snn_objects


def invert_batchnorm_pooling(model):
    """Returns a new model where pooling and batchnorm layers are inverted.
    From a Keras model where pooling layers precede batch normalization
    layers, this function places the BN layers before pooling layers. This
    is the first step before folding BN layers into neural layers.
    Note: inversion of layers is equivalent only if the gammas of BN layers
    are positive. The function raises an error if not.

    Args:
        model (:obj:`tf.keras.Model`): a tf.keras model.
    Returns:
        :obj:`tf.keras.Model`: a keras.Model.
    """

    # Maps between successive pooling->batchnorm layers. These pairs will be
    # inverted when cloning the model.
    pool2bn_map = {}
    bn2pool_map = {}

    for layer in model.layers:
        # We map BatchNormalization layers that have only one inbound layer
        # being a MaxPool2D or GlobalAveragePooling2D.
        if (isinstance(layer, BatchNormalization) and
                len(layer.inbound_nodes) == 1 and
                isinstance(layer.inbound_nodes[0].inbound_layers,
                           (MaxPool2D, GlobalAveragePooling2D))):
            bn2pool_map[layer] = layer.inbound_nodes[0].inbound_layers
            pool2bn_map[layer.inbound_nodes[0].inbound_layers] = layer

    def replace_layer(layer):
        if layer in pool2bn_map:
            # Replace pooling layer with the corresponding BN layer
            layer_bn = pool2bn_map[layer]
            config_bn = layer_bn.get_config()
            if isinstance(layer, GlobalAveragePooling2D):
                config_bn['axis'] = [-1]
            return layer_bn.__class__.from_config(config_bn)
        if layer in bn2pool_map:
            # Replace BN layer with the corresponding pooling layer
            layer_pool = bn2pool_map[layer]
            return layer_pool.__class__.from_config(layer_pool.get_config())
        return layer.__class__.from_config(layer.get_config())

    new_model = clone_model(model, clone_function=replace_layer)

    for layer in model.layers:
        new_model.get_layer(layer.name).set_weights(layer.get_weights())

    return new_model


def fold_batch_norms(model):
    """Returns a new model where batchnorm layers are folded into
    previous neural layers.

    From a Keras model where BN layers follow neural layers, this
    function removes the BN layers and updates weights and bias
    accordingly of the preceding neural layers. The new model is
    strictly equivalent to the previous one.

    Args:
        model (:obj:`tf.keras.Model`): a Keras model.
    Returns:
        :obj:`tf.keras.Model`: a tf.keras.Model.
    """

    # Copy model in order to modify before cloning.
    model_copy = clone_model(model)
    model_copy.set_weights(model.get_weights())

    # Get BN layers to fold, mapping with the preceding neural layer and the
    # following layer if present.
    map_neural_layer_to_bn, map_bn_to_next_layer = _find_batchnorms_to_fold(
        model_copy)

    # Update model before cloning: remove BN layers, update inbound nodes and
    # output layers
    _prepare_model_to_fold_BN(model_copy, map_neural_layer_to_bn,
                              map_bn_to_next_layer)

    # Clone model (BN layers will disappear)
    def replace_layer(layer):
        config = layer.get_config()
        # Set use_bias=True in neural layers where BN layers are folded, to
        # accept new computed weights
        if layer in map_neural_layer_to_bn:
            config['use_bias'] = True
        return layer.__class__.from_config(config)

    model_foldBN = clone_model(model_copy, clone_function=replace_layer)

    # Set weights in the new model
    for layer in model_copy.layers:
        if layer not in map_neural_layer_to_bn:
            model_foldBN.get_layer(layer.name).set_weights(layer.get_weights())
        else:
            # Set new weights
            layer_bn = map_neural_layer_to_bn[layer]
            new_weights = compute_BN_folded_weights(layer, layer_bn)[0]
            model_foldBN.get_layer(layer.name).set_weights(new_weights)

    return model_foldBN


def _find_batchnorms_to_fold(model):
    """Detect BatchNormalization layers that can be folded.

    We limit to BN layers that follow supported neural layer types. Moreover,
    we only fold BN layers with one inbound/outbound node, in order to avoid
    layers with multiple nodes (e.g. layers used multiple times in the model
    or in other models).

    The function returns two maps (dict):
    - one between the neural layer and its BN layer to be folded
    - one between the BN layer and its following layer (it if exists)

    """

    supported_layers = (Conv2D, SeparableConv2D, Dense, QuantizedConv2D,
                        QuantizedSeparableConv2D, QuantizedDense)

    # Map between a neural layer and its following BN layer, and map between
    # the BN layer and its next layer.
    map_neural_layer_to_bn = {}
    map_bn_to_next_layer = {}

    # Find triplet "neural layer -> BN -> next layer"
    for layer in model.layers:
        # Find a neural layer followed by a BN layer
        if (type(layer) in supported_layers and
                len(layer.outbound_nodes) == 1 and
                isinstance(layer.outbound_nodes[0].layer, BatchNormalization)):

            layer_bn = layer.outbound_nodes[0].layer
            # To be folded, BN layer must have only one inbound node and
            # no more than one outbound node.
            bn_outbounds = layer_bn.outbound_nodes
            if (len(layer_bn.inbound_nodes) != 1 or len(bn_outbounds) > 1):
                continue

            map_neural_layer_to_bn[layer] = layer_bn
            if len(bn_outbounds) == 1:
                map_bn_to_next_layer[layer_bn] = bn_outbounds[0].layer

    return map_neural_layer_to_bn, map_bn_to_next_layer


def _prepare_model_to_fold_BN(model, map_neural_layer_to_bn,
                              map_bn_to_next_layer):
    """Prepare model to be cloned with folded BatchNormalization layers.

    To fold BN layers by using "clone_model", the model must be prepared by
    modifying some internal variables, such as _layers, _output_layers or
    _inbound_nodes.

    Three operations are done here:
    1. Remove BN layers from model.layers.
    2. Bypass BN layers in the graph by updating inbound nodes of the layers
       following the BN layers. The new inbound nodes are the neural layers
       preceding the BN layers.
    3. If a BN layer is an output layer of the model, the preceding neural
       layer must be added to the new output layers.

    The model instance and the layers are directly modified in this function.
    """

    # Remove BN layers from model.layers.
    for layer_bn in map_neural_layer_to_bn.values():
        model._layers.remove(layer_bn)  # pylint: disable=protected-access

    # Update inbound nodes as there is no BN between neural layer and
    # following layer. Inbound nodes are used in "clone_layer" function to
    # create the model architecture. Here, we replace the inbound node of the
    # next layer with the inbound node of the BN layer, in order to bypass the
    # BN layer.
    for layer_bn, next_layer in map_bn_to_next_layer.items():
        # pylint: disable=protected-access
        node = layer_bn.outbound_nodes[0]
        node_index = next_layer._inbound_nodes.index(node)
        next_layer._inbound_nodes[node_index] = layer_bn.inbound_nodes[0]

    # If BN layer is an output layer, replace it with its
    # inbound layer
    for neural_layer, layer_bn in map_neural_layer_to_bn.items():
        # pylint: disable=protected-access
        if layer_bn in model._output_layers:
            # Replace BN layer in _output_layers and _output_coordinates
            index_bn = model._output_layers.index(layer_bn)
            model._output_layers[index_bn] = neural_layer
            model._output_coordinates[index_bn] = (neural_layer, 0, 0)


def merge_separable_conv(model):
    """Returns a new model where all depthwise conv2d layers followed by conv2d
    layers are merged into single separable conv layers.

    The new model is strictly equivalent to the previous one.

    Args:
        model (:obj:`tf.keras.Model`): a Keras model.

    Returns:
        :obj:`tf.keras.Model`: a tf.keras.Model.

    """
    # If no layers are Depthwise, there is nothing to be done, return.
    if not any([isinstance(l, QuantizedDepthwiseConv2D) for l in model.layers]):
        return model

    if isinstance(model.layers[0], InputLayer):
        x = model.layers[0].output
        i = 1
    else:
        x = model.layers[0].input
        i = 0
    while i < len(model.layers) - 1:
        layer = model.layers[i]
        next_layer = model.layers[i + 1]

        if isinstance(layer, QuantizedDepthwiseConv2D):
            # Check layers expected order
            if not isinstance(next_layer, QuantizedConv2D):
                raise AttributeError(f"Layer {layer.name} "
                                     "QuantizedDepthwiseConv2D should be "
                                     "followed by QuantizedConv2D layers.")

            if layer.bias is not None:
                raise AttributeError("Unsupported bias in "
                                     "QuantizedDepthwiseConv2D Layer "
                                     f"{layer.name} ")

            # Get weights and prepare new ones
            dw_weights = layer.get_weights()[0]
            pw_weights = next_layer.get_weights()[0]
            new_weights = [dw_weights, pw_weights]
            if next_layer.use_bias:
                bias = next_layer.get_weights()[1]
                new_weights.append(bias)

            # Create new layer
            new_name = f'{layer.name}_{next_layer.name}'
            new_layer = QuantizedSeparableConv2D(next_layer.filters,
                                                 layer.kernel_size,
                                                 quantizer_dw=layer.quantizer,
                                                 quantizer=layer.quantizer,
                                                 padding=layer.padding,
                                                 use_bias=next_layer.use_bias,
                                                 name=new_name)
            x = new_layer(x)
            new_layer.set_weights(new_weights)
            i = i + 2

        else:
            x = chain_cloned_layer(x, layer)
            i = i + 1

    # Add last layer if not done already
    if i == (len(model.layers) - 1):
        if isinstance(model.layers[-1], QuantizedDepthwiseConv2D):
            raise AttributeError(f"Layer {layer.name} "
                                 "QuantizedDepthwiseConv2D should be followed "
                                 "by QuantizedConv2D layers.")
        x = model.layers[-1](x)

    return Model(inputs=model.input, outputs=[x], name=model.name)


def load_quantized_model(filepath, custom_objects=None, compile_model=True):
    """Loads a quantized model saved in TF or HDF5 format.

    If the model was compiled and trained before saving, its training state
    will be loaded as well.
    This function is a wrapper of `tf.keras.models.load_model`.

    Args:
        filepath (string): path to the saved model.
        custom_objects (dict): optional dictionary mapping names (strings) to
            custom classes or functions to be considered during deserialization.
        compile_model (bool): whether to compile the model after loading.

    Returns:
        :obj:`tensorflow.keras.Model`: a Keras model instance.
    """
    if custom_objects is None:
        custom_objects = {}
    all_objects = {**custom_objects, **cnn2snn_objects}
    return load_model(filepath, all_objects, compile_model)


def load_partial_weights(dest_model, src_model):
    """Loads a subset of weights from one Keras model to another

    This goes through each layers of the source model, looking for a matching
    layer in the destination model.
    If a layer with the same name is found, then this method assumes that one
    of the two layer has the same set of weights as the other plus some extra
    weights at the end, and loads only the first common weights into the
    destination layer.

    Args:
        dest_model(:obj:`tensorflow.keras.Model`): the destination Model
        src_model(:obj:`tensorflow.keras.Model`): the source Model

    """
    for src_layer in src_model.layers:
        src_weights = src_layer.get_weights()
        dest_layer = dest_model.get_layer(src_layer.name)
        dest_weights = dest_layer.get_weights()
        # Take the minimum of the two lists of weights
        n_weights = min(len(src_weights), len(dest_weights))
        # Only replace the first weights
        dest_weights[0:n_weights] = src_weights[0:n_weights]
        dest_layer.set_weights(dest_weights)


def create_trainable_quantizer_model(quantized_model):
    """Converts a legacy quantized model to a model using trainable quantizers.

    Legacy cnn2snn models have fixed quantization schemes. This method converts
    such a model to an equivalent model using trainable quantizers.

    Args:
        quantized_model(str, :obj:`tensorflow.keras.Model`): a keras Model or a
        path to a keras Model file

    Returns:
        :obj:`tensorflow.keras.Model`: a Keras Model instance.
    """
    if isinstance(quantized_model, str):
        # Load the model at the specified path
        quantized_model = load_quantized_model(quantized_model)
    # Dump model configuration in a JSON string
    json_string = quantized_model.to_json()
    # Edit the model configuration to replace static quantizers by trainable
    # ones
    json_string = json_string.replace("StdWeightQuantizer",
                                      "TrainableStdWeightQuantizer")
    json_string = json_string.replace("ActivationDiscreteRelu", "QuantizedReLU")
    # Create a new model from the modified configuration
    new_model = model_from_json(json_string, custom_objects=cnn2snn_objects)
    # Transfer weights to the new model
    load_partial_weights(new_model, quantized_model)
    return new_model


def chain_cloned_layer(x, layer):
    """This function creates a hard copy of a layer and apply to it the
    tf.Tensor x.

    """

    config = layer.get_config()
    w = layer.get_weights()
    new_layer = type(layer).from_config(config)
    out = new_layer(x)
    new_layer.set_weights(w)
    return out
