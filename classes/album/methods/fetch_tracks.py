import requests

from api.exceptions import APIError
from classes.album.album import Album
from classes.artist.artist import Artist
from classes.track.track import Track, TrackInfo
from utilities.duration import convert_duration


def fetch_tracks(album_id, token):
    """Fetch an album's tracks from the Spotify API.

    This function sends a GET request to the Spotify API for a specified album.
    It creates and returns a dictionary with track IDs as keys and Track objects
    as values.

    Args:
        album_id: The ID of the album whose tracks are to be fetched.
        token: The Spotify API token for authentication.

    Returns:
        dict: A dictionary with track IDs as keys and Track objects as values.

    Raises:
        APIError: If an error occurs during the API request. The caller is
        responsible for handling this error.
    """
    tracks = {}

    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

    if response.status_code != 200:
        raise APIError(response.status_code)

    for track in response.json()["items"]:
        _id = track["id"]
        track_album = track["album"]
        album = Album(track_album["name"], track_album["id"], token)
        artists = {
            artist["id"]: Artist(artist["name"], artist["id"], token)
            for artist in track["artists"]
        }
        fetched_data: TrackInfo = {
            "duration": convert_duration(track["duration_ms"]),
            "explicit": track["explicit"],
        }
        tracks[_id] = Track(track["name"], _id, token, fetched_data, album, artists)
    return tracks
