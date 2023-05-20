import requests

from api.exceptions import APIError
from classes.album.album import Album
from classes.artist.artist import Artist
from classes.track.track import Track, TrackInfo
from utilities.duration import convert_duration


def fetch_tracks(artist_name: str, albums: dict[str, Album], token: str):
    """Fetch an artist's tracks from the Spotify API.

    This function sends a GET request to the Spotify API for the specified
    artist's albums. It creates and returns a dictionary with track IDs as keys
    and Track objects as values.

    Args:
        artist_name: The name of the artist whose tracks are to be fetched.
        albums: A dictionary with album IDs as keys and Album objects as
            values.
        token: The Spotify API token for authentication.

    Returns:
        dict: A dictionary with track IDs as keys and Track objects as values.

    Raises:
        APIError: If an error occurs during the API request. The caller is
            responsible for handling this error.
    """
    tracks = {}
    for album_id, album in albums.items():
        url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

        if response.status_code != 200:
            raise APIError(response.status_code)

        for track in response.json()["items"]:
            # Filter out tracks from collaboration albums that don't feature the artist
            if any(
                artist_to_check["name"] == artist_name
                for artist_to_check in track["artists"]
            ):
                _id = track["id"]
                artists = {
                    artist["id"]: Artist(artist["name"], artist["id"], token)
                    for artist in track["artists"]
                }
                fetched_data: TrackInfo = {
                    "duration": convert_duration(track["duration_ms"]),
                    "explicit": track["explicit"],
                }
                tracks[_id] = Track(
                    track["name"], _id, token, fetched_data, album, artists
                )
    return tracks
