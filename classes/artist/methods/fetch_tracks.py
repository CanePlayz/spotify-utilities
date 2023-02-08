import requests

from api.exceptions import APIError


def main(albums, token):

    # Create variables
    tracks = []

    # Fetch tracks for each album
    for album in albums:

        # Send a request to the Spotify API
        query = f"https://api.spotify.com/v1/albums/{album}/tracks"
        response = requests.get(query,
                                headers={"Authorization": f"Bearer {token}"})

        # Check if the request was successful
        match response.status_code:
            case 200: pass
            case _: raise APIError(response.status_code)

        # Add the tracks to the list
        for track in response.json()["items"]:
            tracks.append(track["id"])

    print("With duplicates:" + str(len(tracks)))

    # Remove duplicates
    tracks = list(set(tracks))

    return (tracks)
