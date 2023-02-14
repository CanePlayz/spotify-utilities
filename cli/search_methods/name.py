import requests
from terminaltables import SingleTable

import classes as c
import env as env
import actions as a


def name(token):

    valid = False
    type = ""

    while valid == False:

        type = input(
            "Search for track, artist, or album? (track/artist/album): ")

        if type != "track" and type != "artist" and type != "album":
            print("Invalid input.")
        else:
            valid = True

    name = input(f"Enter the name of the {type}: ")

    query = f"https://api.spotify.com/v1/search?q={name}&type={type}"
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": f"Bearer {token}"})

    # Check if there are any results
    if len(response.json()[f"{type}s"]["items"]) == 0:
        print("Nothing could be found.")
    else:

        # Search results for tracks
        i = 1
        results = [["#", "Name", "Artist"]]

        if type == "track":

            print("Search results:")

            for item in response.json()[f"{type}s"]["items"]:
                results.append(
                    [str(i), item["name"], item["artists"][0]["name"]])
                i += 1

            print(SingleTable(results).table)

            print("Which song would you like to work with? ")

        # Search results for artists
        elif type == "artist":

            i = 1
            results = [["#", "Name"]]

            print("Search results:")

            for item in response.json()[f"{type}s"]["items"]:
                results.append([str(i), item["name"]])
                i += 1

            print(SingleTable(results).table)

            pos = int(input("Which artist would you like to work with? "))
            artist = c.Artist(response.json()["artists"]["items"][pos - 1]["name"],
                              response.json()[f"{type}s"]["items"][pos - 1]["id"], token)

            a.actions_artist(artist)

        # Search results for albums
        elif type == "album":

            i = 1
            results = [["#", "Name", "Artist"]]

            print("Search results:")

            for item in response.json()[f"{type}s"]["items"]:
                results.append(
                    [str(i), item["name"], item["artists"][0]["name"]])
                i += 1

            print(SingleTable(results).table)

            print("Which album would you like to work with?")
