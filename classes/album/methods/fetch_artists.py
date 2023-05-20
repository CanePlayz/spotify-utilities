import requests

from api.exceptions import APIError
from classes.artist.artist import Artist


def fetch_artists(album_id: str, token: str) -> dict[str, Artist]:
    """Fetch an album's artists from the Spotify API.

    This function sends a GET request to the Spotify API for the specified
    album and organizes the artists into a dictionary.

    Args:
        album_id: The ID of the album whose artists are to be fetched.
        token: The Spotify API token for authentication.

    Returns:
        dict: A dictionary with the album's artists.

    Raises:
        APIError: If an error occurs during the API request. The caller is
            responsible for handling this error.
    """
    url = f"https://api.spotify.com/v1/albums/{album_id}/artists"
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    if response.status_code != 200:
        raise APIError(response.status_code)

    artists_api = response.json()["artists"]
    artists_dict = {
        artist["id"]: Artist(artist["name"], artist["id"], token)
        for artist in artists_api
    }
    return artists_dict
