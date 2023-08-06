# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
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
"""Command-line interface"""

import argparse
import re
import os

from .converter import convert
from .quantization import quantize
from .utils import load_quantized_model
from .compatibility import _upgrade_model_with_legacy_quantizers


def quantize_model(model_path, wq, aq, iq):
    """Wrapper to quantize model"""
    model = load_quantized_model(model_path)
    if iq == -1:
        iq = wq
    model_q = quantize(model, wq, aq, iq)
    # Extract base name
    base_name = os.path.splitext(model_path)[0]
    # Cross-platform path may contain alpha characters, /, \ and :
    path_re = r"([\w/\\:]+)"
    # Quantization suffix has a well-identified structure
    suffix_re = r"(_iq\d_wq\d_aq\d)"
    p = re.compile(path_re + suffix_re)
    # Look for an existing quantization suffix in the base name
    m = p.match(base_name)
    if m:
        # Only keep the actual base name (group(2) contains the suffix)
        base_name = m.group(1)
    out_path = f"{base_name}_iq{iq}_wq{wq}_aq{aq}.h5"
    model_q.save(out_path, include_optimizer=False)
    print(f"Model successfully quantized and saved as {out_path}.")


def convert_model(model_path, scale, shift, is_image):
    """Wrapper to convert model"""
    base_name = os.path.splitext(model_path)[0]
    q_model = load_quantized_model(model_path)
    ak_model = convert(q_model,
                       input_scaling=(scale, shift),
                       input_is_image=is_image)
    out_path = f"{base_name}.fbz"
    ak_model.save(out_path)
    print(f"Model successfully converted and saved as {out_path}.")


def main():
    """CNN2SNN command-line interface to quantize/convert/upgrade a model"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", default=None, help="The source model")
    sp = parser.add_subparsers(dest="action")
    q_parser = sp.add_parser("quantize", help="Quantize a Keras model")
    q_parser.add_argument("-wq",
                          "--weight_quantization",
                          type=int,
                          default=4,
                          help="The weight quantization")
    q_parser.add_argument("-aq",
                          "--activ_quantization",
                          type=int,
                          default=4,
                          help="The activations quantization")
    q_parser.add_argument("-iq",
                          "--input_weight_quantization",
                          type=int,
                          default=-1,
                          help="The first layer weight quantization (same as" \
                          " weight_quantization if omitted)")
    c_parser = sp.add_parser(
        "convert", help="Convert a quantized Keras model to an akida model")
    c_parser.add_argument("-sc",
                          "--scale",
                          type=int,
                          default=1,
                          help="The scale factor applied on uint8 inputs.")
    c_parser.add_argument("-sh",
                          "--shift",
                          type=int,
                          default=0,
                          help="The shift applied on uint8 inputs.")
    c_parser.add_argument("--no-image-input",
                          action='store_true',
                          default=False,
                          help="If inputs are not 8-bit images")
    u_parser = sp.add_parser(
        "upgrade", help="Upgrade model to be compatible with cnn2snn>=1.8.10")
    u_parser.add_argument("-o",
                          "--output",
                          type=str,
                          default=None,
                          help="Output model filepath")

    args = parser.parse_args()
    if args.action == "quantize":
        quantize_model(args.model, args.weight_quantization,
                       args.activ_quantization, args.input_weight_quantization)
    if args.action == "convert":
        convert_model(args.model, args.scale, args.shift,
                      not args.no_image_input)
    if args.action == "upgrade":
        _upgrade_model_with_legacy_quantizers(args.model, args.output)
