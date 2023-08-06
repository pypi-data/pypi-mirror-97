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
from io import BytesIO
from typing import TYPE_CHECKING

from czmodel.util.model_packing import create_model_zip

# Ignore flake8 imported but unused warnings (does not recognize non-runtime check). Checked by mypy
if TYPE_CHECKING:
    from czmodel.model_metadata import ModelMetadata  # noqa: F401


_ONNX_OPSET = 11


def convert(model: str, model_metadata: "ModelMetadata", output_path: str,) -> None:
    """Converts a given Keras model to a TensorFlow .pb model optimized for inference.

    Args:
        model: Keras model to be converted. The model must have a separate InputLayer as input node.
        model_metadata: The metadata required to generate a CZModel.
        output_path: Destination path to the .czmodel file that will be generated.
    """
    # Pack model into CZModel
    with open(model, "rb") as f:
        buffer = BytesIO(f.read())
        create_model_zip(
            model=buffer.getbuffer(),
            model_metadata=model_metadata,
            output_path=output_path,
        )
