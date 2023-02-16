def track(string):
    if len(string) > 30:
        return (string[0:28] + "...")
    else:
        return (string)


def artists(string):
    if len(string) > 30:
        return (string[0:28] + "...")
    else:
        return (string)


def album(string):
    if len(string) > 30:
        return (string[0:28] + "...")
    else:
        return (string)


def copyright(string):
    if len(string) > 63:
        return (string[0:61] + "...")
    else:
        return (string)
