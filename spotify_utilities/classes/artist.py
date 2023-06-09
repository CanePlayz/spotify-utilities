from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from api.exceptions import APIError
from terminaltables import SingleTable
from utilities.duration import convert_duration
from utilities.tables import check_value
import requests

if TYPE_CHECKING:
    from classes.album import Album, AlbumInfo
    from classes.track import Track, TrackInfo


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
        _info (dict): The artist's information, organized in a dictionary.
        _albums (dict): The artist's albums, organized in a dictionary with
            the album's ID as the key and the Album object as the value.
        _tracks (dict): The artist's tracks, organized in a dictionary with the
            track's ID as the key and the Track object as the value.
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
        """Return the artist's information."""
        if not self._info:
            self.fetch_artist_info()
        return self._info

    @property
    def albums(self) -> dict[str, Album]:
        """Return the artist's albums."""
        if not self._albums:
            self.fetch_albums()
        return self._albums

    @property
    def tracks(self) -> dict[str, Track]:
        """Return the artist's tracks."""
        if not self._tracks:
            self.fetch_tracks()
        return self._tracks

    def fetch_artist_info(self):
        """Fetch an artist's information from the Spotify API."""
        print(f"Fetching information of {self.name}...")

        try:
            url = f"https://api.spotify.com/v1/artists/{self._id}"
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
            info_dict: ArtistInfo = {
                "genres": info_api["genres"],
                "followers": info_api["followers"]["total"],
                "popularity": info_api["popularity"],
                "images": [i["url"] for i in info_api.json()["images"]],
            }
            self._info = info_dict

            print(f"Successfully fetched information of {self.name}.")

    def fetch_albums(self):
        """Fetch an artist's albums from the Spotify API."""
        from classes.album import Album

        print(f"Fetching albums of {self.name}...")
        albums_api = []
        albums = {}
        url = f"https://api.spotify.com/v1/artists/{self._id}/albums?limit=50"

        try:
            # Fetch albums from the API
            while url:
                response = requests.get(
                    url,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.token}",
                    },
                )
            if response.status_code != 200:
                raise APIError(response.status_code)
            response_json = response.json()
            albums_api.extend(response_json["items"])
            url = response_json["next"]

        except APIError as err:
            err.print_error("albums", self.name)

        else:
            # Prepare everything for the Album instantiation
            for album in albums_api:
                fetched_data: AlbumInfo = {
                    "release_date": album["release_date"],
                    "album_type": album["album_type"],
                    "total_tracks": album["total_tracks"],
                    "genres": album["genres"],
                    "popularity": album["popularity"],
                    "label": album["label"],
                    "images": album["images"],
                    "copyright": album["copyright"],
                }
                artists_of_album = {
                    artist["id"]: Artist(artist["name"], artist["id"], self.token)
                    for artist in album["artists"]
                }
                album_id = album["id"]
                albums[album_id] = Album(
                    album["name"], album_id, self.token, fetched_data, artists_of_album
                )
            self._albums = albums

            print(f"Successfully fetched {len(self._albums)} albums of {self.name}.")

    def fetch_tracks(self):
        """Fetch an artist's tracks from the Spotify API."""
        from classes.track import Track

        print(f"Fetching tracks of {self.name}...")
        tracks_api: dict[Album, list[dict]] = {}
        tracks = {}

        try:
            # Fetch tracks from the API for each album
            for album_id, album_object in self.albums.items():
                url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
                while url:
                    response = requests.get(
                        url, headers={"Authorization": f"Bearer {self.token}"}
                    )
                    if response.status_code != 200:
                        raise APIError(response.status_code)
                    response_json = response.json()
                    tracks_api[album_object].extend(response_json["items"])
                    url = response_json["next"]

        except APIError as err:
            err.print_error("tracks", self.name)

        else:
            for album_object, tracks in tracks_api.items():
                for track in tracks:
                    # Filter out tracks from collaboration albums that don't feature the artist
                    if any(
                        artist_to_check["name"] == self.name
                        for artist_to_check in track["artists"]
                    ):
                        # Prepare everything for the Track instantiation
                        track_id = track["id"]
                        fetched_data: TrackInfo = {
                            "duration": convert_duration(track["duration_ms"]),
                            "explicit": track["explicit"],
                        }
                        track_artists = {
                            artist["id"]: Artist(
                                artist["name"], artist["id"], self.token
                            )
                            for artist in track["artists"]
                        }
                        tracks[track_id] = Track(
                            track["name"],
                            track_id,
                            self.token,
                            fetched_data,
                            album_object,
                            track_artists,
                        )
            self._tracks = tracks

            print(f"Successfully fetched {len(self._tracks)} tracks of {self.name}.")

    def print_artist_info(self):
        """Print an artist's information.

        The information is printed in a table with two columns: Property and
        Value. The table is printed using the terminaltables library."""
        data = [["Property", "Value"]]
        data.append(["Name", self.name])
        data.append(["ID", self._id])

        genres = check_value(", ".join(self.info["genres"]))
        data.append(["Genres", genres])

        data.append(["Followers", check_value(self.info["followers"])])
        data.append(["Popularity", check_value(self.info["popularity"])])
        data.append(["Image", check_value(self.info["images"][0])])
        data.append(["Spotify URL", self.url])

        print(SingleTable(data).table)

    def print_tracks(self):
        """Prints a table of tracks to the terminal.

        The table contains the following columns: Name, Artists, Length, ID and
        Spotify URL. The table is printed using the terminaltables library.
        """
        data = [["Name", "Artists", "Length", "Album", "ID", "Spotify URL"]]

        # Create a list of rows for the table
        for track in self.tracks.values():
            row = [
                track.name,
                ", ".join([artist.name for artist in track._artists.values()]),
                track._info["duration"],
                track._id,
                track.url,
            ]
            data.append(row)

        print(SingleTable(data).table)

    def print_albums(self):
        """Prints a table of albums to the terminal.

        The table contains the following columns: Name, Artists, ID and Spotify
        URL. The table is printed using the terminaltables library.
        """
        data = [["Name", "Artists", "ID", "Spotify URL"]]

        # Create a list of rows for the table
        for album in self.albums.values():
            if album["type"] == "album":
                row = [
                    album.name,
                    ", ".join([artist.name for artist in album.artists.values()]),
                    album._id,
                    album.url,
                ]

                data.append(row)

        print(SingleTable(data).table)
