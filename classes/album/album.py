from typing import TypedDict

import api.exceptions as exceptions
import classes.album.methods as methods
from api.exceptions import APIError
from classes.artist.artist import Artist
from classes.track.track import Track


class AlbumInfo(TypedDict):
    """A dictionary with an album's information."""

    release_date: str
    album_type: str
    total_tracks: int
    genres: list[str]
    popularity: int
    label: str
    images: list[str]
    copyright: list[str]


class Album:
    """Represents an album on Spotify.

    The Album class encapsulates the details of a music album.
    It requires the album's name, unique ID, and a valid Spotify API token
    upon instantiation.

    Attributes:
        name (str): The album's name.
        id (str): The album's unique ID.
        url (str): The album's Spotify URL.
        token (str): A valid Spotify API token.
        _info (dict): The album's information.
        _artists (dict): The album's artists.
        _tracks (dict): The album's tracks.
    """

    def __init__(
        self,
        name: str,
        id: str,
        token: str,
        fetched_data: AlbumInfo | None = None,
        artists: dict[str, Artist] = {},
        tracks: dict[str, Track] = {},
    ):
        """
        Initialize an Album object.

        Args:
            name: The album's name.
            _id: The album's unique ID.
            token: A valid Spotify API token.
            If not provided, additional information, artists and tracks are
            lazily loaded upon first access to minimize unnecessary API
            requests.
        """
        self.name: str = name
        self._id: str = id
        self.url: str = f"https://open.spotify.com/album/{id}"
        self.token: str = token
        self._info: AlbumInfo | None = fetched_data if fetched_data else None
        self._artists: dict[str, Artist] = artists
        self._tracks: dict[str, Track] = tracks

    @property
    def info(self) -> AlbumInfo | None:
        """Return the album's detailed information.

        If not already fetched, fetch it first.
        """
        if not self._info:
            self.fetch_album_info()
        return self._info

    @property
    def artists(self) -> dict[str, Artist]:
        """Return the album's artists.

        If not already fetched, fetch them first.
        """
        if not self._artists:
            self.fetch_artists()
        return self._artists

    @property
    def tracks(self) -> dict[str, Track]:
        """Return the album's tracks.

        If not already fetched, fetch them first.
        """
        if not self._tracks:
            self.fetch_tracks()
        return self._tracks

    def fetch_album_info(self):
        """Fetch an album's information from the Spotify API."""
        print(f"Fetching information of {self.name}...")
        try:
            self._info = methods.fetch_album_info(self._id, self.token)
        except APIError as err:
            err.print_error("information", self.name)
        else:
            print(f"Successfully fetched information of {self.name}.")

    def fetch_artists(self):
        """Fetch an album's artists from the Spotify API."""
        print(f"Fetching artists of {self.name}...")
        try:
            self._artists = methods.fetch_artists(self._id, self.token)
        except APIError as err:
            err.print_error("artists", self.name)
        else:
            print(f"Successfully fetched {len(self._artists)} artists of {self.name}.")

    def fetch_tracks(self):
        """Fetch an album's tracks from the Spotify API."""
        print(f"Fetching tracks of {self.name}...")
        try:
            self._tracks = methods.fetch_tracks(self._id, self.token)
        except APIError as err:
            err.print_error("tracks", self.name)
        else:
            print(f"Successfully fetched {len(self._tracks)} tracks of {self.name}.")

    def print_album_info(self):
        methods.print_album_info(self.name, self._id, self.url, self.info)

    def print_tracks(self):
        methods.print_tracks(self._tracks)
