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

"""This is the `angles` module.

It contains functions for processing Sentinel-2 viewing angles using detector
footprint masks.
"""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "1.0.0"


import numpy as np
import xarray as xr


def create_detector_mask(
    footprint: xr.DataArray,
    detector_number: int,
) -> xr.DataArray:
    """Create a binary mask (0 or 255) for a specific detector from a footprint array.

    Parameters
    ----------
    footprint : xr.DataArray
        Detector footprint array where pixel values indicate which detector
        covers that pixel (1 for d01, 2 for d02, ..., 12 for d12).
    detector_number : int
        Detector number (1–12) to create the mask for.

    Returns
    -------
    xr.DataArray
        Binary mask with 255 where ``footprint == detector_number`` and 0
        elsewhere, preserving the input coordinates and attributes.
    """
    mask = xr.where(footprint == detector_number, np.uint8(255), np.uint8(0))
    return mask.astype(np.uint8)


def add_detector_dimension(
    footprint: xr.DataArray,
    dt: xr.DataTree,
    detector_dim: str = "detector",
    geometry_path: str = "conditions/geometry",
) -> xr.DataArray:
    """Add a detector dimension and coordinate to a detector footprint DataArray.

    Converts a ``(y, x)`` detector footprint DataArray — where each pixel
    value is a ``uint8`` integer (1–12) identifying the covering detector —
    into a ``(detector, y, x)`` binary mask array.  The detector coordinate
    dtype and label set are taken from the geometry group so that the output
    is immediately compatible with the viewing-angle arrays.

    Parameters
    ----------
    footprint : xr.DataArray
        A single-band detector footprint with shape ``(y, x)`` sourced from
        one of the three ``/conditions/mask/detector_footprint/{r10m,r20m,r60m}``
        resolution groups.  Pixel values are ``uint8`` integers where the
        value identifies the detector (1 → detector 1, 2 → detector 2, …).
    dt : xr.DataTree
        The full product DataTree.  The detector coordinate is read from
        ``geometry_path`` to determine the label dtype and the set of
        detectors to include.
    detector_dim : str, optional
        Name for the new dimension.  Defaults to ``"detector"``.
    geometry_path : str, optional
        Path within *dt* to the geometry group.
        Defaults to ``"conditions/geometry"``.

    Returns
    -------
    xr.DataArray
        Binary (0 or 1) mask array with dims ``(detector, y, x)``.  Each
        slice along the detector dimension is 1 where the pixel belongs to
        that detector and 0 elsewhere.  The detector coordinate matches the
        dtype and values of the geometry detector coordinate.

    Examples
    --------
    >>> da_footprint = dt["conditions/mask/detector_footprint/r20m"]["b05"]
    >>> da_with_detector = add_detector_dimension(da_footprint, dt)
    >>> da_with_detector.dims
    ('detector', 'y', 'x')
    """
    geometry_detectors = dt[geometry_path].coords[detector_dim]
    detector_dtype = geometry_detectors.dtype

    footprint_values = footprint.values  # (y, x) uint8 array

    masks = []
    detector_labels: list[int | str] = []

    for det_label in geometry_detectors.values:
        if np.issubdtype(detector_dtype, np.integer):
            det_num = int(det_label)
            detector_labels.append(det_num)
        else:
            det_num = int(str(det_label).lstrip("d"))
            detector_labels.append(str(det_label))

        mask = (footprint_values == det_num).astype(np.uint8)
        masks.append(
            xr.DataArray(
                mask,
                dims=footprint.dims,
                coords={k: footprint.coords[k] for k in footprint.dims},
            )
        )

    stacked = xr.concat(masks, dim=detector_dim)
    stacked[detector_dim] = detector_labels
    return stacked


def select_angle_by_detector_mask(
    angles: xr.DataArray,
    detector_mask: xr.DataArray,
    detector_dim: str = "detector",
) -> xr.DataArray:
    """Select the per-pixel viewing angle from its covering detector.

    For each spatial pixel the angle value is taken from the one detector
    whose mask equals 1.  Pixels with no detector coverage, or whose covering
    detector has no interpolated angle, are NaN.

    Raw numpy values are used throughout to avoid xarray coordinate alignment
    issues arising from float32 vs float64 precision differences between the
    interpolated-angle and detector-mask grids.

    Parameters
    ----------
    angles : xr.DataArray
        Interpolated viewing angle array with dims ``(detector, y, x)`` as
        returned by :func:`~biophysical.utils.bilinear_interpolate_xy` applied
        to ``viewing_incidence_angles`` for a single band and angle type
        (zenith or azimuth).  May contain NaN where a detector had no source
        data.
    detector_mask : xr.DataArray
        Binary (0 or 1) mask with dims ``(detector, y, x)`` as produced by
        :func:`add_detector_dimension`.  Exactly one detector slice should be
        1 per pixel.
    detector_dim : str, optional
        Name of the detector dimension.  Defaults to ``"detector"``.

    Returns
    -------
    xr.DataArray
        Viewing angle array with spatial dims ``(y, x)``.  Each pixel holds
        the angle from its covering detector.  Pixels with no detector
        coverage, or whose covering detector has no angle data, are NaN.
    """
    det_axis = angles.dims.index(detector_dim)

    angle_vals = angles.values   # (detector, y, x), may contain NaN
    mask_vals = detector_mask.values  # (detector, y, x), 0 or 1

    # Suppress non-covering detectors: np.where selects 0.0 directly (not
    # a multiply), so NaN in non-covering slices does not contaminate the
    # result.  NaN in the covering slice (mask == 1) propagates as expected.
    masked = np.where(mask_vals == 0, 0.0, angle_vals)

    # Collapse the detector axis.  Since detectors do not overlap, at most
    # one slice is non-zero per pixel, so sum == that detector's angle.
    result = masked.sum(axis=det_axis)

    # Pixels where no detector is active should be NaN, not 0.
    # Check mask coverage directly rather than the angle sum so that
    # a valid angle of exactly 0.0 is never misclassified.
    no_coverage = mask_vals.sum(axis=det_axis) == 0
    result = np.where(no_coverage, np.nan, result)

    spatial_dims = [d for d in angles.dims if d != detector_dim]
    out_coords = {d: angles.coords[d].values for d in spatial_dims if d in angles.coords}
    return xr.DataArray(result, dims=spatial_dims, coords=out_coords, attrs=angles.attrs)


def downsample_detector_masks(
    stacked_masks: xr.DataArray,
    target_shape: tuple[int, int],
) -> xr.DataArray:
    """Downsample stacked detector masks using nearest-neighbor sampling.

    Used when the detector footprint resolution (e.g. 10m → 10980×10980)
    is higher than the target processing resolution (e.g. 20m → 5490×5490).

    Parameters
    ----------
    stacked_masks : xr.DataArray
        Binary mask array with dims ``(detector, y, x)`` as produced by
        :func:`stack_detector_masks`.
    target_shape : tuple[int, int]
        Desired ``(height, width)`` for the y and x dimensions.

    Returns
    -------
    xr.DataArray
        Downsampled mask with dims ``(detector, y, x)`` and shape
        ``(n_detectors, target_shape[0], target_shape[1])``.
    """
    src_h, src_w = stacked_masks.sizes["y"], stacked_masks.sizes["x"]
    tgt_h, tgt_w = target_shape

    if (src_h, src_w) == (tgt_h, tgt_w):
        return stacked_masks

    # Nearest-neighbor indices
    y_idx = np.linspace(0, src_h - 1, tgt_h).round().astype(int)
    x_idx = np.linspace(0, src_w - 1, tgt_w).round().astype(int)

    downsampled = stacked_masks.values[:, y_idx][:, :, x_idx]

    # Build new y/x coordinates by sampling the originals
    new_y = stacked_masks.coords["y"].values[y_idx]
    new_x = stacked_masks.coords["x"].values[x_idx]

    return xr.DataArray(
        downsampled,
        dims=stacked_masks.dims,
        coords={
            "detector": stacked_masks.coords["detector"],
            "y": new_y,
            "x": new_x,
        },
    )


def compute_view_angle_mean(
    per_band_angles: dict[str, xr.DataArray],
) -> xr.DataArray:
    """Compute the pixel-wise mean viewing angle across bands.

    For each pixel the mean is taken over all bands that have a non-zero
    (i.e. detector-covered) value.  Pixels not covered by any band are NaN.

    Parameters
    ----------
    per_band_angles : dict[str, xr.DataArray]
        Mapping of band name to the merged (summed across detectors) angle
        array for that band.  All arrays must share the same spatial
        dimensions.

    Returns
    -------
    xr.DataArray
        Mean viewing angle with shape ``(y, x)``.
    """
    arrays = list(per_band_angles.values())
    stacked = np.stack([a.values for a in arrays], axis=0)

    # Gap pixels (no detector coverage) are NaN after select_angle_by_detector_mask.
    # Use nanmean so they don't dilute the mean of covered bands.
    mean = np.nanmean(stacked, axis=0)

    # Use coordinates from the first band array
    first = arrays[0]
    return xr.DataArray(
        mean,
        dims=first.dims,
        coords={k: v for k, v in first.coords.items() if k in first.dims},
    )
