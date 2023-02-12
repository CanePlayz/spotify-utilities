import requests

import classes as c
import env as env


def start():

    # Check if there are saved credentials

    if env.check_for_credentials():
        client_id, client_secret = env.get_credentials()
    else:
        client_id = input("Enter your client ID: ")
        client_secret = input("Enter your client secret: ")
        f = open("credentials.txt", "w")
        f.write(client_id + "\n" + client_secret)

    id = input("Enter the ID of the song/artist/album: ")

    # Try to get a token

    try:
        token = env.get_token(client_id, client_secret)
    except:
        print("Wrong credentials entered.")
    else:

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
