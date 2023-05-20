import requests

from api.exceptions import APIError
from classes.artist.artist import ArtistInfo


def fetch_artist_info(artist_id: str, token: str) -> ArtistInfo:
    """Fetch an artist's information from the Spotify API.

    This function sends a GET request to the Spotify API for the specified
    artist and organizes the information into a dictionary.

    Args:
        artist_id: The ID of the artist whose information is to be fetched.
        token: The Spotify API token for authentication.

    Returns:
        dict: A dictionary with the artist's information.

    Raises:
        APIError: If an error occurs during the API request. The caller is
            responsible for handling this error.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
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
    info_dict: ArtistInfo = {
        "genres": info_api["genres"],
        "followers": info_api["followers"]["total"],
        "popularity": info_api["popularity"],
        "images": [i["url"] for i in info_api.json()["images"]],
    }
    return info_dict
