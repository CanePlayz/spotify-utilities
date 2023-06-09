import base64

import requests

import api.exceptions as exceptions


def get_token(client_id, client_secret):
    """Retrieves the access token from Spotify's API."""
    # Prepare the client ID and client secret for the request
    client_credentials = f"{client_id}:{client_secret}"
    b64_token = base64.b64encode(client_credentials.encode()).decode()

    # Make request to Spotify's API
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {b64_token}",
        },
    )

    # Return the response
    if response.status_code != 200:
        raise exceptions.APIError(response.status_code)
    return response.json()["access_token"]
