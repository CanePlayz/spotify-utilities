import requests

from api.exceptions import APIError
from classes.album.album import AlbumInfo


def fetch_album_info(album_id, token) -> AlbumInfo:
    """Fetch an albums's information from the Spotify API.

    This function sends a GET request to the Spotify API for the specified
    album and organizes the information into a dictionary.

    Args:
        album_id: The ID of the album whose information is to be fetched.
        token: The Spotify API token for authentication.

    Returns:
        dict: A dictionary with the album's information.

    Raises:
        APIError: If an error occurs during the API request. The caller is
            responsible for handling this error.
    """
    url = f"https://api.spotify.com/v1/albums/{album_id}"
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
    info_dict: AlbumInfo = {
        "release_date": info_api["release_date"],
        "album_type": info_api["album_type"].capitalize(),
        "total_tracks": info_api["total_tracks"],
        "genres": info_api["genres"],
        "popularity": info_api["popularity"],
        "label": info_api["label"],
        "images": [image["url"] for image in info_api["images"]],
        "copyright": [copyright["text"] for copyright in info_api["copyrights"]],
    }
    return info_dict
