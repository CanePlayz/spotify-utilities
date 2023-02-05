import methods as m
import utilities.exceptions as e


class Artist(object):

    def __init__(self, name, artistID, albums=[], tracks=[], genres=[], popularity=0, followers=0, image_url="", spotify_url="", spotify_id=""):
        self.name = name
        self.artistID = artistID
        self.albums = []
        self.tracks = []
        self.fetch_albums()
        self.fetch_tracks()

    def fetch_artist(self, artistID):
        try:
            fetch_artist.main(artistID)
        except e.ErrorException:
            print("Error while fetching artist: " +
                  e.code_to_str_dict(e.ErrorException.code))
        else:
            self.artist = fetch_artist.main(artistID)

    def fetch_albums(self):
        print("Fetching albums...")
        try:
            fetch_albums.main(self.artistID)
        except e.ErrorException:
            print("Error while fetching albums: " +
                  e.code_to_str_dict(e.ErrorException.code))
        else:
            self.albums = fetch_albums.main(self.artistID)
            print("Albums fetched successfully.")

    def fetch_tracks(self):
        print("Fetching tracks...")
        try:
            fetch_tracks.main(self.artistID)
        except e.ErrorException:
            print("Error while fetching tracks: " +
                  e.exc_to_str_dict(e.ErrorException.code))
        else:
            self.tracks = fetch_tracks.main(self.artistID)
            print("Tracks fetched successfully.")

    def show_artist_info(self):
        print_albums.main(self.albums)

    def show_artist_info(self):
        print_tracks.main(self.tracks)


ConnorPrice = Artist("5zixe6AbgXPqt4c1uSl94L")
