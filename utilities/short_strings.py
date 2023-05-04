def shorten_track(string):
    """Shortens track name to 30 characters"""
    if len(string) > 30:
        return string[0:28] + "..."
    else:
        return string


def shorten_artists(string):
    """Shortens artist name to 30 characters"""
    if len(string) > 30:
        return string[0:28] + "..."
    else:
        return string


def shorten_album(string):
    """Shortens album name to 30 characters"""
    if len(string) > 30:
        return string[0:28] + "..."
    else:
        return string


def copyright(string):
    """Shortens copyright to 61 characters"""
    if len(string) > 63:
        return string[0:61] + "..."
    else:
        return string
