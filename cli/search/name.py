import requests
from terminaltables import SingleTable

import classes as c
import env as env


def ask_for_type():
    # Ask user for input as long as no valid input has been provided
    while True:

        type = input(
            "Search for track, artist, or album? (track/artist/album): ")

        valid_inputs = ["track", "artist", "album"]

        if any(type == check for check in valid_inputs):
            return (type)
        else:
            print("Invalid input.")


def search_for_track(token):
    # Create a list of search results
    results = [["#", "Name", "Artist"]]

    # Send a search request to the Spotify API
    name = input(f"Enter the name of the track: ")
    query = f"https://api.spotify.com/v1/search?q={name}&type=track"
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": f"Bearer {token}"})

    # Check if there are any results
    if len(response.json()[f"{type}s"]["items"]) == 0:
        print("Nothing could be found.")
    else:
        for i, item in enumerate(response.json()["tracks"]["items"]):
            results.append([str(i + 1), item["name"],
                           item["artists"][0]["name"]])

            # Print the search results
            print(SingleTable(results).table)

            # Ask the user which track they want to work with and create an object
            pos = int(input("Which artist would you like to work with? "))
            track = c.Track(response.json()["tracks"]["items"][pos - 1]["name"],
                            response.json()["tracks"]["items"][pos - 1]["id"], token)
            return (track)


def search_for_artist(token):
    # Create a list of search results
    results = [["#", "Name"]]

    # Send a search request to the Spotify API
    name = input(f"Enter the name of the artist: ")
    query = f"https://api.spotify.com/v1/search?q={name}&type=artist"
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": f"Bearer {token}"})

    # Check if there are any results
    if len(response.json()[f"artists"]["items"]) == 0:
        print("Nothing could be found.")
    else:
        for i, item in enumerate(response.json()["artists"]["items"]):
            results.append([str(i + 1), item["name"]])

            # Print the search results
            print(SingleTable(results).table)

            # Ask the user which artist they want to work with and create an object
            pos = int(input("Which artist would you like to work with? "))
            artist = c.Artist(response.json()["artists"]["items"][pos - 1]["name"],
                              response.json()["artists"]["items"][pos - 1]["id"], token)
            return (artist)


def search_for_album(token):
    # Create a list of search results
    results = [["#", "Name", "Artist"]]

    # Send a search request to the Spotify API
    name = input(f"Enter the name of the album: ")
    query = f"https://api.spotify.com/v1/search?q={name}&type=album"
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": f"Bearer {token}"})

    # Check if there are any results
    if len(response.json()[f"{type}s"]["items"]) == 0:
        print("Nothing could be found.")
    else:
        for i, item in enumerate(response.json()["albums"]["items"]):
            results.append([str(i + 1), item["name"],
                           item["artists"][0]["name"]])

            # Print the search results
            print(SingleTable(results).table)

            # Ask the user which album they want to work with and create an object
            pos = int(input("Which artist would you like to work with? "))
            album = c.Album(response.json()["albums"]["items"][pos - 1]["name"],
                            response.json()["albums"]["items"][pos - 1]["id"], token)
            return (album)
