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

"""This is the `models` module.

It contains data models and domain enums for biophysical operations.
"""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "1.0.0"

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

from numpy.typing import NDArray

SENTINEL2_BANDS_10M = (
    "B03",
    "B04",
    "B08",
)
SENTINEL2_BANDS_20M = (
    "B03",
    "B04",
    "B05",
    "B06",
    "B07",
    "B8A",
    "B11",
    "B12",
    )


@dataclass(frozen=True, slots=True)
class Sentinel2ProductIdentifier:
    """A data structure to handle the naming information of a
    Sentinel 2 product. These attributes can be joined together with an
    underscore (_) and a period (.) between the `product_discriminator`
    and the `product_format` to create the name of the parent foolder of
    the decompressed product.
        For example:
            `S2A_MSIL1C_20170105T013442_N0204_R031_T53NMJ_20170105T013443.SAFE`

            Identifies a Level-1C product acquired by Sentinel-2A on the 5th
            of January, 2017 at 1:34:42 AM. It was acquired over Tile 53NMJ(2)
            during Relative Orbit 031, and processed with Processing
            Baseline 02.04.

    Attributes:
        full_identifier (str): The full identifier composed of all of the
            following attributes.
        mission_id (str): The mission identifier (ID), in the format MMM,
            i.e. "S2A", "S2B", or "S2C.
        product_level (str):  In the format MSIXXX, where "MSIL1C" denotes the
            Level-1C product level and "MSIL2A" denotes the Level-2A
            product level.
        datatake_sensing_start_time (str): The datatake sensing start time,
            in the format YYYYMMDDTHHMMSS.
        processing_baseline_number (str): The Processing Baseline number
            in the format Nxxyy, e.g., "N0204".
        relative_orbit_number (str): The retlative orbin number, in the format
            R000, i.e. "R001" - "R143".
        tile_id (str): The tile identifier in the format Txxxxx.
        product_discriminator (str): A 15 character-long date-time string,
            in the format YYYYMMDDTHHMMSS, used to distinguish between
            different end user products from the same datatake. Depending on
            the instance, the time in this field can be earlier or slightly
            later than the datatake sensing time.
        product_format (str): Defaults to "SAFE". There should be no reason
            to change this unless the format of the product delivered by the
            European Space Agency (ESA) changes to another format.
    """
    full_identifier: str
    mission_id: str
    product_level: str
    datatake_sensing_start_time: str
    processing_baseline_number: str
    relative_orbit_number: str
    tile_id: str
    product_discriminator: str
    product_format: str = "SAFE"


@dataclass(frozen=True, slots=True)
class BiophysicalVariable:
    label: str
    name: str
    description: str
    unit: str


class BiophysicalVariables(Enum):
    LAI = BiophysicalVariable(
        label="LAI",
        name="LAI",
        description="Leaf Area Index (LAI) is defined as half the developed area of "
        "photosynthetically active elements of the vegetation per unit horizontal "
        "ground area.",
        unit="",
    )


class SatelliteSensorType(Enum):
    SENTINEL2A = "Sentinel-2A"
    SENTINEL2B = "Sentinel-2B"
    SENTINEL2C = "Sentinel-2C"


@dataclass(frozen=True, slots=True)
class SatelliteSensor:
    sensor_type: SatelliteSensorType
    spatial_resolution_meters: int
    input_layer_count: int
    biophysical_operations: Sequence[BiophysicalVariables]
    bands: tuple[str, ...] = ()


class SatelliteSensors(Enum):
    S2A = SatelliteSensor(
        sensor_type=SatelliteSensorType.SENTINEL2A,
        spatial_resolution_meters=20,
        input_layer_count=11,
        biophysical_operations=(
            BiophysicalVariables.LAI,
        ),
        bands=SENTINEL2_BANDS_20M,

    )
    S2A_10m = SatelliteSensor(
        sensor_type=SatelliteSensorType.SENTINEL2A,
        spatial_resolution_meters=10,
        input_layer_count=6,
        biophysical_operations=(
            BiophysicalVariables.LAI,
        ),
        bands=SENTINEL2_BANDS_10M,
    )
    S2B = SatelliteSensor(
        sensor_type=SatelliteSensorType.SENTINEL2B,
        spatial_resolution_meters=20,
        input_layer_count=11,
        biophysical_operations=(
            BiophysicalVariables.LAI,
        ),
        bands=SENTINEL2_BANDS_20M,
    )
    S2B_10m = SatelliteSensor(
        sensor_type=SatelliteSensorType.SENTINEL2B,
        spatial_resolution_meters=10,
        input_layer_count=6,
        biophysical_operations=(
            BiophysicalVariables.LAI,
        ),
        bands=SENTINEL2_BANDS_10M,
    )
    S2C = SatelliteSensor(
        sensor_type=SatelliteSensorType.SENTINEL2C,
        spatial_resolution_meters=20,
        input_layer_count=11,
        biophysical_operations=(
            BiophysicalVariables.LAI,
        ),
        bands=SENTINEL2_BANDS_20M,

    )
    S2C_10m = SatelliteSensor(
        sensor_type=SatelliteSensorType.SENTINEL2C,
        spatial_resolution_meters=10,
        input_layer_count=6,
        biophysical_operations=(
            BiophysicalVariables.LAI,
        ),
        bands=SENTINEL2_BANDS_10M,
    )


@dataclass(slots=True)
class Result:
    data: NDArray | None = None

    input_out_of_range: bool = False
    output_threshold_set_to_min_output: bool = False
    output_threshold_set_to_max_output: bool = False
    output_too_low: bool = False
    output_too_high: bool = False

    input_out_of_range_mask: NDArray | None = None
    output_threshold_set_to_min_output_mask: NDArray | None = None
    output_threshold_set_to_max_output_mask: NDArray | None = None
    output_too_low_mask: NDArray | None = None
    output_too_high_mask: NDArray | None = None
