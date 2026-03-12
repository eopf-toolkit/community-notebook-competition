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

"""Main entry point for running biophysical operations as a module."""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "1.0.0"

from pathlib import Path

import numpy as np
from max.driver import CPU, Accelerator, accelerator_count

from biophysical import (
    BiophysicalOpProcess,
    BiophysicalVariables,
    SatelliteSensors,
    process,
)
from biophysical.utils import factorize

if __name__ == "__main__":
    """Run biophysical operations on test data if the module is executed directly."""
    parent_path = Path(__file__).parent.parent
    test_data_path = (
        parent_path / "resources/esa/biophysical/3_0/S2B/LAI/LAI_TestCases"
    )

    data = np.loadtxt(test_data_path, dtype=np.float32, delimiter=",", encoding="utf-8")
    print(f"original data.shape: {data.shape}")
    data = data.T
    target = data[-1, :]
    features = data[:-1, :]
    # features = data[:11, :]  # Cw testCases have extra columns in them
    # features = data[:6, :]  # S2X_10m LAI_TestCases: need columns 0, 1, and 5
    print(f"data.T.shape: {data.shape}")
    print(f"features.shape: {features.shape}")
    print(f"target.shape: {target.shape}")

    # convert the features list into 3 dimensions: input features, rows, columns
    factors = factorize(features.shape[1])
    i = len(factors) // 2
    rows = factors[i - 1]
    cols = factors[i]
    features = features.reshape(features.shape[0], rows, cols)
    print(f"2D features.shape: {features.shape}")

    op_process = process(
        BiophysicalOpProcess(
            sensor=SatelliteSensors.S2B,
            biophysical_op=BiophysicalVariables.LAI,
            device=CPU() if accelerator_count() == 0 else Accelerator(),
            input_data=features,
        )
    )
    print(f"Processing using {op_process.device}.")
    if op_process.result.data is None:
        print("No results generated.")
    else:
        results = tuple(zip(op_process.result.data.flatten().tolist(), target.tolist()))
        # print(results)
        # print()

        results_passed_test = []
        for result, expected in results:
            threshold = 1e-2
            if expected * 0.001 > threshold:
                threshold = expected * 0.001
            if result < expected + threshold and result > expected - threshold:
                results_passed_test.append(True)
            else:
                results_passed_test.append(False)
        
        # print(results_passed_test)
        total = len(results_passed_test)
        total_true = sum(results_passed_test)
        total_false = total - total_true
        print(f"Total tests: {total}")
        print(f"True: {total_true} ({(total_true / total * 100):.2f}%)")
        print(f"False: {total_false} ({(total_false / total * 100):.2f}%)")
