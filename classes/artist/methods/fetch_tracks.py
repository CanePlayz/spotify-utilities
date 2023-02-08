import requests

from api.exceptions import APIError
from tokens import access_token


def main(albums):

    # Create variables
    tracks = []

    # Fetch tracks for each album
    for album in albums:

        # Send a request to the Spotify API
        query = f"https://api.spotify.com/v1/albums/{album}/tracks"
        response = requests.get(query,
                                headers={"Authorization": f"Bearer {access_token}"})

        # Check if the request was successful
        match response.status_code:
            case 200: pass
            case _: raise APIError(response.status_code)

        # Add the tracks to the list
        for track in response.json()["items"]:
            tracks.append(track["id"])

    return (tracks)
