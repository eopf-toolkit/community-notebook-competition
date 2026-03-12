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

"""This is the `validation` module.

It contians functions for validating the input and output data for biophysical
operations, such as checking to see if the input data values are within the
definition domainfor the operation and checking to see if the output data values
are within the expected range for the operation.
"""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "1.0.0"

from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from biophysical.constants import (
    BIOPHYSICAL_OPS_DATA_DIR_V3,
    DataFileSuffixes,
)
from biophysical.exceptions import ArrayShapeError, InvalidBiophysicalVariable
from biophysical.models import (
    BiophysicalVariable,
    BiophysicalVariables,
    Result,
    SatelliteSensors,
)

if TYPE_CHECKING:
    from biophysical.processing import BiophysicalOpProcess


def is_valid_biophysical_variable(variable: BiophysicalVariable) -> bool:
    return variable in BiophysicalVariables


def value_is_outside_min_max(
    value: int | float,
    min: int | float,
    max: int | float,
) -> int:
    """Returns 1 (True) if value is NOT inclusively within the minimum (min) and
    maximum (max) values, otherwise returns 0 (False).

    This is used to create an array mask where the input values fall outside the
    minimum and maximum allowed values.

    Examples:
        value = -1, min = 0, and max = 1 would return 1 (True) because value < min.
        value = 1.000000001, min = 0, and max = 1 would return 1 (True)
            because value > max.
        value = 0, min = 0, and max = 1 would return 0 (False)
            because min <= value <= max.
        value = 1, min = 0, and max = 1 would return 0 (False)
            because min <= value <= max.
        value = 0.5, min = 0, and max = 1 would return 0 (False)
            because min <= value <= max.
    """
    if value < min or value > max:
        return 1
    return 0


def _validate_data_minmax_arrays(
    data: NDArray,
    minmax_ndarray: NDArray,
) -> None:
    if minmax_ndarray.ndim != 2:
        raise ArrayShapeError(
            "Minimum and maximum values array does not have 2 dimensions."
        )
    if data.shape[0] != minmax_ndarray.shape[1]:
        raise ArrayShapeError(
            "There is a mismatch between the number of input features (channels/bands)"
            " in the processing data array and the number of columns in the"
            " domain minimum and maximum array."
        )
    if minmax_ndarray.shape[0] != 2:
        raise ArrayShapeError(
            "The domain minimum and maximum array does not contain two rows"
            "(min, max)."
        )


def check_input_min_max(
    process_result: Result,
    minmax_ndarray: NDArray,
) -> Result:
    """
    Creates a mask where the input pixels are out of range as defined by the minimum
    and maximum values in the definition domain minimum and maximum values array.
    """
    if not isinstance(process_result.data, np.ndarray):
        raise TypeError(
            "`process_result.data` should be an instance of `numpy.ndarray`."
        )
    if process_result.data.ndim != 3:
        raise ArrayShapeError("Processing data array does not have 3 dimensions.")
    # remove the sun and view angle features from the data array, so that only the
    # values from the imaging bands are left
    data = process_result.data[:-3, :, :]

    _validate_data_minmax_arrays(
        data,
        minmax_ndarray,
    )
    # Vectorized min/max check: reshape bounds to (n_bands, 1, 1) for broadcasting
    mins = minmax_ndarray[0, :].reshape(-1, 1, 1)
    maxs = minmax_ndarray[1, :].reshape(-1, 1, 1)
    invalid_mask = (data < mins) | (data > maxs)
    if np.any(invalid_mask):
        process_result.input_out_of_range = True
        process_result.input_out_of_range_mask = invalid_mask
    return process_result



def check_input_domain(
    process_result: Result,
    domain_grid_ndarray: NDArray,
    minmax_ndarray: NDArray,
) -> Result:
    """Checks to see if the combined band input values for each pixel are within
    the approximated convex hull (see ATBD).
    """
    if not isinstance(process_result.data, np.ndarray):
        raise TypeError(
            "`process_result.data` should be an instance of `numpy.ndarray`."
        )
    if process_result.data.ndim != 3:
        raise ArrayShapeError("Processing data array does not have 3 dimensions.")
    # remove the sun and view angle features from the data array, so that only the
    # values from the imaging bands are left
    data = process_result.data[:-3, :, :]

    _validate_data_minmax_arrays(
        data,
        minmax_ndarray,
    )
    if domain_grid_ndarray.ndim != 2:
        raise ArrayShapeError("Domain grid array does not have 2 dimensions.")
    if data.shape[0] != domain_grid_ndarray.shape[1]:
        raise ArrayShapeError(
            "There is a mismatch between the number of input features (channels/bands)"
            " in the processing data array and the number of columns in the"
            " domain grid array."
        )

    n_bands, height, width = data.shape

    # Vectorized projection: floor(10 * (x - min) / (max - min) + 1)
    # Reshape bounds to (n_bands, 1, 1) for broadcasting
    mins = minmax_ndarray[0, :].reshape(-1, 1, 1)
    maxs = minmax_ndarray[1, :].reshape(-1, 1, 1)
    projected = np.floor(10.0 * (data - mins) / (maxs - mins) + 1.0).astype(np.int32)

    # Reshape to (n_pixels, n_bands) for row-wise comparison
    projected_pixels = projected.reshape(n_bands, -1).T  # (n_pixels, n_bands)

    # Build a set of valid domain grid rows using byte views for fast lookup
    domain_grid_int = domain_grid_ndarray.astype(np.int32)
    domain_grid_bytes = np.ascontiguousarray(domain_grid_int).view(
        np.dtype((np.void, domain_grid_int.dtype.itemsize * domain_grid_int.shape[1]))
    )
    domain_set = set(domain_grid_bytes.ravel().tolist())

    # Check membership using byte views (avoids Python list of 30M elements)
    projected_bytes = np.ascontiguousarray(projected_pixels).view(
        np.dtype((np.void, projected_pixels.dtype.itemsize * projected_pixels.shape[1]))
    )
    # Process in chunks to avoid creating a single 30M-element Python list
    chunk_size = 500_000
    n_pixels = projected_bytes.shape[0]
    invalid_flat = np.empty(n_pixels, dtype=bool)
    for start in range(0, n_pixels, chunk_size):
        end = min(start + chunk_size, n_pixels)
        chunk = projected_bytes[start:end].ravel().tolist()
        invalid_flat[start:end] = [row not in domain_set for row in chunk]

    invalid_mask = invalid_flat.reshape(height, width)

    if np.any(invalid_mask):
        process_result.input_out_of_range = True
        if process_result.input_out_of_range_mask is None:
            process_result.input_out_of_range_mask = invalid_mask
        else:
            process_result.input_out_of_range_mask = (
                invalid_mask | process_result.input_out_of_range_mask
            )

    return process_result


def get_model_data_filepath(
    variable: BiophysicalVariable,
    sensor: SatelliteSensors,
    file_type: DataFileSuffixes,
) -> Path:
    if not is_valid_biophysical_variable(variable):
        raise InvalidBiophysicalVariable(
            f"{variable.name} is not a member of `BiophysicalVariables`."
        )

    return (
        BIOPHYSICAL_OPS_DATA_DIR_V3
        / sensor.name
        / variable.label
        / f"{variable.label}_{file_type.value}"
    )


def check_input_out_of_range(op_process: BiophysicalOpProcess) -> BiophysicalOpProcess:
    """Checks to see if the input values of the imaging bands are within the
    definition domain for the operation.

    If any values are out of bounds defined in the definition domain, then a flag will
    be set on the result, and a mask will be generated identifying those pixels that
    are out of bounds with 1. Any pixel in the mask whose combined band values are
    within the bounds of the definition domain will be set to 0.
    """
    sensor = op_process.sensor
    operation = op_process.biophysical_op
    process_result = op_process.result

    minmax_data_filepath = get_model_data_filepath(
        operation.value, sensor, DataFileSuffixes.DEFINITION_DOMAIN_MINMAX
    )
    minmax_ndarray = np.loadtxt(
        minmax_data_filepath, dtype=np.float32, delimiter=",", encoding="utf-8"
    )
    # print(f"minmax.shape: {minmax_ndarray.shape}")
    process_result = check_input_min_max(process_result, minmax_ndarray)

    grid_data_filepath = get_model_data_filepath(
        operation.value, sensor, DataFileSuffixes.DEFINITION_DOMAIN_GRID
    )
    domain_grid_ndarray = np.loadtxt(
        grid_data_filepath, dtype=np.float32, delimiter=",", encoding="utf-8"
    )
    # print(f"domain_grid.shape: {domain_grid_ndarray.shape}")

    process_result = check_input_domain(
        process_result,
        domain_grid_ndarray,
        minmax_ndarray,
    )
    op_process.result = process_result

    return op_process  # type: ignore


def is_value_too_low(
    value: int | float,
    min: int | float,
    tolerance: int | float,
) -> int:
    """Returns 1 if value is less than min - tolerance. Otherwise returns 0"""
    return 1 if value < (min - tolerance) else 0


def is_value_within_min_tolerance(
    value: int | float,
    min: int | float,
    tolerance: int | float,
) -> int:
    return 1 if (((min - tolerance) < value) and (value < min)) else 0


def is_value_within_max_tolerance(
    value: int | float, max: int | float, tolerance: int | float
) -> int:
    return 1 if (((max + tolerance) > value) and (value > max)) else 0


def is_value_too_high(
    value: int | float,
    max: int | float,
    tolerance: int | float,
) -> int:
    """Returns 1 if value is greater than max + tolerance. Otherwise returns 0"""
    return 1 if value > (max + tolerance) else 0


def check_output_out_of_range(
    op_process: BiophysicalOpProcess,
) -> BiophysicalOpProcess:
    """Checks the output tensor for out of range values.

    Parameters:
        biophysical_op_request: The biophysical opertaion that has been requested.

    Returns:
        The BiophysicalOpRequest with an updated result property.
    """
    sensor = op_process.sensor
    operation = op_process.biophysical_op
    process_result = op_process.result

    if not isinstance(process_result.data, np.ndarray):
        raise TypeError(
            "Processing data array should be an instance of `numpy.ndarray`."
        )
    data: NDArray = process_result.data
    extreme_cases_filepath = get_model_data_filepath(
        operation.value, sensor, DataFileSuffixes.EXTREME_CASES
    )
    extreme_cases = np.loadtxt(
        extreme_cases_filepath,
        delimiter=",",
        encoding="utf-8",
        dtype=np.float32,
    )
    if extreme_cases.shape != (3,):
        raise Exception(
            f"{extreme_cases_filepath.stem} not valid. The file should "
            "contain 1 comma-delimited line with three values: the "
            "tolerance, minimum, and maximum, in that order."
        )
    tolerance = abs(extreme_cases[0])
    output_min = extreme_cases[1]
    output_max = extreme_cases[2]

    # Vectorized output range checks using native numpy comparisons
    # OutputTooLowMask: value < (min - tolerance)
    too_low_mask = data < (output_min - tolerance)
    if np.any(too_low_mask):
        process_result.output_too_low = True
        process_result.output_too_low_mask = too_low_mask

    # OutputSetToOutputMinMask: (min - tolerance) < value < min
    within_min_tol_mask = (data > (output_min - tolerance)) & (data < output_min)
    if np.any(within_min_tol_mask):
        process_result.output_threshold_set_to_min_output = True
        process_result.output_threshold_set_to_min_output_mask = within_min_tol_mask
        data = np.where(within_min_tol_mask, output_min, data)

    # OutputSetToOutputMaxMask: max < value < (max + tolerance)
    within_max_tol_mask = (data > output_max) & (data < (output_max + tolerance))
    if np.any(within_max_tol_mask):
        process_result.output_threshold_set_to_max_output = True
        process_result.output_threshold_set_to_max_output_mask = within_max_tol_mask
        data = np.where(within_max_tol_mask, output_max, data)

    # OutputTooHighMask: value > (max + tolerance)
    too_high_mask = data > (output_max + tolerance)
    if np.any(too_high_mask):
        process_result.output_too_high = True
        process_result.output_too_high_mask = too_high_mask

    process_result.data = data
    op_process.result = process_result
    return op_process
