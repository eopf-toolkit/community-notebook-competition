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

"""This is the `exceptions` module.

It contains custom exception classes for handling errors related to biophysical
operations, such as invalid array shapes, invalid biophysical variables, and invalid
biophysical operation requests.
"""

from __future__ import annotations

__author__: str = "David Meaux"
__version__: str = "1.0.0"


class ArrayShapeError(Exception):
    """Exception raised when an array, which could be a scalar, vector, matrix, or
       tensor, passed into a function has the wrong number of dimensions or one or
       more dimensions has the wrong length.

    Attributes:
        message: An explanation of the error.
    """

    def __init__(self, message: str | None):
        if message:
            self.message = message
        else:
            message = "Invalid input array shape."
        super().__init__(self.message)


class InvalidBiophysicalVariable(Exception):
    """Exception raised when the biophysical variable is not a member of
    BiophysicalVariables.

    Attributes:
        message: An explanation of the error.
    """

    def __init__(self, message: str | None):
        if message:
            self.message = message
        else:
            message = (
                "The given BiophysicalVariable is not a member of BiophysicalVariables."
            )
        super().__init__(self.message)


class InvalidBiophysicalOperationRequest(Exception):
    """Exception raised when the biophysical operation is not valid for the given
    satellite sensor.

    Attributes:
        message: An explanation of the error.
    """

    def __init__(self, message: str | None):
        if message:
            self.message = message
        else:
            message = (
                "The requested operation is not valid for the given" "satellite sensor."
            )
        super().__init__(self.message)
