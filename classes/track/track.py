from typing import TypedDict

import classes.track.methods
from api.exceptions import APIError
from classes.album.album import Album
from classes.artist.artist import Artist


class TrackInfo(TypedDict):
    """A dictionary with a track's information."""

    duration: str
    explicit: bool


class ResponseDict(TypedDict):
    """A dictionary with a response from the fetch track info method."""

    info: TrackInfo
    album: Album
    artists: dict[str, Artist]


class Track:
    """Represents a track on Spotify.

    The Track class encapsulates the details of a music track.
    It requires the track's name, unique ID, and a valid Spotify API token
    upon instantiation.

    Attributes:
        name (str): The track's name.
        id (str): The track's unique ID.
        url (str): The track's Spotify URL.
        token (str): A valid Spotify API token.
        _info (dict): The track's information.
        _album (Album): The track's album.
        _artists (dict): The track's artists.
    """

    def __init__(
        self,
        name: str,
        _id: str,
        token: str,
        fetched_data: TrackInfo | None = None,
        album: Album | None = None,
        artists: dict[str, Artist] = {},
    ):
        """Initialize a Track object.

        Args:
            name: The track's name.
            _id: The track's unique ID.
            token: A valid Spotify API token.
            If not provided, additional information, album and artists are
            lazily loaded upon first access to minimize unnecessary API
            requests.
        """
        self.name: str = name
        self._id: str = _id
        self.url: str = f"https://open.spotify.com/track/{_id}"
        self.token: str = token
        self._info: TrackInfo | None = fetched_data
        self._album: Album | None = album
        self._artists: dict[str, Artist] = artists

    @property
    def info(self) -> TrackInfo | None:
        """Return the track's detailed information.

        If not already fetched, fetch it first.
        """
        if not self._info:
            self.fetch_track_info()
        return self._info

    def fetch_track_info(self):
        """Fetch the track's detailed information.

        This method only has one fetch function because the track's artist(s)
        and album can be easily added to the object with the same request.
        """
        print(f"Fetching track info for {self.name}...")
        try:
            response = classes.track.methods.fetch_track_info(self._id, self.token)
            self._info = response["info"]
            self._artists = response["artists"]
            self._album = response["album"]
        except APIError as err:
            err.print_error("information", self.name)
