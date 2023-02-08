exception_codes = [400, 401, 403, 404, 429, 500, 502, 503]


class APIError(Exception):

    def __init__(self, code):
        self.code = code


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
