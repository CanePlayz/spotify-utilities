import requests

from api.exceptions import APIError
from tokens import access_token


def main(artist_id):
    query = "https://api.spotify.com/v1/artists/{}/albums".format(artist_id)
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": "Bearer {}".format(access_token)})
    match response.status_code:
        case 200: albums = response.json()
        case _: raise APIError(response.status_code)
    albums_final = []
    for album in albums["items"]:
        albums_final = albums_final + album["id"]
    print(albums_final)
    return (albums_final)
