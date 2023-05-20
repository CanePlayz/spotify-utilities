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


class APIError(Exception):
    """Raised when the Spotify API returns an error."""

    def __init__(self, code):
        self.code = code

    def print_error(self, type: str, name: str):
        """Print the error message.

        Args:
            type: The type of the object that caused the error.
            name: The name of the object that caused the error.
        """
        message = (
            code_to_str_dict[self.code]
            if self.code in exception_codes
            else "Unknown Error"
        )
        print(f"Error while fetching {type} of {name}: {self.code} ({message})")
