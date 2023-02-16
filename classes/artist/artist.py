import api.exceptions as exceptions
import classes.artist.methods as methods


class Artist(object):

    def __init__(self, name, id, token):
        self.name = name
        self.id = id
        self.url = f"https://open.spotify.com/artist/{id}"
        self.token = token
        self.fetch_artist_info()
        self.fetch_albums()
        self.fetch_tracks()

    def fetch_artist_info(self):
        print(f"Fetching information of {self.name}...")
        try:
            self.info = methods.fetch_artist_info(self.id, self.token)
        except exceptions.APIError as err:
            print(
                "Error while fetching information of {}}...: {} ({})".format(self.name,
                                                                             err.code, exceptions.code_to_str_dict[err.code]))
        else:
            print(f"Successfully fetched information of {self.name}.")

    def fetch_albums(self):
        print(f"Fetching albums of {self.name}...")
        try:
            self.albums = methods.fetch_albums(
                self.id, self.token)
        except exceptions.APIError as err:
            print(
                f"Error while fetching albums of {self.name}: {err.code} ({exceptions.code_to_str_dict[err.code]})")
        else:
            print(
                f"Successfully fetched {len(self.albums)} albums of {self.name}.")

    def fetch_tracks(self):
        print(f"Fetching tracks of {self.name}...")
        try:
            self.tracks = methods.fetch_tracks(
                self.name, self.albums, self.token)
        except exceptions.APIError as err:
            print(
                f"Error while fetching tracks of {self.name}: {err.code} ({exceptions.code_to_str_dict[err.code]})")
        else:
            print(
                f"Successfully fetched {len(self.tracks)} tracks of {self.name}.")

    def print_artist_info(self):
        methods.print_artist_info(self.name, self.id, self.url, self.info)

    def print_tracks(self):
        methods.print_tracks(self.tracks)

    def print_albums(self):
        methods.print_albums(self.albums)
