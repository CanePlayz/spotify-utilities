from terminaltables import SingleTable

import utilities.short_strings as short


def main(tracks):

    # Create table header
    data = [["Name", "Artists", "Length",
             "Album", "ID", "Spotify URL"]]

    # Convert dictionary to list
    for i in tracks:

        row = [short.track(tracks[i]["name"]),
               short.artists(", ".join(tracks[i]["artists"])),
               tracks[i]["length"],
               short.album(tracks[i]["album"]),
               tracks[i]["id"],
               tracks[i]["spotify-url"]]

        data.append(row)

    print(SingleTable(data).table)
