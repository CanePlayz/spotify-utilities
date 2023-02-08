import requests

from api.exceptions import APIError
from tokens import access_token


def main(albums):
    tracks = []
    for album in albums:
        query = f"https://api.spotify.com/v1/albums/{album}/tracks"
        response = requests.get(query,
                                headers={"Authorization": f"Bearer {access_token}"})
        match response.status_code:
            case 200: pass
            case _: raise APIError(response.status_code)
        for track in response.json()["items"]:
            tracks.append(track["id"])
    return (tracks)
