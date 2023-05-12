import requests
from terminaltables import SingleTable
from InquirerPy.prompts import ListPrompt as select
from cli.prompts.style import style

import classes as c
import env as env


def ask_for_type():
    """Ask the user for the type of object they want to work with."""
    # Ask user for input
    type = select(
        message="What do you want to search for?",
        choices=["Track", "Artist", "Album"],
        instruction="(Use arrow keys)",
        style=style,
    ).execute()

    return type


def search_for_tracks(token):
    # Create a list of search results
    results = [["#", "Name", "Artist"]]

    # Send a search request to the Spotify API
    name = input(f"Enter the name of the track: ")
    query = f"https://api.spotify.com/v1/search?q={name}&type=track"
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    # Check if there are any results
    if len(response.json()[f"tracks"]["items"]) == 0:
        print("Nothing could be found.")
        return None
    else:
        for i, item in enumerate(response.json()["tracks"]["items"]):
            results.append([str(i + 1), item["name"], item["artists"][0]["name"]])

            # Print the search results
            print(SingleTable(results).table)

            # Ask the user which track they want to work with and create an object
            pos = int(
                input("Which track would you like to work with? (Enter the number): ")
            )
            track = c.Track(
                response.json()["tracks"]["items"][pos - 1]["name"],
                response.json()["tracks"]["items"][pos - 1]["id"],
                token,
            )
            return track


def search_for_artists(token):
    # Create a list of search results
    results = [["#", "Name"]]

    # Send a search request to the Spotify API
    name = input(f"Enter the name of the artist: ")
    query = f"https://api.spotify.com/v1/search?q={name}&type=artist"
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    # Check if there are any results
    if len(response.json()[f"artists"]["items"]) == 0:
        print("Nothing could be found.")
    else:
        for i, item in enumerate(response.json()["artists"]["items"]):
            results.append([str(i + 1), item["name"]])

            # Print the search results
            print(SingleTable(results).table)

            # Ask the user which artist they want to work with and create an object
            pos = int(
                input("Which artist would you like to work with? (Enter the number): ")
            )
            artist = c.Artist(
                response.json()["artists"]["items"][pos - 1]["name"],
                response.json()["artists"]["items"][pos - 1]["id"],
                token,
            )
            return artist


def search_for_albums(token):
    # Create a list of search results
    results = [["#", "Name", "Artist"]]

    # Send a search request to the Spotify API
    name = input(f"Enter the name of the album: ")
    query = f"https://api.spotify.com/v1/search?q={name}&type=album"
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    # Check if there are any results
    if len(response.json()["albums"]["items"]) == 0:
        print("Nothing could be found.")
    else:
        for i, item in enumerate(response.json()["albums"]["items"]):
            results.append([str(i + 1), item["name"], item["artists"][0]["name"]])

            # Print the search results
            print(SingleTable(results).table)

            # Ask the user which album they want to work with and create an object
            pos = int(
                input("Which album would you like to work with? (Enter the number): ")
            )
            album = c.Album(
                response.json()["albums"]["items"][pos - 1]["name"],
                response.json()["albums"]["items"][pos - 1]["id"],
                token,
            )
            return album
