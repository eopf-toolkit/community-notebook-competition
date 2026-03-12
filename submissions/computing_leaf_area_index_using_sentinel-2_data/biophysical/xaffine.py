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

"""This is the `xaffine` module.

It contains the `Affine` class, which represents a vectorized 2D affine
transformation matrix backed by numpy arrays. The `Affine` class provides
methods for applying the affine transformation to pixel coordinates,
computing map coordinates for a given xarray DataArray, inverting the affine
transformation, and composing affine transformations.
"""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "1.0.0"

import numpy as np
import xarray as xr
from numpy.typing import ArrayLike


class Affine:
    """
    Vectorized 2D affine transformation matrix backed by numpy arrays.

    Represents the 3x3 matrix:
        | a  b  c |
        | d  e  f |
        | 0  0  1 |
    which maps pixel (col, row) to map coordinates:
        x = a * col + b * row + c
        y = d * col + e * row + f

    All coefficients are stored as numpy arrays so that every operation
    (composition, application, inversion) broadcasts over batched
    transforms or coordinate grids automatically.

    Parameters
    ----------
    a : ArrayLike
        Scale in x (row 0, col 0).
    b : ArrayLike
        Shear in x (row 0, col 1).
    c : ArrayLike
        Translation in x (row 0, col 2).
    d : ArrayLike
        Shear in y (row 1, col 0).
    e : ArrayLike
        Scale in y (row 1, col 1).
    f : ArrayLike
        Translation in y (row 1, col 2).
    """

    __slots__ = ("a", "b", "c", "d", "e", "f")

    def __init__(self, a: ArrayLike, b: ArrayLike, c: ArrayLike,
                 d: ArrayLike, e: ArrayLike, f: ArrayLike) -> None:
        self.a = np.asarray(a, dtype=np.float32)
        self.b = np.asarray(b, dtype=np.float32)
        self.c = np.asarray(c, dtype=np.float32)
        self.d = np.asarray(d, dtype=np.float32)
        self.e = np.asarray(e, dtype=np.float32)
        self.f = np.asarray(f, dtype=np.float32)

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------

    @classmethod
    def translation(cls, tx: ArrayLike, ty: ArrayLike) -> "Affine":
        """Pure translation: ``| 1 0 tx | | 0 1 ty | | 0 0 1 |``."""
        tx = np.asarray(tx, dtype=np.float32)
        ty = np.asarray(ty, dtype=np.float32)
        return cls(
            np.ones_like(tx), np.zeros_like(tx), tx,
            np.zeros_like(ty), np.ones_like(ty), ty,
        )

    @classmethod
    def from_dataarray(cls, da: xr.DataArray,
                       x_dim: str = "x", y_dim: str = "y") -> "Affine":
        """Derive the affine transform from a DataArray's regular coordinate grid.

        Coordinates are assumed to be at pixel centres.  The returned
        transform origin is the top-left corner of the top-left pixel.

        Parameters
        ----------
        da : xr.DataArray
            Input array whose *x_dim* and *y_dim* coordinates form a
            regular grid.
        x_dim, y_dim : str
            Names of the x and y coordinate dimensions.
        """
        x = da.coords[x_dim].values.astype(np.float32)
        y = da.coords[y_dim].values.astype(np.float32)

        pixel_size_x = (x[-1] - x[0]) / (len(x) - 1)
        pixel_size_y = (y[-1] - y[0]) / (len(y) - 1)

        x_origin = x[0] - pixel_size_x / 2.0
        y_origin = y[0] - pixel_size_y / 2.0

        return cls(pixel_size_x, 0.0, x_origin,
                   0.0, pixel_size_y, y_origin)

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def apply(self, col: ArrayLike, row: ArrayLike
              ) -> tuple[np.ndarray, np.ndarray]:
        """Transform pixel ``(col, row)`` to map ``(x, y)``.

        Parameters
        ----------
        col, row : ArrayLike
            Pixel coordinates.  Any shape that broadcasts with the
            transform coefficients is accepted.

        Returns
        -------
        x, y : np.ndarray
            Map coordinates.
        """
        col = np.asarray(col, dtype=np.float32)
        row = np.asarray(row, dtype=np.float32)
        x = self.a * col + self.b * row + self.c
        y = self.d * col + self.e * row + self.f
        return x, y

    def map_coords(self, da: xr.DataArray,
                   x_dim: str = "x", y_dim: str = "y"
                   ) -> tuple[xr.DataArray, xr.DataArray]:
        """Compute map coordinates for every pixel in *da*.

        Returns two DataArrays (``x_map``, ``y_map``) with the same
        shape and dimensions as the *y_dim* x *x_dim* slice of *da*.
        """
        cols = np.arange(da.sizes[x_dim], dtype=np.float32)
        rows = np.arange(da.sizes[y_dim], dtype=np.float32)
        col_grid, row_grid = np.meshgrid(cols, rows)

        x_map, y_map = self.apply(col_grid, row_grid)

        return (
            xr.DataArray(x_map, dims=(y_dim, x_dim), name="x_map"),
            xr.DataArray(y_map, dims=(y_dim, x_dim), name="y_map"),
        )

    def inverse(self) -> "Affine":
        """Return the inverse affine transform.

        Raises
        ------
        numpy.linalg.LinAlgError
            If any determinant in the batch is zero.
        """
        det = self.a * self.e - self.b * self.d
        inv_det = 1.0 / det
        return Affine(
            self.e * inv_det,
            -self.b * inv_det,
            (self.b * self.f - self.e * self.c) * inv_det,
            -self.d * inv_det,
            self.a * inv_det,
            (self.d * self.c - self.a * self.f) * inv_det,
        )

    # ------------------------------------------------------------------
    # Composition
    # ------------------------------------------------------------------

    def __mul__(self, other: "Affine") -> "Affine":
        """Compose two affine transforms (``self * other``).

        Broadcasts element-wise when coefficients are arrays.
        """
        if not isinstance(other, Affine):
            return NotImplemented
        return Affine(
            self.a * other.a + self.b * other.d,
            self.a * other.b + self.b * other.e,
            self.a * other.c + self.b * other.f + self.c,
            self.d * other.a + self.e * other.d,
            self.d * other.b + self.e * other.e,
            self.d * other.c + self.e * other.f + self.f,
        )

    # ------------------------------------------------------------------
    # Comparison / display
    # ------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Affine):
            return NotImplemented
        return bool(np.all(
            (self.a == other.a) & (self.b == other.b) & (self.c == other.c)
            & (self.d == other.d) & (self.e == other.e) & (self.f == other.f)
        ))

    def __repr__(self) -> str:
        return (f"Affine({self.a}, {self.b}, {self.c},\n"
                f"       {self.d}, {self.e}, {self.f})")
