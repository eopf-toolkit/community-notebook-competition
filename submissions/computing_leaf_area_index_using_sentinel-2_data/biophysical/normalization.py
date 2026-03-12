# ===---------------------------------------------------------------------=== #
#    Copyright © 2026, Geomatys, SAS. All rights reserved.
#    http://www.geomatys.com
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you
#    may not use this file except in compliance with the License. You may
#    obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#    or implied. See the License for the specific language governing
#    permissions and limitations under the License.
# ===---------------------------------------------------------------------=== #

"""This is the `normalization` module.

It contains functions for normalizing and denormalizing input and output data for
biophysical operations, such as scaling input features to a range of [-1, 1] and
denormalizing neural network outputs back to their original scale.
"""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "1.0.0"


import numpy as np
from numpy.typing import NDArray

from biophysical.exceptions import ArrayShapeError


def normalize_input_value(
    x: int | float, min: int | float, max: int | float
) -> int | float:
    scale = (2.0 / (max - min))
    bias = (-2.0 * min / (max - min) - 1)
    return (scale * x) + bias


def normalize_by_dtype(ndarray: NDArray) -> NDArray:
    """Normalizes the input array to a 64 bit floating point value ranging
    between 0 and 1.

    Parameters:
        ndarray: The input array, which must be either and integer or floating
            point data type.

    Returns: An ndarray as a `float32` data type.
    """
    match ndarray.dtype.kind:
        case "i" | "u":
            min = np.iinfo(ndarray.dtype).min
            max = np.iinfo(ndarray.dtype).max
        case "f":
            min = np.finfo(ndarray.dtype).min
            max = np.finfo(ndarray.dtype).max
        case _:
            raise TypeError(
                "The input array is neither an integer or floating " "point data type."
            )
    ndarray = ndarray.astype(np.float32)
    return (ndarray - min) / (max - min)


def normalize_nn_input_data(data: NDArray, norms: NDArray) -> NDArray:
    if data.ndim != 3:
        raise ArrayShapeError("Input data array does not have 3 dimensions.")
    if norms.ndim != 2:
        raise ArrayShapeError(
            "Array containing normalization values does not have 2 dimensions."
        )
    if data.shape[0] != norms.shape[0]:
        raise ArrayShapeError(
            "There is a mismatch between the number of input "
            "features (channels/bands) in the data array and the number of "
            "normalization entries in the norms array."
        )
    if norms.shape[1] != 2:
        raise ArrayShapeError(
            "The norms array does not contain two columns (min, max)."
        )

    # Vectorized normalization: scale = 2/(max-min), bias = -2*min/(max-min) - 1
    # Reshape norms to (n_bands, 1, 1) for broadcasting over (y, x)
    mins = norms[:, 0].reshape(-1, 1, 1)
    maxs = norms[:, 1].reshape(-1, 1, 1)
    scale = 2.0 / (maxs - mins)
    bias = -2.0 * mins / (maxs - mins) - 1.0
    return (scale * data + bias).astype(data.dtype)


def denormalize_input_value(
    y: int | float, min: int | float, max: int | float
) -> int | float:
    scale = (0.5 * (max - min))
    bias = (0.5 * (max - min) + min)
    return (scale * y) + bias


def denormalize_nn_ouput_data(data: NDArray, denorms: NDArray) -> NDArray:
    if data.ndim != 2:
        raise ArrayShapeError("Output array does not have 2 dimensions.")
    if denorms.ndim != 1:
        raise ArrayShapeError(
            "Array containing denormalization values does not have 1 dimension."
        )
    if denorms.shape[0] != 2:
        raise ArrayShapeError(
            "Array containing denormalization values does not contain two "
            "columns (min, max)."
        )

    # Vectorized denormalization: scale = 0.5*(max-min), bias = 0.5*(max-min) + min
    scale = 0.5 * (denorms[1] - denorms[0])
    bias = 0.5 * (denorms[1] - denorms[0]) + denorms[0]
    return scale * data + bias
