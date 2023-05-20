import requests

from api.exceptions import APIError
from classes.album.album import Album
from classes.artist.artist import Artist
from classes.track.track import ResponseDict, TrackInfo
from utilities.duration import convert_duration


def fetch_track_info(track_id: str, token: str) -> ResponseDict:
    """Fetch a track's information from the Spotify API.

    This function sends a GET request to the Spotify API for the specified
    track and organizes the information into a dictionary.

    Args:
        track_id: The ID of the track whose information is to be fetched.
        token: The Spotify API token for authentication.

    Returns:
        dict: A dictionary with the track's information, album and artists.

    Raises:
        APIError: If an error occurs during the API request. The caller is
            responsible for handling this error.
    """
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    if response.status_code != 200:
        raise APIError(response.status_code)

    info_api = response.json()
    info_dict: TrackInfo = {
        "duration": convert_duration(info_api["duration_ms"]),
        "explicit": info_api["explicit"],
    }
    album_api = info_api["album"]
    album = Album(album_api["name"], album_api["id"], token)
    artists_api = info_api["artists"]
    artists = {
        "id": Artist(artist["name"], artist["id"], token) for artist in artists_api
    }

    data: ResponseDict = {"info": info_dict, "album": album, "artists": artists}
    return data
