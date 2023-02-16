import base64

import requests


def check_for_credentials():
    try:
        with open("credentials.txt", "r") as f:
            return True
    except FileNotFoundError:
        return False


def enter_credentials():
    client_id = input("Enter your client ID: ")
    client_secret = input("Enter your client secret: ")
    with open("credentials.txt", "w") as f:
        f.write(client_id + "\n" + client_secret)
    return client_id, client_secret


def retrieve_credentials():
    with open("credentials.txt", "r") as f:
        return f.read().splitlines()


def get_token(client_id, client_secret):
    b64_token = base64.b64encode(
        f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    query = "https://accounts.spotify.com/api/token"
    response = requests.post(query,
                             data={"grant_type": "client_credentials"},
                             headers={"Content-Type": "application/x-www-form-urlencoded",
                                      "Authorization": f"Basic {b64_token}"})
    return (response.json()["access_token"])
