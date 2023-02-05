exception_codes = [400, 401, 403, 404, 429, 500, 502, 503]

# Create a dictionary of exceptions with the keys being the status codes and the values being the exceptions
error = {code: type(f'Exception{code}', (Exception,), {})
         for code in exception_codes}


class ErrorException(Exception):

    def __init__(self, code):
        self.code = code


status_to_exc_dict = {
    400: error[400],
    401: error[401],
    403: error[403],
    404: error[404],
    429: error[429],
    500: error[500],
    502: error[502],
    503: error[503],
}

exc_to_str_dict = {
    error[400]: "Bad Request",
    error[401]: "Unauthorized",
    error[403]: "Forbidden",
    error[404]: "Not Found",
    error[429]: "Too Many Requests",
    error[500]: "Internal Server Error",
    error[502]: "Bad Gateway",
    error[503]: "Service Unavailable",
}

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
