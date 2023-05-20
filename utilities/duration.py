def convert_duration(duration: int) -> str:
    """Convert a track's duration from milliseconds to minutes and seconds."""
    minutes, seconds = divmod(duration / 1000, 60)
    return f"{int(minutes)}:{int(seconds):02}"
