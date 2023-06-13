def check_value(value: str) -> str:
    """Check if a value is known."""
    if value == None or value == [] or value == "":
        return "Unknown"
    else:
        return value


def shorten_string(string: str, length: int):
    """Shorten a string."""
    if len(string) > length:
        return string[0 : (length - 2)] + "..."
    else:
        return string
