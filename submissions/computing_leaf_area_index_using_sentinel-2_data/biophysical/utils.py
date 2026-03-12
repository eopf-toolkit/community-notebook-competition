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

"""This is the `utils` module.

It contains utility functions for biophysical operations, such as parsing
Sentinel-2 product names, factorizing dimensions, and performing bilinear
interpolation with NaN handling and border extrapolation.
"""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "1.0.0"

from pathlib import Path

import numpy as np
import xarray as xr
from numpy.typing import NDArray
from scipy.ndimage import map_coordinates

from biophysical.models import Sentinel2ProductIdentifier
from biophysical.xaffine import Affine


def _interp_matrix(coords_1d: NDArray, n: int) -> np.ndarray:
    """Build an (M, n) float32 bilinear interpolation matrix.

    Row *i* of the returned matrix encodes the bilinear weights for
    sampling a 1-D array of length *n* at position ``coords_1d[i]``,
    using nearest-boundary clamping (equivalent to ``mode='nearest'``).

    Parameters
    ----------
    coords_1d : NDArray
        1-D array of M sample positions (float).
    n : int
        Length of the source 1-D array.

    Returns
    -------
    np.ndarray
        (M, n) float32 matrix *A* such that ``A @ v`` gives the
        bilinearly interpolated values of a vector *v* of length *n*.
    """
    m = len(coords_1d)
    A = np.zeros((m, n), dtype=np.float32)
    i0 = np.clip(np.floor(coords_1d).astype(np.intp), 0, n - 1)
    i1 = np.clip(i0 + 1, 0, n - 1)
    t = (coords_1d - np.floor(coords_1d)).astype(np.float32)
    rows = np.arange(m)
    # When i0 == i1 (boundary clamp), both weights land on the same
    # cell and correctly sum to 1.
    np.add.at(A, (rows, i0), 1.0 - t)
    np.add.at(A, (rows, i1), t)
    return A


def parse_sentinel2_product_name(
    product_path: Path,
) -> Sentinel2ProductIdentifier:
    """Returns a `Sentinel2ProductIdentifier` from its path."""
    name_parts = product_path.stem.split("_")
    return Sentinel2ProductIdentifier(
        full_identifier=str(product_path),
        mission_id=name_parts[0],
        product_level=name_parts[1],
        datatake_sensing_start_time=name_parts[2],
        processing_baseline_number=name_parts[3],
        relative_orbit_number=name_parts[4],
        tile_id=name_parts[5],
        product_discriminator=name_parts[6],
        product_format=product_path.suffix[1:],
    )


def factorize(n: int) -> list[int]:
    """Return all factors of n."""
    return [x for x in range(1, n + 1) if n % x == 0]


def last_finite(arr: NDArray, axis: int) -> NDArray:
    """Return the last finite value along the given axis.

    NaN, +inf, and -inf are all treated as missing. For each position in
    the output array, the value is the last finite entry found along
    ``axis``. If every value along that axis is non-finite, the result at
    that position is NaN.

    Parameters
    ----------
    arr : NDArray
        Input array (must be a float dtype or convertible to one).
    axis : int
        Axis along which to collapse.

    Returns
    -------
    NDArray
        Array with ``axis`` removed, containing the last finite values.
    """
    arr = np.asarray(arr, dtype=float)
    flipped = np.flip(arr, axis=axis)
    mask = np.isfinite(flipped)
    # argmax on a boolean array returns the index of the first True,
    # which in the flipped view corresponds to the *last* non-NaN.
    idx = np.argmax(mask, axis=axis, keepdims=True)
    result = np.take_along_axis(flipped, idx, axis=axis).squeeze(axis=axis)
    
    # Where the entire slice is NaN, argmax returns 0 — patch those positions.
    # all_nan = ~mask.any(axis=axis)
    # return np.where(all_nan, np.nan, result)

    return result


def _extend_data_v2(slice_2d: NDArray) -> NDArray:
    """Pad 1 pixel on all sides and fill NaN by extrapolation.

    Port of Java ``S2ResamplerUtils.extendDataV2()``.  Copies finite source
    values into the interior of a ``(H+2) × (W+2)`` array and runs 2 passes
    of:

    1. **surroundValuesWithINF** – marks NaN cells that are 8-connected-adjacent
       to any finite *interior* cell as ``+inf`` (candidates for filling).
    2. **extrapolateINFValues** – fills ``+inf`` cells that have two finite
       neighbours in the same axial direction by linear extrapolation:
       ``v = 2·v1 − v2``.
    3. **copyNeighbourINFValues** – fills any remaining ``+inf`` cells by
       copying the value of the nearest finite 8-connected neighbour.

    NaN cells that are still unfilled after both passes (no valid data within
    two pixels in any direction) are set to ``0.0``, matching Java.

    Parameters
    ----------
    slice_2d : NDArray
        2-D source array (float32).  NaN marks missing values.

    Returns
    -------
    NDArray
        ``(H+2) × (W+2)`` float32 array with no NaN.
    """
    h, w = slice_2d.shape
    EH, EW = h + 2, w + 2
    ext = np.full((EH, EW), np.nan, dtype=np.float32)
    src = np.asarray(slice_2d, dtype=np.float32)
    valid = np.isfinite(src)
    ext[1 : h + 1, 1 : w + 1] = np.where(valid, src, np.nan)

    _8nb = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for _ in range(2):
        # ------------------------------------------------------------------ #
        # surroundValuesWithINF                                              #
        # Interior finite cells mark non-finite 8-connected neighbours as    #
        # +inf.  Border cells (row/col 0 and EH-1/EW-1) are never sources.   #
        # ------------------------------------------------------------------ #
        interior_fin = np.isfinite(ext)
        interior_fin[0, :] = interior_fin[-1, :] = False
        interior_fin[:, 0] = interior_fin[:, -1] = False
        mark = np.zeros((EH, EW), dtype=bool)
        for di, dj in _8nb:
            sr = slice(max(0, -di), EH + min(0, -di))
            sc = slice(max(0, -dj), EW + min(0, -dj))
            tr = slice(max(0,  di), EH + min(0,  di))
            tc = slice(max(0,  dj), EW + min(0,  dj))
            mark[tr, tc] |= interior_fin[sr, sc]
        ext[np.isnan(ext) & mark] = np.inf

        # ------------------------------------------------------------------ #
        # extrapolateINFValues                                               #
        # Fill +inf cells that have two finite axial neighbours.             #
        # ------------------------------------------------------------------ #
        changed = True
        while changed:
            changed = False
            inf = np.isposinf(ext)
            fin = np.isfinite(ext)
            # Left cell from right two neighbours
            v = inf[:, :-2] & fin[:, 1:-1] & fin[:, 2:]
            if v.any():
                ext[:, :-2] = np.where(v, 2 * ext[:, 1:-1] - ext[:, 2:], ext[:, :-2])
                changed = True
                inf, fin = np.isposinf(ext), np.isfinite(ext)
            # Right cell from left two neighbours
            v = inf[:, 2:] & fin[:, 1:-1] & fin[:, :-2]
            if v.any():
                ext[:, 2:] = np.where(v, 2 * ext[:, 1:-1] - ext[:, :-2], ext[:, 2:])
                changed = True
                inf, fin = np.isposinf(ext), np.isfinite(ext)
            # Top cell from two rows below
            v = inf[:-2, :] & fin[1:-1, :] & fin[2:, :]
            if v.any():
                ext[:-2, :] = np.where(v, 2 * ext[1:-1, :] - ext[2:, :], ext[:-2, :])
                changed = True
                inf, fin = np.isposinf(ext), np.isfinite(ext)
            # Bottom cell from two rows above
            v = inf[2:, :] & fin[1:-1, :] & fin[:-2, :]
            if v.any():
                ext[2:, :] = np.where(v, 2 * ext[1:-1, :] - ext[:-2, :], ext[2:, :])
                changed = True

        # ------------------------------------------------------------------ #
        # copyNeighbourINFValues                                             #
        # Copy from nearest finite 8-connected neighbour into +inf cells.    #
        # ------------------------------------------------------------------ #
        changed = True
        while changed:
            changed = False
            inf = np.isposinf(ext)
            if not inf.any():
                break
            fin = np.isfinite(ext)
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0),
                           (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                sr = slice(max(0, -di), EH + min(0, -di))
                sc = slice(max(0, -dj), EW + min(0, -dj))
                tr = slice(max(0,  di), EH + min(0,  di))
                tc = slice(max(0,  dj), EW + min(0,  dj))
                copy = inf[tr, tc] & fin[sr, sc]
                if copy.any():
                    ext[tr, tc] = np.where(copy, ext[sr, sc], ext[tr, tc])
                    changed = True
                    break  # restart from first direction (mirrors Java break)

    # Any NaN still remaining (no valid data within 2 pixels) → 0.0
    np.nan_to_num(ext, nan=0.0, copy=False)
    return ext


def _pad_extrapolate_interpolate(
    slice_2d: NDArray,
    coords_y: NDArray,
    coords_x: NDArray,
) -> NDArray:
    """Extend, fill NaN by extrapolation, and bilinear-interpolate a single 2-D slice.

    Uses :func:`_extend_data_v2` (port of Java ``extendDataV2``) to produce a
    ``(H+2) × (W+2)`` array with no NaN, then runs bilinear interpolation onto
    the ``coords_y / coords_x`` pixel grid.
    """
    padded = _extend_data_v2(slice_2d)
    return map_coordinates(padded, [coords_y, coords_x], order=1, mode="nearest")


def bilinear_interpolate_xy(
    da: xr.DataArray,
    target_shape: tuple[int, int],
    x_dim: str = "x",
    y_dim: str = "y",
) -> xr.DataArray:
    """Pad, extrapolate borders, clean non-finite values, and bilinear-interpolate.

    The interpolation is applied along the *x_dim* and *y_dim* axes.
    Any additional dimensions are preserved and each ``(y, x)`` slice
    is processed independently (important when NaN patterns differ
    across slices, e.g. per-detector viewing angles).

    Parameters
    ----------
    da : xr.DataArray
        N-D DataArray with regular *x_dim* / *y_dim* coordinate grids.
    target_shape : tuple[int, int]
        ``(rows, cols)`` of the desired spatial output.
    x_dim, y_dim : str
        Names of the x and y coordinate dimensions.

    Returns
    -------
    xr.DataArray
        Bilinear-interpolated DataArray.  Non-spatial dimensions are
        unchanged; the *y_dim* and *x_dim* axes have *target_shape*
        with recomputed coordinates derived from the affine transform.
    """
    # Ensure y, x are the last two axes
    other_dims = [d for d in da.dims if d not in (y_dim, x_dim)]
    ordered = da.transpose(*(other_dims + [y_dim, x_dim]))

    arr = np.asarray(ordered.values, dtype=np.float32)
    spatial_h, spatial_w = arr.shape[-2], arr.shape[-1]
    batch_shape = arr.shape[:-2]
    batch_size = int(np.prod(batch_shape)) if batch_shape else 1
    arr_3d = arr.reshape(batch_size, spatial_h, spatial_w)

    # Pixel-to-map affine from the input coordinate grid
    transform = Affine.from_dataarray(da, x_dim=x_dim, y_dim=y_dim)

    # Shift the affine origin by -1 pixel in x and y to account for
    # the border padding so that padded pixel (1, 1) still maps to the
    # same map coordinate as original pixel (0, 0).
    padded_transform = transform * Affine.translation(-1, -1)

    # Precompute the interpolation grid (same for every slice).
    # The linspace spans padded pixels 1 to padded_h-2 (i.e. the
    # original data extent) so that output pixel 0 lands exactly on
    # original pixel 0 and the extrapolated border only serves as
    # boundary support for the bilinear kernel.
    target_h, target_w = target_shape
    padded_h, padded_w = spatial_h + 2, spatial_w + 2
    out_y = np.linspace(1, padded_h - 2, target_h)
    out_x = np.linspace(1, padded_w - 2, target_w)
    coords_y, coords_x = np.meshgrid(out_y, out_x, indexing="ij")

    # Interpolate each (y, x) slice independently
    results = np.empty((batch_size, target_h, target_w), dtype=np.float32)
    for i in range(batch_size):
        results[i] = _pad_extrapolate_interpolate(
            arr_3d[i], coords_y, coords_x,
        )

    result = results.reshape(*batch_shape, target_h, target_w)

    # Compute output coordinates from the original (unpadded) affine.
    # out_x spans [1 .. padded_w-2] in the padded grid, which
    # corresponds to [0 .. spatial_w-1] in the original grid.
    # Pixel centres sit at half-integer affine positions (idx + 0.5).
    orig_x = np.linspace(0, spatial_w - 1, target_w)
    orig_y = np.linspace(0, spatial_h - 1, target_h)
    x_coords = float(transform.a) * (orig_x + 0.5) + float(transform.c)
    y_coords = float(transform.e) * (orig_y + 0.5) + float(transform.f)

    out_coords: dict[str, NDArray] = {x_dim: x_coords, y_dim: y_coords}
    for d in other_dims:
        out_coords[d] = ordered.coords[d].values
    # Preserve scalar (non-dimension) coordinates
    for name, coord in da.coords.items():
        if name not in da.dims and name not in out_coords:
            out_coords[name] = coord.values

    return xr.DataArray(
        result,
        dims=other_dims + [y_dim, x_dim],
        coords=out_coords,
        attrs=da.attrs,
    )
