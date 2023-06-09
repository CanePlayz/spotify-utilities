from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

import requests
from api.exceptions import APIError
from utilities.duration import convert_duration

if TYPE_CHECKING:
    from classes.album import Album
    from classes.artist import Artist


class TrackInfo(TypedDict):
    """A dictionary with a track's information."""

    duration: str
    explicit: bool


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
        """Return the track's information."""
        if not self._info:
            self.fetch_track_info()
        return self._info

    @property
    def album(self) -> Album:
        """Return the track's album."""
        if not self._album:
            self.fetch_track_info()
        return self._album

    @property
    def artists(self) -> dict[str, Artist]:
        """Return the track's artists."""
        if not self._artists:
            self.fetch_track_info()
        return self._artists

    def fetch_track_info(self):
        """Fetch a track's information, album and artists from the Spotify
        API."""
        from classes.album import Album
        from classes.artist import Artist

        print(f"Fetching track info for {self.name}...")

        try:
            url = f"https://api.spotify.com/v1/tracks/{self._id}"
            response = requests.get(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.token}",
                },
            )
            if response.status_code != 200:
                raise APIError(response.status_code)

        except APIError as err:
            err.print_error("information", self.name)

        else:
            info_api = response.json()
            info_dict: TrackInfo = {
                "duration": convert_duration(info_api["duration_ms"]),
                "explicit": info_api["explicit"],
            }

            album_api = info_api["album"]
            album = Album(album_api["name"], album_api["id"], self.token)

            artists_api = info_api["artists"]
            artists = {
                "id": Artist(artist["name"], artist["id"], self.token)
                for artist in artists_api
            }

            self._info = info_dict
            self._album = album
            self._artists = artists
