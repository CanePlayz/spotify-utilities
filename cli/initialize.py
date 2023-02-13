import requests
from terminaltables import SingleTable

import classes as c
import env as env


def main():

    # Check if there are any saved credentials
    if env.check_for_credentials():
        client_id, client_secret = env.get_credentials()
    else:
        client_id = input("Enter your client ID: ")
        client_secret = input("Enter your client secret: ")
        f = open("credentials.txt", "w")
        f.write(client_id + "\n" + client_secret)

    # Try to get a token
    try:
        token = env.get_token(client_id, client_secret)
    except:
        print("Wrong credentials entered.")
    else:

        # Ask user if they want to search by id or name
        valid = False

        while valid == False:

            search_by = input("Search by ID or name? (id/name): ")

            if search_by == "name":
                valid = True
                name(token)
            elif search_by == "id":
                valid = True
                id(token)
            else:
                print("Invalid input.")


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

            artist.print_tracks()

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

            pos = int(input("Which album would you like to work with?"))


def id(token):

    id = input("Enter the ID of the song/artist/album: ")

    # Check for a song

    query = "https://api.spotify.com/v1/tracks/" + id
    response = requests.get(query,
                            headers={"Content-Type": "application/json",
                                     "Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        print("\"{}\" has been found!".format(response.json()["name"]))
    else:

        # Check for an album

        query = "https://api.spotify.com/v1/albums/" + id
        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            print("\"{}\" has been found!".format(response.json()["name"]))
        else:

            # Check for an artist

            query = "https://api.spotify.com/v1/artists/" + id
            response = requests.get(query,
                                    headers={"Content-Type": "application/json",
                                             "Authorization": f"Bearer {token}"})

            if response.status_code == 200:
                print("\"{}\" has been found!".format(
                    response.json()["name"]))
            else:
                print("Nothing could be found.")
