class Album(object):

    def __init__(self, name, id, token):
        self.name = name
        self.id = id
        self.url = f"https://open.spotify.com/album/{id}"
        self.token = token
        # self.fetch_album_info()
        # self.fetch_tracks()
