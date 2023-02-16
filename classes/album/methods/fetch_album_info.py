import requests

from api.exceptions import APIError


def fetch_album_info(album_id, token):

    # Create variable
    info = {}

    # Send a request to the Spotify API
    query = f"https://api.spotify.com/v1/albums/{album_id}"
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": f"Bearer {token}"})

    # Check if the request was successful
    match response.status_code:
        case 200: pass
        case _: raise APIError(response.status_code)

    # Return the response

    info["release_date"] = response.json()["release_date"]
    info["artists"] = [i["name"] for i in response.json()["artists"]]
    info["album_type"] = response.json()["album_type"].capitalize()
    info["total_tracks"] = response.json()["total_tracks"]
    info["genres"] = response.json()["genres"]
    info["popularity"] = response.json()["popularity"]
    info["label"] = response.json()["label"]
    info["images"] = [i["url"] for i in response.json()["images"]]
    info["copyright"] = [i["text"] for i in response.json()["copyrights"]]
    # info["isrc"] = response.json()["external_ids"]["isrc"]
    # info["ean"] = response.json()["external_ids"]["ean"]
    # info["upc"] = response.json()["external_ids"]["upc"]
    return (info)
