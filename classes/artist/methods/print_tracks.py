from terminaltables import SingleTable

import utilities.short_strings as short


def print_tracks(tracks):
    # Create table header
    data = [["Name", "Artists", "Length", "Album", "ID", "Spotify URL"]]

    # Convert dictionary to list
    for track in tracks.values():
        row = [
            short.shorten_track(track["name"]),
            short.shorten_artists(", ".join(track["artists"])),
            track["length"],
            short.shorten_album(track["album"]),
            track["id"],
            track["spotify-url"],
        ]

        data.append(row)

    print(SingleTable(data).table)
