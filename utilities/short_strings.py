def track(string):
    if len(string) > 35:
        return (string[0:32] + "...")
    return (string[0:35])


def album(string):
    return (string[0:35])
