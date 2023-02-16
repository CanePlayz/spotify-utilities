import requests

from api.exceptions import APIError


def fetch_tracks(album_id, token):

    # Create variables
    tracks = {}

    # Send a request to the Spotify API
    query = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    response = requests.get(query,
                            headers={"Authorization": f"Bearer {token}"})

    # Check if the request was successful
    match response.status_code:
        case 200: pass
        case _: raise APIError(response.status_code)

    # Add the tracks with corresponding data to the tracks dictionary
    for i, track in enumerate(response.json()["items"]):
        tracks[i + 1] = {"id": track["id"],
                         "name": track["name"],
                         "artists": [i["name"] for i in track["artists"]],
                         "length": str(track["duration_ms"] // 60000) + ":" + str(int((track["duration_ms"] % 60000) / 1000)).zfill(2) + " min",
                         "spotify-url": track["external_urls"]["spotify"]
                         }

    return (tracks)
