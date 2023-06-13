from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

import requests
from api.exceptions import APIError
from terminaltables import SingleTable
from utilities.duration import convert_duration
from utilities.tables import check_value, shorten_string

if TYPE_CHECKING:
    from classes.artist import Artist
    from classes.track import Track, TrackInfo


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
        _info (dict): The album's information, organized in a dictionary.
        _artists (dict): The album's artists, organized in a dictionary with
            the artist's ID as the key and the Artist object as the value.
        _tracks (dict): The album's tracks, organized in a dictionary with the
            track's ID as the key and the Track object as the value.
    """

    def __init__(
        self,
        name: str,
        _id: str,
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
        self._id: str = _id
        self.url: str = f"https://open.spotify.com/album/{_id}"
        self.token: str = token
        self._info: AlbumInfo | None = fetched_data if fetched_data else None
        self._artists: dict[str, Artist] = artists
        self._tracks: dict[str, Track] = tracks

    @property
    def info(self) -> AlbumInfo | None:
        """Return the album's information."""
        if not self._info:
            self.fetch_album_info()
        return self._info

    @property
    def artists(self) -> dict[str, Artist]:
        """Return the album's artists."""
        if not self._artists:
            self.fetch_album_info()
        return self._artists

    @property
    def tracks(self) -> dict[str, Track]:
        """Return the album's tracks."""
        if not self._tracks:
            self.fetch_tracks()
        return self._tracks

    def fetch_album_info(self):
        """Fetch an albums's information from the Spotify API."""
        from classes.artist import Artist

        print(f"Fetching information of '{self.name}'...")

        try:
            url = f"https://api.spotify.com/v1/albums/{self._id}"
            response = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {self.token}",
                },
            )
            if response.status_code != 200:
                raise APIError(response.status_code)

        except APIError as e:
            e.print_error("information", self.name)

        else:
            info_api = response.json()
            info: AlbumInfo = {
                "release_date": info_api["release_date"],
                "album_type": info_api["album_type"],
                "total_tracks": info_api["total_tracks"],
                "genres": info_api["genres"],
                "popularity": info_api["popularity"],
                "label": info_api["label"],
                "images": [image["url"] for image in info_api["images"]],
                "copyright": [
                    copyright["text"] for copyright in info_api["copyrights"]
                ],
            }
            self._info = info

            artists_api = info_api["artists"]
            self._artists = {
                artist["id"]: Artist(artist["name"], artist["id"], self.token)
                for artist in artists_api
            }

            print(f"Successfully fetched information of {self.name}.")

    def fetch_tracks(self):
        """Fetch an album's tracks from the Spotify API."""
        from classes.artist import Artist
        from classes.track import Track

        print(f"Fetching tracks of '{self.name}'...")

        try:
            tracks = {}
            url = f"https://api.spotify.com/v1/albums/{self._id}/tracks"
            response = requests.get(
                url, headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code != 200:
                raise APIError(response.status_code)

        except APIError as e:
            e.print_error("tracks", self.name)

        else:
            for track in response.json()["items"]:
                # Prepare everything for the Track instantiation
                track_id = track["id"]
                track_info: TrackInfo = {
                    "duration": convert_duration(track["duration_ms"]),
                    "explicit": track["explicit"],
                }
                track_album = self
                track_artists = {
                    artist["id"]: Artist(artist["name"], artist["id"], self.token)
                    for artist in track["artists"]
                }
                tracks[track_id] = Track(
                    track["name"],
                    track["id"],
                    self.token,
                    track_info,
                    track_album,
                    track_artists,
                )
            self._tracks = tracks

            print(f"Successfully fetched {len(self._tracks)} tracks of {self.name}.")

    def print_album_info(self):
        """Print an album's information.

        The information is printed in a table with two columns: Property and
        Value. The table is printed using the terminaltables library.
        """
        # Create a list of rows for the table
        data = [["Property", "Value"]]
        data.append(["Name", self.name])
        data.append(["ID", self._id])
        data.append(["Release date", check_value(self.info["release_date"])])

        artist_names = [artist.name for artist in self.artists.values()]
        if len(artist_names) == 1:
            data.append(["Artist", artist_names[0]])
        else:
            data.append(["Artists", ", ".join(artist_names)])

        data.append(["Type", self.info["album_type"].capitalize()])
        data.append(["Total tracks", self.info["total_tracks"]])

        genres = check_value(", ".join(self.info["genres"]))
        data.append(["Genres", genres])

        data.append(["Popularity", self.info["popularity"]])
        data.append(["Label", check_value(self.info["label"])])

        try:
            image = self.info["images"][0]
        except IndexError:
            image = None
        data.append(["Cover", check_value(image)])

        copyright = check_value(", ".join(self.info["copyright"]))
        data.append(["Copyright", copyright])

        data.append(["Spotify URL", self.url])

        print(SingleTable(data).table)

    def print_tracks(self):
        """Prints a table of tracks to the terminal.

        The table contains the following columns: Name, Artists, Length, and
        Spotify URL. The table is printed using the terminaltables library.
        """
        data = [["Name", "Artists", "Length", "Spotify URL"]]

        # Create a list of rows for the table
        for track in self.tracks.values():
            data.append(
                [
                    shorten_string(track.name, 32),
                    shorten_string(
                        ", ".join([artist.name for artist in track._artists.values()]),
                        32,
                    ),
                    track._info["duration"],
                    track.url,
                ]
            )

        print(SingleTable(data).table)
