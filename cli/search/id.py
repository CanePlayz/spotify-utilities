import requests
from terminaltables import SingleTable

import classes as c
import env as env


def search_by_id(token):

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
