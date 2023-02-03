# MIT License
#
# Copyright (c) 2022 Rahul Nanwani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""DBL Exceptions Module"""

__all__ = (
    'DBLException',
    'EmptyResponse',
    'RateLimited',
    'RequestFailure'
)


class DBLException(Exception):
    """DBL exception base class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)


class RequestFailure(DBLException):
    """API Request Failure

    :param status: (int) API response status code
    :param response: (str) API response message
    """

    def __init__(self, status: int, response: str):
        super().__init__(f"{status}: {response}")


class RateLimited(DBLException):
    """API Rate Limited

    :param json: (dict) API response
    """

    def __init__(self, json: dict):
        super().__init__(
            f"The request to the API endpoint was rate-limited. \n"
            f"Please re-attempt this request after {round(json.get('retry_after', 0), 2):,} seconds."
            if "retry_after" in json else ""
        )


class EmptyResponse(DBLException):
    """API No/Empty Response"""

    def __init__(self):
        super().__init__("No response was received from the API")
