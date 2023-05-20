import requests

from api.exceptions import APIError
from classes.album.album import Album, AlbumInfo
from classes.artist.artist import Artist


def fetch_albums(artist_id: str, token: str) -> dict[str, Album]:
    """Fetch an artist's albums from the Spotify API.

    This function sends a GET request to the Spotify API for the specified
    artist. It creates and returns a dictionary with album IDs as keys
    and Album objects as values.

    Args:
        artist_id: The ID of the artist whose albums are to be fetched.
        token: The Spotify API token for authentication.

    Returns:
        dict: A dictionary with album ids as keys and Album objects as values.

    Raises:
        APIError: If an error occurs during the API request. The caller is
            responsible for handling this error.
    """
    albums = {}
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?offset=0&limit=50"
    while url:
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
        )

        if response.status_code != 200:
            raise APIError(response.status_code)

        for album in response.json()["items"]:
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
            artists = {
                artist["id"]: Artist(artist["name"], artist["id"], token)
                for artist in album["artists"]
            }

            _id = album["id"]
            albums[_id] = Album(album["name"], _id, token, fetched_data, artists)

        url = response.json()["next"]
    return albums
