import requests
from ...utilities.tokens import access_token
from ...utilities.exceptions import ErrorException


def main(artist_id):
    query = "https://api.spotify.com/v1/artists/{}/albums".format(artist_id)
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": "Bearer {}".format(access_token)})
    match response.status_code:
        case 200: albums = response.json()
        case _: raise ErrorException(response.status_code)
    albums_final = []
    for album in albums["items"]:
        albums_final = albums_final + [album["id"]]
    print(albums_final)


main("5zixe6AbgXPqt4c1uSl94L")
