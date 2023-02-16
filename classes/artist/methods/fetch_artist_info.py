import requests

from api.exceptions import APIError


def fetch_artist_info(artist_id, token):

    # Create variable
    info = {}

    # Send a request to the Spotify API
    query = f"https://api.spotify.com/v1/artists/{artist_id}"
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": f"Bearer {token}"})

    # Check if the request was successful
    match response.status_code:
        case 200: pass
        case _: raise APIError(response.status_code)

    # Return the response

    info["genres"] = response.json()["genres"]
    info["followers"] = response.json()["followers"]["total"]
    info["popularity"] = response.json()["popularity"]
    info["images"] = [i["url"] for i in response.json()["images"]]
    return (info)
