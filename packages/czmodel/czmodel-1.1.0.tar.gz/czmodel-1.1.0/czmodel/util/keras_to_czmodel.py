# Copyright 2020 Carl Zeiss Microscopy GmbH

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Provides conversion utility functions."""
import logging
import os
import tempfile
from io import BytesIO
from typing import Sequence, Tuple, Union, Optional, Dict, TYPE_CHECKING
from zipfile import ZipFile

import onnx  # type: ignore  # Library does not provide type hints
import tensorflow as tf
from tf2onnx import tf_loader, utils, optimizer  # type: ignore  # Library does not provide type hints
from tf2onnx.tfonnx import process_tf_graph  # type: ignore  # Library does not provide type hints

from czmodel.util.model_packing import create_model_zip, zip_directory
from czmodel.util.preprocessing import add_preprocessing_layers
from czmodel.util.postprocessing import add_postprocessing_layers

# Ignore flake8 imported but unused warnings (does not recognize non-runtime check). Checked by mypy
if TYPE_CHECKING:
    from tensorflow.keras import Model  # noqa: F401
    from tensorflow.keras.layers import Layer  # noqa: F401
    from czmodel.model_metadata import ModelMetadata  # noqa: F401 # pylint: disable=C0412


_ONNX_OPSET = 12


def convert_saved_model_to_onnx(
    saved_model_dir: str,
    output_file: str,
    target: Optional[Sequence] = None,
    custom_op_handlers: Optional[Dict] = None,
    extra_opset: Optional[Sequence] = None,
) -> None:
    """Exports a SavedModel on disk to an ONNX file.

    Arguments:
        saved_model_dir: The directory containing the model in SavedModel format.
        output_file: The path to the file to be created for the ONNX model.
        target: Workarounds applied to help certain platforms.
        custom_op_handlers: Handlers for custom operations.
        extra_opset: Extra opset, for example the opset used by custom ops.
    """
    graph_def, inputs, outputs = tf_loader.from_saved_model(saved_model_dir, None, None)

    with tf.Graph().as_default() as tf_graph:
        tf.import_graph_def(graph_def, name="")

    with tf_loader.tf_session(graph=tf_graph):
        g = process_tf_graph(
            tf_graph,
            continue_on_error=False,
            target=target,
            opset=_ONNX_OPSET,
            custom_op_handlers=custom_op_handlers,
            extra_opset=extra_opset,
            input_names=inputs,
            output_names=outputs,
        )

    onnx_graph = optimizer.optimize_graph(g)

    model_proto = onnx_graph.make_model(
        "Model {} in ONNX format".format(os.path.split(saved_model_dir)[1])
    )

    utils.save_protobuf(output_file, model_proto)

    # Verify model's structure and check for valid model schema
    onnx.checker.check_model(output_file)


def convert(
    model: "Model",
    model_metadata: "ModelMetadata",
    output_path: str,
    spatial_dims: Optional[Tuple[int, int]] = None,
    preprocessing: Union["Layer", Sequence["Layer"]] = None,
    postprocessing: Union["Layer", Sequence["Layer"]] = None,
) -> None:
    """Converts a given Keras model to either an ONNX model or (upon failure) to a TensorFlow .saved_model.

    The exported model is optimized for inference.

    Args:
        model: Keras model to be converted. The model must have a separate InputLayer as input node.
        model_metadata: The metadata required to generate a CZModel.
        output_path: Destination path to the .czmodel file that will be generated.
        preprocessing: The layers to be prepended.
        postprocessing: The layers to be appended.
        spatial_dims: New spatial dimensions for the input node (see final usage for more details)
    """
    if preprocessing is not None or spatial_dims is not None:
        model = add_preprocessing_layers(
            model=model, layers=preprocessing, spatial_dims=spatial_dims
        )

    if postprocessing is not None:
        model = add_postprocessing_layers(
            model=model, layers=postprocessing
        )

    with tempfile.TemporaryDirectory() as tmpdir_saved_model_name, tempfile.TemporaryDirectory() as tmpdir_onnx_name:
        # Export Keras model in SavedModel format
        model.save(tmpdir_saved_model_name, include_optimizer=False, save_format="tf")
        try:
            # Convert to ONNX
            onnx_path = os.path.join(tmpdir_onnx_name, "model.onnx")
            convert_saved_model_to_onnx(tmpdir_saved_model_name, onnx_path)
            with open(onnx_path, "rb") as f:
                buffer = BytesIO(f.read())
        # pylint: disable=W0703  # Broad exception is justified here since this is a general fallback
        except Exception:
            # Log fallback to SavedModel
            logging.warning(
                "Model could not be converted to ONNX format. "
                "Falling back to SavedModel format. "
                "Using this format is discouraged."
            )
            # Zip saved model
            buffer = BytesIO()
            with ZipFile(buffer, mode="w") as zf:
                zip_directory(tmpdir_saved_model_name, zf)

        # Pack model into CZModel
        create_model_zip(
            model=buffer.getbuffer(),
            model_metadata=model_metadata,
            output_path=output_path,
        )
