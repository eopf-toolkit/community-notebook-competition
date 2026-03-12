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

"""This is the `processing` module.

It contains the main processing logic for biophysical operations, including
functions for validating biophysical operation requests and running neural
network inference for biophysical operations.
"""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "0.0a1"


from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from max import engine
from max.driver import CPU, Device, Buffer
from max.dtype import DType
from max.graph import DeviceRef, Graph, TensorType, ops

from biophysical.constants import DataFileSuffixes
from biophysical.exceptions import InvalidBiophysicalOperationRequest
from biophysical.models import (
    BiophysicalVariables,
    Result,
    SatelliteSensors,
)
from biophysical.normalization import (
    denormalize_nn_ouput_data,
    normalize_nn_input_data,
)
from biophysical.validation import (
    check_input_out_of_range,
    check_output_out_of_range,
    get_model_data_filepath,
)


@dataclass(slots=True)
class BiophysicalOpProcess:
    sensor: SatelliteSensors
    biophysical_op: BiophysicalVariables
    device: Device
    result: Result

    def __init__(
        self,
        biophysical_op: BiophysicalVariables,
        sensor: SatelliteSensors,
        input_data: NDArray,
        device: Device = CPU(),
    ):
        self.biophysical_op = biophysical_op
        self.sensor = sensor
        self.device = device
        self.result = Result(
            data=input_data,
        )


def is_valid_biophysical_op_request(
    sensor: SatelliteSensors,
    biophysical_op: BiophysicalVariables,
) -> bool:
    valid_sensor = sensor in SatelliteSensors
    valid_op_for_sensor = biophysical_op in sensor.value.biophysical_operations
    return valid_sensor and valid_op_for_sensor


def biophysical_op_nn(op_process: BiophysicalOpProcess) -> BiophysicalOpProcess:
    # NOTE 1: float64 dtypes causes errors on the GPU 2025-09-18
    # NOTE 2: SNAP optical-toolbox opttbx-biophysical uses Float32 data types
    sensor = op_process.sensor
    operation = op_process.biophysical_op
    process_result = op_process.result

    if not isinstance(process_result.data, np.ndarray):
        raise TypeError(
            "Processing data array should be an instance of `numpy.ndarray`."
        )
    data: NDArray = process_result.data
    if not is_valid_biophysical_op_request(sensor, operation):
        raise InvalidBiophysicalOperationRequest(
            f"Calculating {operation.value.name} is not a valid operation for "
            f"{sensor.name}."
        )
    device = op_process.device

    # Normalize data using data from Normalization file
    normalization_filepath = get_model_data_filepath(
        operation.value, sensor, DataFileSuffixes.NORMALIZATION
    )
    norms_ndarray = np.loadtxt(
        normalization_filepath, dtype=np.float32, delimiter=",", encoding="utf-8"
    )
    # print(f"normalisation.shape: {norms_ndarray.shape}")
    data = normalize_nn_input_data(data, norms_ndarray)

    layer_1_weight_filepath = get_model_data_filepath(
        operation.value, sensor, DataFileSuffixes.LAYER_1_WEIGHT
    )
    w1 = np.loadtxt(
        layer_1_weight_filepath, dtype=np.float32, delimiter=",", encoding="utf-8"
    )  # type: ignore

    layer_1_bias_filepath = get_model_data_filepath(
        operation.value, sensor, DataFileSuffixes.LAYER_1_BIAS
    )
    b1 = np.loadtxt(
        layer_1_bias_filepath, dtype=np.float32, delimiter=",", encoding="utf-8"
    )  # type: ignore

    layer_2_weight_filepath = get_model_data_filepath(
        operation.value, sensor, DataFileSuffixes.LAYER_2_WEIGHT
    )
    w2 = np.loadtxt(
        layer_2_weight_filepath, dtype=np.float32, delimiter=",", encoding="utf-8"
    )  # type: ignore

    layer_2_bias_filepath = get_model_data_filepath(
        operation.value, sensor, DataFileSuffixes.LAYER_2_BIAS
    )
    b2 = np.loadtxt(
        layer_2_bias_filepath, dtype=np.float32, delimiter=",", encoding="utf-8"
    )  # type: ignore


    # --- Graph / InferenceSession (old approach) ---
    # DeviceRef is the symbolic device for graph construction;
    # the runtime Device is used for tensor operations and inference.
    device_ref = DeviceRef.from_device(device)

    input_type = TensorType(
        dtype=DType.float32,
        shape=data.shape,
        device=device_ref,
    )
    with Graph(
        "biophysical_op_graph",
        input_types=[input_type],
    ) as graph:
        x = graph.inputs[0]
        # Layer 1 weights/bias as graph constants
        w1_c = ops.constant(w1, dtype=DType.float32, device=device_ref)
        b1_c = ops.constant(b1, dtype=DType.float32, device=device_ref)
        # Linear + tangent sigmoid
        y1 = ops.matmul(ops.transpose(x, 0, 2), ops.transpose(w1_c, 0, 1)) + b1_c  # type: ignore
        y2 = ops.tanh(y1)
        # Layer 2 weights/bias as graph constants
        w2_c = ops.constant(w2, dtype=DType.float32, device=device_ref)
        b2_c = ops.constant(b2, dtype=DType.float32, device=device_ref)
        # Second linear (no activation)
        y3 = ops.matmul(y2, w2_c) + b2_c
        # Set graph output
        graph.output(y3)
    session = engine.InferenceSession(devices=[device])
    model = session.load(graph)
    tensor = Buffer.from_numpy(data)
    tensor = tensor.to(device)
    output = model.execute(tensor)[0]
    assert isinstance(output, Buffer)
    output_ndarray = output.to_numpy()
    output_ndarray = output_ndarray.transpose(1, 0)

    # denormalize data using data from Denormalization file
    denormalization_filepath = get_model_data_filepath(
        operation.value, sensor, DataFileSuffixes.DENORMALIZATION
    )
    denorms_array = np.loadtxt(
        denormalization_filepath, dtype=np.float32, delimiter=",", encoding="utf-8"
    )
    output_ndarray = denormalize_nn_ouput_data(output_ndarray, denorms_array)

    process_result.data = output_ndarray
    op_process.result = process_result

    # return output
    return op_process


def process(
    op_process: BiophysicalOpProcess,
) -> BiophysicalOpProcess:
    """Process the input array for the biophysical operation.

    NOTE:
        All values of the input array should be converted to floating point values
        ranging between 0 and 1 **before** running the process.
    """
    # check if input values out of range
    op_process = check_input_out_of_range(op_process)

    # run biophysical operation neural network inference
    op_process = biophysical_op_nn(op_process)

    # check if nn output out of range
    op_process = check_output_out_of_range(op_process)
    return op_process
