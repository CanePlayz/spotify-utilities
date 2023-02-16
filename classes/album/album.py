import classes.album.methods as methods
import api.exceptions as exceptions


class Album(object):

    def __init__(self, name, id, token):
        self.name = name
        self.id = id
        self.url = f"https://open.spotify.com/album/{id}"
        self.token = token
        self.fetch_album_info()
        self.fetch_tracks()

    def fetch_album_info(self):
        print(f"Fetching information of {self.name}...")
        try:
            self.info = methods.fetch_album_info(self.id, self.token)
        except exceptions.APIError as err:
            print(
                "Error while fetching information of {}}...: {} ({})".format(self.name,
                                                                             err.code, exceptions.code_to_str_dict[err.code]))
        else:
            print(f"Successfully fetched information of {self.name}.")

    def fetch_tracks(self):
        print(f"Fetching tracks of {self.name}...")
        try:
            self.tracks = methods.fetch_tracks(
                self.id, self.token)
        except exceptions.APIError as err:
            print(
                f"Error while fetching tracks of {self.name}: {err.code} ({exceptions.code_to_str_dict[err.code]})")
        else:
            print(
                f"Successfully fetched {len(self.tracks)} tracks of {self.name}.")

    def print_album_info(self):
        methods.print_album_info(self.name, self.id, self.url, self.info)

    def print_tracks(self):
        methods.print_tracks(self.tracks)
