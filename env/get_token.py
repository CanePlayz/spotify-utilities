import base64

import requests


def get_token(client_id, client_secret):
    b64_token = base64.b64encode(
        f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    query = "https://accounts.spotify.com/api/token"
    response = requests.post(query,
                             data={"grant_type": "client_credentials"},
                             headers={"Content-Type": "application/x-www-form-urlencoded",
                                      "Authorization": f"Basic {b64_token}"})
    return (response.json()["access_token"])
