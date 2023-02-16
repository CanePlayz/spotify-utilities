class Track(object):

    def __init__(self, name, id, token):
        self.name = name
        self.id = id
        self.url = f"https://open.spotify.com/track/{id}"
        self.token = token
        # self.fetch_track_info()
