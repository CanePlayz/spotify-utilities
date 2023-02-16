import api.exceptions as e
import classes.artist.methods as m
import env as env


class Artist(object):

    def __init__(self, name, id, token):
        self.name = name
        self.artistID = id
        self.token = token
        self.albums = []
        self.tracks = []
        self.genres = []
        self.popularity = 0
        self.followers = 0
        self.fetch_artist()
        self.fetch_albums()
        self.fetch_tracks()

    def fetch_artist(self):
        print(f"Fetching information of {self.name}...")
        try:
            res = m.fetch_artist(self.artistID)
        except e.APIError as err:
            print(
                "Error while fetching information of {}}...: {} ({})".format(self.name,
                                                                             err.code, e.code_to_str_dict[err.code]))
        else:
            self.followers = res
            # Set attributes

    def fetch_albums(self):
        print(f"Fetching albums of {self.name}...")
        try:
            self.albums = m.fetch_albums(
                self.artistID, self.token)
        except e.APIError as err:
            print(
                f"Error while fetching albums of {self.name}: {err.code} ({e.code_to_str_dict[err.code]})")
        else:
            print(
                f"Successfully fetched {len(self.albums)} albums of {self.name}.")

    def fetch_tracks(self):
        print(f"Fetching tracks of {self.name}...")
        try:
            self.tracks = m.fetch_tracks(
                self.name, self.albums, self.token)
        except e.APIError as err:
            print(
                f"Error while fetching tracks of {self.name}: {err.code} ({e.code_to_str_dict[err.code]})")
        else:
            print(
                f"Successfully fetched {len(self.tracks)} tracks of {self.name}.")

    def print_artist_info(self):
        m.print_albums(self.albums)

    def print_tracks(self):
        m.print_tracks(self.tracks)

    def print_albums(self):
        m.print_albums(self.albums)
