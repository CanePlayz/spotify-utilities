def track(string):
    if len(string) > 39:
        return (string[0:37] + "...")
    else:
        return (string[0:40])


def artists(string):
    if len(string) > 39:
        return (string[0:37] + "...")
    else:
        return (string[0:40])


def album(string):
    if len(string) > 39:
        return (string[0:37] + "...")
    else:
        return (string[0:40])
