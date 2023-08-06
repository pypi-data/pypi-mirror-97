# Copyright (C) 2021, Mindee.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

import logging
import re
import os
import hashlib
from pathlib import Path
from zipfile import ZipFile
from tensorflow.keras import layers, Model
from tensorflow.keras.utils import get_file
from typing import Optional, List, Any

logging.getLogger("tensorflow").setLevel(logging.DEBUG)


__all__ = ['load_pretrained_params', 'conv_sequence', 'IntermediateLayerGetter']


# matches bfd8deac from resnet18-bfd8deac.ckpt
HASH_REGEX = re.compile(r'-([a-f0-9]*)\.')


def load_pretrained_params(
    model: Model,
    url: Optional[str] = None,
    hash_prefix: Optional[str] = None,
    overwrite: bool = False,
    internal_name: str = 'weights',
    **kwargs: Any,
) -> None:
    """Load a set of parameters onto a model

    Example::
        >>> from doctr.models import load_pretrained_params
        >>> load_pretrained_params(model, "https://yoursource.com/yourcheckpoint-yourhash.zip")

    Args:
        model: the keras model to be loaded
        url: URL of the zipped set of parameters
        hash_prefix: first characters of SHA256 expected hash
        overwrite: should the zip extraction be enforced if the archive has already been extracted
        internal_name: name of the ckpt files
    """

    if url is None:
        logging.warning("Invalid model URL, using default initialization.")
    else:
        filename = url.rpartition('/')[-1]
        archive_path = get_file(filename, url, cache_subdir="models", **kwargs)

        # Check hash in file name
        if hash_prefix is None:
            r = HASH_REGEX.search(filename)
            hash_prefix = r.group(1) if r else None

        if isinstance(hash_prefix, str):
            # Hash the file
            with open(archive_path, 'rb') as f:
                sha_hash = hashlib.sha256(f.read()).hexdigest()

            # Compare to expected hash
            if sha_hash[:len(hash_prefix)] != hash_prefix:
                # Remove file
                os.remove(archive_path)
                raise ValueError(f"corrupted download, the hash of {url} does not match its expected value")

        # Unzip the archive
        archive_path = Path(archive_path)
        params_path = archive_path.parent.joinpath(archive_path.stem)
        if not params_path.is_dir() or overwrite:
            with ZipFile(archive_path, 'r') as f:  # type: ignore[assignment]
                f.extractall(path=params_path)  # type: ignore[attr-defined]

        # Load weights
        model.load_weights(f"{params_path}{os.sep}{internal_name}")


def conv_sequence(
    out_channels: int,
    activation: str = None,
    bn: bool = False,
    padding: str = 'same',
    kernel_initializer: str = 'he_normal',
    **kwargs: Any,
) -> List[layers.Layer]:
    """Builds a convolutional-based layer sequence

    Example::
        >>> from doctr.models import conv_sequence
        >>> from tensorflow.keras import Sequential
        >>> module = Sequential(conv_sequence(32, 'relu', True, kernel_size=3, input_shape=[224, 224, 3]))

    Args:
        out_channels: number of output channels
        activation: activation to be used (default: no activation)
        bn: should a batch normalization layer be added
        padding: padding scheme
        kernel_initializer: kernel initializer

    Returns:
        list of layers
    """
    # No bias before Batch norm
    kwargs['use_bias'] = kwargs.get('use_bias', not(bn))
    # Add activation directly to the conv if there is no BN
    kwargs['activation'] = activation if not bn else None
    conv_seq = [layers.Conv2D(out_channels, padding=padding, kernel_initializer=kernel_initializer, **kwargs)]

    if bn:
        conv_seq.append(layers.BatchNormalization())

    if isinstance(activation, str) and bn:
        conv_seq.append(layers.Activation(activation))

    return conv_seq


class IntermediateLayerGetter(Model):
    """Implements an intermediate layer getter

    Example::
        >>> from doctr.models import IntermediateLayerGetter
        >>> from tensorflow.keras.applications import ResNet50
        >>> target_layers = ["conv2_block3_out", "conv3_block4_out", "conv4_block6_out", "conv5_block3_out"]
        >>> feat_extractor = IntermediateLayerGetter(ResNet50(include_top=False, pooling=False), target_layers)

    Args:
        model: the model to extract feature maps from
        layer_names: the list of layers to retrieve the feature map from
    """
    def __init__(
        self,
        model: Model,
        layer_names: List[str]
    ) -> None:
        intermediate_fmaps = [model.get_layer(layer_name).output for layer_name in layer_names]
        super().__init__(model.input, outputs=intermediate_fmaps)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
