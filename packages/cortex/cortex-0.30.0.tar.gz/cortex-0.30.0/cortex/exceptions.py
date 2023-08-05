# Copyright 2021 Cortex Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class CortexException(Exception):
    """
    Base class for all Cortex's errors. Each custom exception should be derived from this class.
    """

    pass


class CortexBinaryException(CortexException):
    """
    Raise when binary execution returns an unexpected non-zero return code.
    """

    pass


class NotFound(CortexException):
    """
    Raise when the specified resource or name is not found.
    """

    pass
