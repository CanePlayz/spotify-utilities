from terminaltables import SingleTable

import utilities.short_strings as short


def main(albums):

    # Create table header
    data = [["Name", "Artists", "ID", "Spotify URL"]]

    # Convert dictionary to list
    for i in albums:

        # Check if album is an actual album
        if albums[i]["type"] == "album":

            row = [albums[i]["name"],
                   ", ".join(albums[i]["artists"]),
                   albums[i]["id"],
                   albums[i]["spotify-url"]]

            data.append(row)

    print(SingleTable(data).table)
