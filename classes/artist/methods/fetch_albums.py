import requests

from api.exceptions import APIError
from tokens import access_token


def main(artist_id):

    # Create variables
    albums = []
    limit_reached = False
    counter = 0

    # Fetch albums until there are no more albums to be fetched
    while limit_reached == False:

        # Send a request to the Spotify API
        query = f"https://api.spotify.com/v1/artists/{artist_id}/albums?offset={counter}&limit=50"
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": f"Bearer {access_token}"})
        # Check if the request was successful
        match response.status_code:
            case 200: pass
            case _: raise APIError(response.status_code)

        # Add the albums to the list
        for album in response.json()["items"]:
            albums.append(album["id"])

        # Check if there are more albums to fetch
        if response.json()["next"] == None:
            limit_reached = True
        else:
            counter += 50

    return (albums)
