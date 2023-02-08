import classes.artist.methods as m
import api.exceptions as e


class Artist(object):

    def __init__(self, name, artistID):
        self.name = name
        self.artistID = artistID
        self.albums = []
        self.tracks = []
        self.genres = []
        self.popularity = 0
        self.followers = 0
        # ... and so on
        # self.fetch_albums()
        # self.fetch_tracks()

    def fetch_artist(self, artistID):
        print(f"Fetching information of {self.name}...")
        try:
            m.fetch_artist.main(artistID)
        except e.APIError as err:
            print(
                "Error while fetching information of {}}...: {} ({})".format(self.name,
                                                                             err.code, e.code_to_str_dict[err.code]))
        else:
            self.artist = m.fetch_artist.main(artistID)

    def fetch_albums(self):
        print(f"Fetching albums of {self.name}...")
        try:
            m.fetch_albums.main(self.artistID)
        except e.APIError as err:
            print("Error while fetching albums of {}: {} ({})".format(self.name,
                                                                      err.code, e.code_to_str_dict[err.code]))
        else:
            self.albums = m.fetch_albums.main(self.artistID)
            print("Albums fetched successfully.")

    def fetch_tracks(self):
        print(f"Fetching tracks of {self.name}...")
        try:
            m.fetch_tracks.main(self.artistID)
        except e.APIError as err:
            print("Error while fetching tracks: " +
                  e.code_to_str_dict[err.code])
        else:
            self.tracks = m.fetch_tracks.main(self.artistID)
            print("Tracks fetched successfully.")

    def show_artist_info(self):
        m.print_albums.main(self.albums)
