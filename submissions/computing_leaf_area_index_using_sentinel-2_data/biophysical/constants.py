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

"""This is the `constants` module.

It contains constants, enums, and configuration values used across the biophysical
operations, such as conversion factors, regular expressions for file naming patterns,
and enums for output value range handling and data file suffixes.
"""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "1.0.0"

import math
import re
from enum import Enum
from pathlib import Path

# Resource directory paths
RESOURCES_DIR = Path(__file__).parent.parent / "resources"
ESA_DATA_DIR = RESOURCES_DIR / "esa"
BIOPHYSICAL_OPS_DATA_DIR = ESA_DATA_DIR / "biophysical"
BIOPHYSICAL_OPS_DATA_DIR_V3 = BIOPHYSICAL_OPS_DATA_DIR / "3_0"

"""
Outputs (from "S2ToolBox Level 2 products: LAI, FAPAR, FCOVER Version 2.1,"
    Section 3.1.2, pg. 20)
| Product       | Unit       | Minimum | Maximum | resolution | 10m Product | 20m Product |
| ------------- | ---------- | ------- | ------- | ---------- | ----------- | ----------- |
| LAI           | m² * m⁻²   |       0 |    8.00 |     0.0100 | x           | x           |
| FAPAR         | -          |       0 |    1.00 |     0.0100 | x           | x           |
| FVC (FCOVER)  | -          |       0 |    1.00 |     0.0100 | x           | x           |
| CCC (LAI_Cab) | µg/cm²     |       0 |  600.00 |     1.0000 |             | x           |
| CWC (LAI_Cw)  | g/cm²      |       0 |    0.55 |     0.0025 |             | x           |
"""  # noqa: E501


# Conversion factor for degrees to radians
DTOR = math.pi / 180.0
# Conversion factor for radians to degrees
RTOD = 180.0 / math.pi  # Java double in original source code

S2L2APattern = re.compile(r"S2[A-C]_MSIL2A_\\d{8}T\\d{6}_N\\d{4}_R\\d{3}_T\\d{2}\\w{3}_\\d{8}T\\d{6}")
S2L1CPattern = re.compile(r"S2[A-C]_MSIL1C_\\d{8}T\\d{6}_N\\d{4}_R\\d{3}_T\\d{2}\\w{3}_\\d{8}T\\d{6}")


class OutputOutOfRangeTypes(Enum):
    OUTPUT_TOO_LOW = "Output value(s) too low."
    OUTPUT_SET_TO_OUTPUT_MIN = "Output value(s) set to output minimum."
    OUTPUT_TOO_HIGH = "Output value(s) too high."
    OUTPUT_SET_TO_OUTPUT_MAX = "Output value(s) set to output maximum."


class DataFileSuffixes(Enum):
    DEFINITION_DOMAIN_GRID = "DefinitionDomain_Grid"
    DEFINITION_DOMAIN_MINMAX = "DefinitionDomain_MinMax"
    DENORMALISATION = "Denormalisation"
    DENORMALIZATION = "Denormalisation"
    EXTREME_CASES = "ExtremeCases"
    NORMALISATION = "Normalisation"
    NORMALIZATION = "Normalisation"
    TEST_CASES = "TestCases"
    LAYER_1_BIAS = "Weights_Layer1_Bias"
    LAYER_1_WEIGHT = "Weights_Layer1_Neurons"
    LAYER_2_BIAS = "Weights_Layer2_Bias"
    LAYER_2_WEIGHT = "Weights_Layer2_Neurons"
