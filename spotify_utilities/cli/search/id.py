import requests
from classes import *


def search_for_album_by_id(token: str):
    _id = input(f"Enter the ID of the album: ")

    query = f"https://api.spotify.com/v1/albums/{_id}"
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    result = response.json()
    name = result["name"]
    if response.status_code == 200:
        print(f"'{name}' has been found!")

    album = Album(name, _id, token)
    return album


def search_for_artist_by_id(token: str):
    _id = input(f"Enter the ID of the artist: ")

    query = f"https://api.spotify.com/v1/artists/{_id}"
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    result = response.json()
    name = result["name"]
    if response.status_code == 200:
        print(f"'{name}' has been found!")

    artist = Artist(name, _id, token)
    return artist


def search_for_track_by_id(token: str):
    _id = input(f"Enter the ID of the track: ")

    query = f"https://api.spotify.com/v1/tracks/{_id}"
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
    result = response.json()
    name = result["name"]
    if response.status_code == 200:
        print(f"'{name}' has been found!")

    track = Track(name, _id, token)
    return track
