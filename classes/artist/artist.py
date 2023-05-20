from api.exceptions import APIError
import classes.artist.methods as methods
from typing import TypedDict
from classes.album.album import Album
from classes.track.track import Track


class ArtistInfo(TypedDict):
    """A dictionary with an artist's information."""

    genres: list[str]
    followers: str
    popularity: int
    images: list[str]


class Artist:
    """Represents an artist on Spotify.

    The Artist class encapsulates the details of an artist.
    It requires the artist'ss name, unique ID, and a valid Spotify API token
    upon instantiation.

    Attributes:
        name (str): The artist's name.
        id (str): The artist's unique ID.
        url (str): The artist's Spotify URL.
        token (str): A valid Spotify API token.
        _info (dict): The artist's information.
        _albums (dict): The artist's albums.
        _tracks (dict): The artist's tracks.
    """

    def __init__(self, name: str, _id: str, token: str):
        """Initialize an Artist object.

        Args:
            name: The artist's name.
            id: The artist's unique ID.
            token: A valid Spotify API token.
        """
        self.name: str = name
        self._id: str = _id
        self.url: str = f"https://open.spotify.com/artist/{id}"
        self.token: str = token
        self._info: ArtistInfo | None = None
        self._albums: dict[str, Album] = {}
        self._tracks: dict[str, Track] = {}

    @property
    def info(self) -> ArtistInfo | None:
        """Return the artist's information.

        If not already fetched, fetch it first.
        """
        if not self._info:
            self.fetch_artist_info()
        return self._info

    @property
    def albums(self) -> dict[str, Album]:
        """Return the artist's albums.

        If not already fetched, fetch them first.
        """
        if not self._albums:
            self.fetch_albums()
        return self._albums

    @property
    def tracks(self) -> dict[str, Track]:
        """Return the artist's tracks.

        If not already fetched, fetch them first.
        """
        if not self._tracks:
            self.fetch_tracks()
        return self._tracks

    def fetch_artist_info(self):
        """Fetch an artist's information from the Spotify API."""
        print(f"Fetching information of {self.name}...")
        try:
            self._info = methods.fetch_artist_info(self._id, self.token)
        except APIError as err:
            err.print_error("information", self.name)
        else:
            print(f"Successfully fetched information of {self.name}.")

    def fetch_albums(self):
        """Fetch an artist's albums from the Spotify API."""
        print(f"Fetching albums of {self.name}...")
        try:
            self._albums = methods.fetch_albums(self._id, self.token)
        except APIError as err:
            err.print_error("albums", self.name)
        else:
            print(f"Successfully fetched {len(self._albums)} albums of {self.name}.")

    def fetch_tracks(self):
        """Fetch an artist's tracks from the Spotify API."""
        print(f"Fetching tracks of {self.name}...")
        try:
            self._tracks = methods.fetch_tracks(self.name, self.albums, self.token)
        except APIError as err:
            err.print_error("tracks", self.name)
        else:
            print(f"Successfully fetched {len(self._tracks)} tracks of {self.name}.")

    def print_artist_info(self):
        methods.print_artist_info(self.name, self._id, self.url, self.info)

    def print_tracks(self):
        methods.print_tracks(self.tracks)

    def print_albums(self):
        methods.print_albums(self.albums)
