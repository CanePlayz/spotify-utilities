import requests

from api.exceptions import APIError


def main(artist_id, token):

    # Create variables
    albums = {}
    limit_reached = False
    counter = 0

    # Fetch albums until there are no more albums to be fetched
    while limit_reached == False:

        # Send a request to the Spotify API
        query = f"https://api.spotify.com/v1/artists/{artist_id}/albums?offset={counter}&limit=50"
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": f"Bearer {token}"})
        # Check if the request was successful
        match response.status_code:
            case 200: pass
            case _: raise APIError(response.status_code)

        # Add the albums
        for album in response.json()["items"]:
            albums[counter] = {"id": album["id"],
                               "name": album["name"],
                               "artists": [album["artists"][i]["name"] for i in range(0, len(album["artists"]))],
                               # "genres": album["genres"],
                               "spotify-url": album["external_urls"]["spotify"],
                               "type": album["album_type"]
                               }
            counter += 1

        # Check if there are more albums to fetch
        if response.json()["next"] == None:
            limit_reached = True
        else:
            counter += 50

    return (albums)
