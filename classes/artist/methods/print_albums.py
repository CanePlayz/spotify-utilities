from terminaltables import SingleTable

import utilities.short_strings as short


def print_albums(albums):

    # Create table header
    data = [["Name", "Artists", "ID", "Spotify URL"]]

    # Convert dictionary to list
    for album in albums.values():

        # Check if the album object is an actual album
        if album["type"] == "album":

            row = [album["name"],
                   ", ".join(album["artists"]),
                   album["id"],
                   album["spotify-url"]]

            data.append(row)

    print(SingleTable(data).table)
