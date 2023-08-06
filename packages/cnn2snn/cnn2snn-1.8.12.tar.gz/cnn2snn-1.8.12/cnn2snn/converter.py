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
"""Conversion of a Keras/CNN2SNN model into an Akida model"""

import os
import tensorflow as tf
from . import utils
from .mapping_generator import generate_model_mapping, check_mapping_compatibility
from .model_generator import generate_model
from .weights_ops import set_weights_thresholds


def convert(model, file_path=None, input_scaling=None, input_is_image=True):
    """Converts a Keras quantized model to an Akida one.

    After quantizing a Keras model with :func:`cnn2snn.quantize`, it can be
    converted to an Akida model. By default, the conversion expects that the
    Akida model takes 8-bit images as inputs. ``input_scaling`` defines how the
    images have been rescaled to be fed into the Keras model (see note below).

    If inputs are spikes, you can set ``input_is_image=False``. In this case,
    Akida inputs are then expected to be integers between 0 and 15.

    Note:
        The relationship between Keras and Akida inputs is defined as::

            input_akida = input_scaling[0] * input_keras + input_scaling[1].

        If a :class:`tf.keras.layers.experimental.preprocessing.Rescaling`
        layer is present as first layer of the model, ``input_scaling`` must
        be None: the :class:`Rescaling` parameters will be used to compute the
        input scaling.

    Examples:

        >>> # Convert a quantized Keras model with Keras inputs as images
        >>> # rescaled between -1 and 1
        >>> inputs_akida = images.astype('uint8')
        >>> inputs_keras = (images.astype('float32') - 128) / 128
        >>> model_akida = cnn2snn.convert(model_keras, input_scaling=(128, 128))
        >>> model_akida.evaluate(inputs_akida)

        >>> # Convert a quantized Keras model with Keras inputs as spikes and
        >>> # input scaling of (2.5, 0). Akida spikes must be integers between
        >>> # 0 and 15
        >>> inputs_akida = spikes.astype('uint8')
        >>> inputs_keras = spikes.astype('float32') / 2.5
        >>> model_akida = cnn2snn.convert(model_keras, input_scaling=(2.5, 0))
        >>> model_akida.evaluate(inputs_akida)

        >>> # Convert and directly save the Akida model to fbz file.
        >>> cnn2snn.convert(model_keras, 'model_akida.fbz')

    Args:
        model (:obj:`tf.keras.Model`): a tf.keras model
        file_path (str, optional): destination for the akida model.
            (Default value = None)
        input_scaling (2 elements tuple, optional): value of the input scaling.
            (Default value = None)
        input_is_image (bool, optional): True if input is an image (3-D 8-bit
            input with 1 or 3 channels) followed by QuantizedConv2D. Akida model
            input will be InputConvolutional. If False, Akida model input will
            be InputData. (Default value = True)

    Returns:
        :obj:`akida.Model`: an Akida model.

    Raises:
        ValueError: If ``input_scaling[0]`` is null or negative.
        ValueError: If a :class:`Rescaling` layer is present and
            ``input_scaling`` is not None.
        SystemError: If Tensorflow is not run in eager mode.
    """

    if not tf.executing_eagerly():
        raise SystemError("Tensorflow eager execution is disabled. "
                          "It is required to convert Keras weights to Akida.")

    # Merge separable convolution
    model_sep = utils.merge_separable_conv(model)

    # Generate model mapping
    model_map = generate_model_mapping(model_sep, input_is_image)

    # Check Keras Rescaling layer to replace the input_scaling
    rescaling_input_scaling = _get_rescaling_layer_params(model_sep)
    if rescaling_input_scaling is not None and input_scaling is not None:
        raise ValueError("If a Rescaling layer is present in the model, "
                         "'input_scaling' argument must be None. Receives "
                         f"{input_scaling}.")

    input_scaling = rescaling_input_scaling or input_scaling or (1, 0)

    if input_scaling[0] <= 0:
        raise ValueError("The scale factor 'input_scaling[0]' must be strictly"
                         f" positive. Receives: input_scaling={input_scaling}")

    # Check compatibility of the model map
    check_mapping_compatibility(model_map)

    # Generate Akida model
    ak_inst = generate_model(model_map, input_scaling)

    # Convert weights
    set_weights_thresholds(model_map, ak_inst, input_scaling)

    # Save model if file_path is given
    if file_path:
        # Create directories
        dir_name, base_name = os.path.split(file_path)
        if base_name:
            file_root, file_ext = os.path.splitext(base_name)
            if not file_ext:
                file_ext = '.fbz'
        else:
            file_root = model.name
            file_ext = '.fbz'

        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)

        save_path = os.path.join(dir_name, file_root + file_ext)
        ak_inst.save(save_path)

    return ak_inst


def _get_rescaling_layer_params(model):
    """Computes the new input scaling retrieved from the Keras
    `Rescaling` layer.

    Keras Rescaling layer works as:

     input_k = scale * input_ak + offset

    CNN2SNN input scaling works as:

     input_ak = input_scaling[0] * input_k + input_scaling[1]

    Equivalence leads to:

     input_scaling[0] = 1 / scale
     input_scaling[1] = -offset / scale

    Args:
        model (:obj:`tf.keras.Model`): a tf.keras model.

    Returns:
        tuple: the new input scaling from the Rescaling layer or None if
            no Rescaling layer is at the beginning of the model.
    """

    Rescaling = tf.keras.layers.experimental.preprocessing.Rescaling
    for layer in model.layers[:2]:
        if isinstance(layer, Rescaling):
            return (1 / layer.scale, -layer.offset / layer.scale)
    return None
