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
"""Provides preprocessing utilities."""
from typing import Any  # noqa # pylint: disable=unused-import
from typing import Optional, Sequence, Tuple, Union
import collections.abc
import warnings

import tensorflow as tf


class RgbToBgr(tf.keras.layers.Layer):
    """A Keras pre-processing layer that converts RGB inputs to BGR color representation."""

    @tf.function
    def call(self, inputs: "tf.Tensor", **kwargs: "Any") -> "tf.Tensor":
        """Performs the RGB to BGR conversion.

        Args:
            inputs: The RGB image.
            kwargs: Additional keyword arguments.

        Returns:
            The BGR image.
        """
        # pylint: disable=no-self-use
        return inputs[..., ::-1]


class RgbaToBgra(tf.keras.layers.Layer):
    """A Keras pre-processing layer that converts RGBA inputs to BGRA color representation."""

    @tf.function
    def call(self, inputs: "tf.Tensor", **kwargs: "Any") -> "tf.Tensor":
        """Performs the RGBA to BGRA conversion.

        Args:
            inputs: The RGBA image.
            kwargs: Additional keyword arguments.

        Returns:
            The BGRA image.
        """
        # pylint: disable=no-self-use
        return tf.concat([inputs[..., :-1][..., ::-1], inputs[..., -1:]], -1)


class PerImageStandardization(tf.keras.layers.Layer):
    """A Keras pre-processing layer that applies per image standardization."""

    @tf.function
    def call(self, inputs: "tf.Tensor", **kwargs: "Any") -> "tf.Tensor":
        """Shifts and linearly scales each image.

         The image will have mean 0 and variance 1. The image is implicitly converted to float representation.

        Args:
            inputs: The image(s) to be standardized.
            kwargs: Additional keyword arguments.

        Returns:
            The standardized image.
        """
        # pylint: disable=no-self-use
        if inputs.dtype != tf.float32:
            inputs = tf.image.convert_image_dtype(inputs, dtype=tf.float32)

        return tf.image.per_image_standardization(inputs)


class Normalization(tf.keras.layers.Layer):
    """A Keras pre-processing layer that shifts the data to zero mean and standard deviation 1."""

    def __init__(
        self,
        mean: Tuple[float, ...],
        std: Tuple[float, ...],
        *args: "Any",
        **kwargs: "Any"
    ) -> None:
        """Creates an instance of the normalization layer.

        Args:
            mean: The mean of the dataset.
            std: The standard deviation of the dataset.
            args: Additional arguments to be passed to the base Layer class.
            kwargs: Additional keyword arguments to be passed to the base Layer class.
        """
        super().__init__(*args, **kwargs)
        self._mean = tf.convert_to_tensor(mean)
        self._std = tf.convert_to_tensor(std)
        if tf.reduce_any(self._std == 0):
            warnings.warn(
                "The defined standard deviation contains zeros. This may lead to numerical issues."
            )

    @tf.function
    def call(self, inputs: "tf.Tensor", **kwargs: "Any") -> "tf.Tensor":
        """Shifts and linearly scales an image by constant values.

        Args:
            inputs: The image(s) to be normalized.
            kwargs: Additional keyword arguments.

        Returns:
            The normalized image.
        """
        return (inputs - tf.cast(self._mean, inputs.dtype)) / tf.cast(
            self._std, inputs.dtype
        )


DEFAULT_LAYER = RgbToBgr()


def add_preprocessing_layers(
    model: "tf.keras.Model",
    layers: Optional[
        Union["tf.keras.layers.Layer", Sequence["tf.keras.layers.Layer"]]
    ] = DEFAULT_LAYER,
    spatial_dims: Optional[Tuple["int", "int"]] = None,
) -> "tf.keras.Model":
    """Prepends a given pre-processing layer to a given Keras model.

    Args:
        model: The Keras model to be wrapped.
        layers: The layers to be prepended.
        spatial_dims: Set new spatial dimensions for the input node. This parameter is expected to contain the
            new height and width in that order. Note: Setting this parameter is only possible for models
            that are invariant to the spatial dimensions of the input such as FCNs.

    Returns:
        A new Keras model wrapping the provided Keras model and the pre-processing layers.
    """
    # Handle single layer and None input
    if layers is None:
        layers = []
    elif not isinstance(layers, collections.abc.Sequence):
        layers = [layers]

    # Create input layer
    new_shape = (
        (model.inputs[0].shape[0],) + spatial_dims + (model.inputs[0].shape[-1],)
        if spatial_dims is not None
        else model.inputs[0].shape
    )
    input_layer = tf.keras.Input(batch_shape=new_shape, name="input")

    # Apply pre-processing layer
    converted = input_layer
    for layer in layers:
        converted = layer(converted)

    # Apply model
    outputs = model(converted)

    # Return new Keras model
    return tf.keras.Model(inputs=input_layer, outputs=outputs)
