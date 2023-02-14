import requests

from api.exceptions import APIError


def main(name, albums, token):

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
            nu_artists = len(track["artists"])
            for i in range(0, nu_artists):
                if track["artists"][i]["name"] == name:

                    # Check if this song is already in the list (filter out duplicates)
                    dupl = False
                    for possible_duplicate in tracks:
                        if tracks[possible_duplicate]["name"].casefold() == track["name"].casefold():
                            dupl = True
                            break

                    # Finally, add the track to the list
                    if not dupl:
                        tracks[counter] = {"id": track["id"],
                                           "name": track["name"],
                                           "artists": [track["artists"][i]["name"] for i in range(0, nu_artists)],
                                           "album": albums[i]["name"],
                                           "length": str(track["duration_ms"] // 60000) + ":" + str(int((track["duration_ms"] % 60000) / 1000)) + " min",
                                           "spotify-url": track["external_urls"]["spotify"]
                                           }
                        counter += 1

    return (tracks)
