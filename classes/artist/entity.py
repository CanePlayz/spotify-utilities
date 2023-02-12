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
        # ... and so on
        # self.fetch_albums()
        # self.fetch_tracks()

    def fetch_artist(self):
        print(f"Fetching information of {self.name}...")
        try:
            res = m.fetch_artist.main(self.artistID)
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
            self.albums = m.fetch_albums.main(self.artistID, self.token)
        except e.APIError as err:
            print(
                f"Error while fetching albums of {self.name}: {err.code} ({e.code_to_str_dict[err.code]})")
        else:
            print(
                f"Successfully fetched {len(self.albums)} albums of {self.name}.")
            print("Album IDs: " + str(self.albums))

    def fetch_tracks(self):
        print(f"Fetching tracks of {self.name}...")
        try:
            self.tracks = m.fetch_tracks.main(
                self.name, self.albums, self.token)
        except e.APIError as err:
            print(
                f"Error while fetching tracks of {self.name}: {err.code} ({e.code_to_str_dict[err.code]})")
        else:
            # print(
            # f"Successfully fetched {len(self.tracks)} tracks of {self.name}.")
            print("Track IDs: " + str(self.tracks))

    def show_artist_info(self):
        m.print_albums.main(self.albums)
