import requests

from api.exceptions import APIError


def fetch_tracks(artist, albums, token):

    # Create variables
    tracks = {}
    counter = 0

    # Fetch tracks for each album
    for i in albums:

        # Send a request to the Spotify API
        query = "https://api.spotify.com/v1/albums/{}/tracks".format(
            albums[i]["id"])
        response = requests.get(query,
                                headers={"Authorization": f"Bearer {token}"})

        # Check if the request was successful
        match response.status_code:
            case 200: pass
            case _: raise APIError(response.status_code)

        # Add the tracks
        for track in response.json()["items"]:

            # Check for each artist attribute of the track if it matches the name of the desired artist (filter out tracks from collaboration albums)
            if any(artist_to_check["name"] == artist for artist_to_check in track["artists"]):

                # Check if this song is already in the list (filter out duplicates)
                if not (any(possible_duplicate["name"].casefold() == track["name"].casefold() for possible_duplicate in tracks.values())):

                    # Finally, add the tracks with corresponding data to the tracks dictionary
                    tracks[counter] = {"id": track["id"],
                                       "name": track["name"],
                                       "artists": [i["name"] for i in track["artists"]],
                                       "album": albums[i]["name"],
                                       "length": str(track["duration_ms"] // 60000) + ":" + str(int((track["duration_ms"] % 60000) / 1000)).zfill(2) + " min",
                                       "spotify-url": track["external_urls"]["spotify"]
                                       }
                    counter += 1

    return (tracks)
