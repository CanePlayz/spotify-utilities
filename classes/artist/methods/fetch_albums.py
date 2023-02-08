import requests

from api.exceptions import APIError
from tokens import access_token


def main(artist_id):
    query = "https://api.spotify.com/v1/artists/{}/albums".format(artist_id)
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": "Bearer {}".format(access_token),
                                     "limit": "50"})
    match response.status_code:
        case 200: pass
        case _: raise APIError(response.status_code)
    albums = []
    for album in response.json()["items"]:
        albums.append(album["id"])
    return (albums)
