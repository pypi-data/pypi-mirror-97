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
"""Provides conversion functions to generate a CZModel from exported TensorFlow models."""
import os
from typing import Tuple, Union, Sequence, Optional, TYPE_CHECKING

from tensorflow.keras import Model
from tensorflow.keras.models import load_model

from .model_metadata import ModelSpec
from .util import keras_to_czmodel
from .util.argument_parsing import dir_file

# Ignore flake8 imported but unused warnings (does not recognize non-runtime check). Checked by mypy
if TYPE_CHECKING:
    from tensorflow.keras.layers import Layer  # noqa: F401


def convert_from_model_spec(
    model_spec: ModelSpec,
    output_path: str,
    output_name: str = "DNNModel",
    spatial_dims: Optional[Tuple[int, int]] = None,
    preprocessing: Union["Layer", Sequence["Layer"]] = None,
) -> None:
    """Convert a TensorFlow .pb or TensorFlow Keras model to a CZModel usable in ZEN Intellesis.

    Args:
        model_spec: A ModelSpec object describing the specification of the CZModel to be generated.
        output_path: A folder to store the generated CZModel file.
        output_name: The name of the generated .czmodel file.
        spatial_dims: New spatial dimensions for the input node (see final usage for more details)
        preprocessing: A sequence of layers to be prepended to the model. (see final usage for more details)
    """
    # Create output directory
    os.makedirs(output_path, exist_ok=True)

    # Load model if necessary
    model = (
        model_spec.model
        if isinstance(model_spec.model, Model)
        else load_model(model_spec.model)
    )

    # Convert model
    keras_to_czmodel.convert(
        model=model,
        model_metadata=model_spec.model_metadata,
        output_path=os.path.join(output_path, output_name),
        spatial_dims=spatial_dims,
        preprocessing=preprocessing,
    )


def convert_from_json_spec(
    model_spec_path: str,
    output_path: str,
    output_name: str = "DNNModel",
    spatial_dims: Optional[Tuple[int, int]] = None,
    preprocessing: Union["Layer", Sequence["Layer"]] = None,
) -> None:
    """Converts a TensorFlow SavedModel specified in a JSON metadata file to a CZModel that is usable in ZEN Intellesis.

    Args:
        model_spec_path: The path to the JSON specification file.
        output_path: A folder to store the generated CZModel file.
        output_name: The name of the generated .czmodel file.
        spatial_dims: New spatial dimensions for the input node (see final usage for more details)
        preprocessing: A sequence of layers to be prepended to the model. (see final usage for more details)
    """
    # Parse the specification JSON file
    parsed_spec = ModelSpec.from_json(model_spec_path)

    # Write CZModel to disk
    convert_from_model_spec(
        parsed_spec,
        output_path,
        output_name,
        spatial_dims=spatial_dims,
        preprocessing=preprocessing,
    )


def main() -> None:
    """Console script to convert a TensorFlow proto-buffer to a CZModel."""
    # Import argument parser
    import argparse  # pylint: disable=import-outside-toplevel

    # Define expected arguments
    parser = argparse.ArgumentParser(
        description="Convert a TensorFlow proto-buffer to a CZModel that can be executed inside ZEN."
    )
    parser.add_argument(
        "model_spec",
        type=dir_file,
        help="A JSON file containing the model specification.",
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="The path where the generated CZModel will be created.",
    )
    parser.add_argument(
        "output_name", type=str, help="The name of the generated CZModel."
    )

    # Parse arguments
    args = parser.parse_args()

    # Run conversion
    convert_from_json_spec(args.model_spec, args.output_path, args.output_name)


if __name__ == "__main__":
    main()
