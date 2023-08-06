# Copyright 2021 Carl Zeiss Microscopy GmbH

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Provides common functionality for packing ANN models into a czmodel file."""
import os
from io import BytesIO
from typing import Union, TYPE_CHECKING
from zipfile import ZipFile

# Ignore flake8 imported but unused warnings (does not recognize non-runtime check). Checked by mypy
if TYPE_CHECKING:
    from czmodel.model_metadata import ModelMetadata  # noqa: F401


def zip_directory(directory: str, zip_file: ZipFile) -> None:
    """Adds an entire directory to a ZipFile.

    Args:
        directory: The directory to be added to the zip file.
        zip_file: The zip file to add the directory to.
    """
    # Iterate all the files in directory
    for folder, _, filenames in os.walk(directory):
        for filename in filenames:
            # Determine full path
            full_path = os.path.join(folder, filename)
            # Determine path relative to directory
            rel_path = os.path.relpath(full_path, directory)
            # Add file to zip
            zip_file.write(full_path, arcname=rel_path)


def create_model_zip(
    model: Union[str, bytes, memoryview],
    model_metadata: "ModelMetadata",
    output_path: str,
) -> None:
    """Creates a CZModel file from a given ModelMetadata.

    Args:
        model: The Keras model to be packed.
        model_metadata: The meta data describing the CZModel to be generated.
        output_path: The path of the CZModel file to be generated.
    """
    # Append correct extension if necessary
    if not output_path.lower().endswith(".czmodel"):
        output_path = output_path + ".czmodel"

    # Create ZIP file
    with ZipFile(output_path, mode="w") as zf:
        # Write model xml file
        buffer = BytesIO()
        model_metadata.to_xml().write(buffer, encoding="utf-8", xml_declaration=True)
        zf.writestr(str(model_metadata.model_id) + ".xml", buffer.getvalue())
        # Pack and rename proto-buffer file
        arcname = str(model_metadata.model_id) + ".model"
        if isinstance(model, str):
            zf.write(model, arcname=arcname)
        else:
            zf.writestr(arcname, model)
        # Pack license file
        if model_metadata.license_file is not None:
            zf.write(
                model_metadata.license_file,
                arcname=os.path.split(model_metadata.license_file)[1],
            )
        # Write empty file with model id
        zf.writestr("modelid=" + str(model_metadata.model_id), "")
