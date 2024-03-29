"""
This module contains the APIError exception class for handling errors from the Spotify API.
"""


class APIError(Exception):
    """Raised when the Spotify API returns an error."""

    exception_codes = [400, 401, 403, 404, 429, 500, 502, 503]

    code_to_str_dict = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        429: "Too Many Requests",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
    }

    def __init__(self, code):
        self.code = code

    def print_error(self, type: str, name: str):
        """Print the error message.

        Args:
            type: The type of the object that caused the error.
            name: The name of the object that caused the error.
        """
        message = self.code_to_str_dict.get(self.code, "Unknown Error")
        print(f"Error while fetching {type} of '{name}': {self.code} ({message})")
