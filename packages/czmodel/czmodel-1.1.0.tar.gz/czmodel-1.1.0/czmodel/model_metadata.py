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
"""This module provides data structures to represent the meta-data of a CZModel containing a TensorFlow ANN model."""
import json
import os
import uuid
from typing import Dict, List, Tuple, NamedTuple, Union, Optional, TYPE_CHECKING
from xml.etree.ElementTree import Element, SubElement, ElementTree

from .util.color_generation import ColorGenerator

# Ignore flake8 imported but unused warnings (does not recognize non-runtime check). Checked by mypy
if TYPE_CHECKING:
    from tensorflow.keras import Model  # noqa: F401


class SegmentationClass(NamedTuple):
    """Class representing the metadata of one target class of a segmentation problem."""

    name: str
    color: Tuple[int, int, int]

    def to_xml(self, label_value: int, node_name: str = "Item") -> Element:
        """Create an XML representation of the model meta data.

        Args:
            label_value: The value of the label assigned to this class.
            node_name: The name of the created node where the class metadata resides in.

        Returns:
            An XML node containing the class metadata.
        """
        # Define node
        model_node = Element(node_name)

        # Add attributes
        model_node.set("colB", str(self.color[2]))
        model_node.set("colG", str(self.color[1]))
        model_node.set("colR", str(self.color[0]))
        model_node.set("LabelValue", str(label_value))
        model_node.set("Name", self.name)

        return model_node


class ModelMetadata(NamedTuple):
    """Class representing the metadata of a model.

    Attributes:
        name: The name of the generated model.
        border_size: For Intellesis models this attribute defines the size of the border that needs to be added to an
            input image such that there are no border effects visible in the required area of the generated
            segmentation mask. For deep architectures this value can be infeasibly large so that the border size must
            be defined in a way that the border effects are “acceptable” in the ANN model creator’s opinion.
        color_handling (Type: string)**: Specifies how color (RGB and RGBA) pixel data are converted to one or more
            channels of scalar pixel data.
            Possible values are: ConvertToMonochrome (Converts color to gray scale),
            SplitRgb (Keeps the pixel representation in RGB space).
        pixel_type: The expected input type of the model. Possible values are:
            Gray8: 8 bit unsigned
            Gray16: 16 bit unsigned
            Gray32Float: 4 byte IEEE float
            Bgr24: 8 bit triples, representing the color channels Blue, Green and Red
            Bgr48: 16 bit triples, representing the color channels Blue, Green and Red
            Bgr96Float: Triple of 4 byte IEEE float, representing the color channels Blue, Green and Red
            Bgra32: 8 bit triples followed by an alpha (transparency) channel
            Gray64ComplexFloat: 2 x 4 byte IEEE float, representing real and imaginary part of a complex number
            Bgr192ComplexFloat: A triple of 2 x 4 byte IEEE float, representing real and imaginary part of a
                complex number, for the color channels Blue, Green and Red
        classes: A list of class names corresponding to the output dimensions of the predicted segmentation mask.
            If the last dimension of the prediction has shape n the provided list must be of length n.
        test_image_file: The path to a test image in a format supported by ZEN. This image is used for basic validation
            of the converted model inside ZEN. Can be absolute or relative to the JSON file.
        license_file: The path to a license file that is added to the generated CZModel. Can be absolute or relative to
            the JSON file.
    """

    name: str
    color_handling: str
    pixel_type: str
    classes: List[SegmentationClass]
    border_size: int
    license_file: Optional[str] = None
    post_processing: Optional[str] = None
    model_id: uuid.UUID = uuid.uuid4()

    @classmethod
    def from_json(cls, model_metadata: Union[str, Dict]) -> "ModelMetadata":
        """This function parses a model specification JSON file to a ModelMetadata object.

        Args:
            model_metadata: The path to the JSON file containing the model specification.

        Returns:
            A ModelMetadata instance carrying all information to generate a CZModel file.
        """
        spec: Dict
        # Load spec from json if necessary
        if isinstance(model_metadata, str):
            with open(model_metadata, "r") as f:
                spec = json.load(f)
        else:
            spec = model_metadata

        # Create color generator
        color_gen = iter(ColorGenerator())

        # Resolve classes
        classes_resolved = [
            SegmentationClass(seg_class, color)
            for seg_class, color in zip(spec["Classes"], color_gen)
        ]

        return ModelMetadata(
            name=os.path.basename(spec.get("ModelPath", "DNN model")),
            color_handling=spec["ColorHandling"],
            pixel_type=spec["PixelType"],
            classes=classes_resolved,
            border_size=spec["BorderSize"],
            license_file=spec.get("LicenseFile", None),
        )

    @classmethod
    def from_params(
        cls,
        color_handling: str,
        pixel_type: str,
        classes: List[str],
        border_size: int,
        name: str = "DNN Model",
        license_file: Optional[str] = None,
    ) -> "ModelMetadata":
        """This function creates ModelMetadata object for a given TensorFlow Keras model.

        Args:
            name: The name of the generated model.
            border_size: For Intellesis models this attribute defines the size of the border that needs to be added to
                an input image such that there are no border effects visible in the required area of the generated
                segmentation mask. For deep architectures this value can be infeasibly large so that the border size
                must be defined in a way that the border effects are “acceptable” in the ANN model creator’s opinion.
            color_handling: Specifies how color (RGB and RGBA) pixel data are converted to one or more channels of
                scalar pixel data. Possible values are: ConvertToMonochrome (Converts color to gray scale),
                SplitRgb (Keeps the pixel representation in RGB space).
            pixel_type: The expected input type of the model. Possible values are:
                Gray8: 8 bit unsigned
                Gray16: 16 bit unsigned
                Gray32Float: 4 byte IEEE float
                Bgr24: 8 bit triples, representing the color channels Blue, Green and Red
                Bgr48: 16 bit triples, representing the color channels Blue, Green and Red
                Bgr96Float: Triple of 4 byte IEEE float, representing the color channels Blue, Green and Red
                Bgra32: 8 bit triples followed by an alpha (transparency) channel
                Gray64ComplexFloat: 2 x 4 byte IEEE float, representing real and imaginary part of a complex number
                Bgr192ComplexFloat: A triple of 2 x 4 byte IEEE float, representing real and imaginary part of a
                    complex number, for the color channels Blue, Green and Red
            classes: A list of class names corresponding to the output dimensions of the predicted segmentation mask.
                If the last dimension of the prediction has shape n the provided list must be of length n.
            license_file: The path to a license file that is added to the generated CZModel. Can be absolute or
                relative to the JSON file.

        Returns:
            A ModelMetadata instance carrying all information to generate a CZModel file.
        """
        # Create color generator
        color_gen = iter(ColorGenerator())
        # Resolve classes
        classes_resolved = [
            SegmentationClass(seg_class, color)
            for seg_class, color in zip(classes, color_gen)
        ]

        model_metadata = ModelMetadata(
            name=name,
            color_handling=color_handling,
            pixel_type=pixel_type,
            classes=classes_resolved,
            border_size=border_size,
            license_file=license_file,
        )

        return model_metadata

    def to_xml(self) -> ElementTree:
        """Creates an XML representation of the model meta data."""
        # Create root node
        model_node = Element("Model")
        model_node.set("Version", "3.1.0")

        # Create model ID
        id_node = SubElement(model_node, "Id")
        id_node.text = str(self.model_id)

        # Add model name
        name_node = SubElement(model_node, "ModelName")
        name_node.text = str(self.name)

        # Add status (only 'Trained' is supported for .pb models)
        status_node = SubElement(model_node, "Status")
        status_node.text = "Trained"

        # Add feature extractor (only 'DeepNeuralNetwork' is supported)
        feature_extractor_node = SubElement(model_node, "FeatureExtractor")
        feature_extractor_node.text = "DeepNeuralNetwork"

        # Add post-processing node
        post_processing_node = SubElement(model_node, "Postprocessing")
        post_processing_node.text = self.post_processing

        # Add color handling node
        color_handling_node = SubElement(model_node, "ColorHandling")
        color_handling_node.text = self.color_handling

        # Add channels (currently only a single channel is supported
        channels_node = SubElement(model_node, "Channels")
        channels_item_node = SubElement(channels_node, "Item")
        channels_item_node.set("PixelType", self.pixel_type)

        # Add Segmentation Classes
        training_classes_node = SubElement(model_node, "TrainingClasses")
        for i, segmentation_class in enumerate(self.classes):
            training_classes_node.append(segmentation_class.to_xml(label_value=i + 1))

        # Add border size
        border_size_node = SubElement(model_node, "BorderSize")
        border_size_node.text = str(self.border_size)

        return ElementTree(model_node)


class ModelSpec(NamedTuple):
    """Model specification tuple."""

    model: Union[str, "Model"]
    model_metadata: ModelMetadata

    @classmethod
    def from_json(cls, model_spec_path: str) -> "ModelSpec":
        """This function parses a model specification JSON file to a ModelSpec object.

        Args:
            model_spec_path: The path to the JSON file containing the model specification.

        Returns:
            A ModelMetadata instance carrying all information to generate a CZModel file.
        """
        with open(model_spec_path, "r") as f:
            spec = json.load(f)

        return ModelSpec(
            model=spec["ModelPath"], model_metadata=ModelMetadata.from_json(spec)
        )
