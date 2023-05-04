from terminaltables import SingleTable

import utilities.short_strings as short


def print_tracks(tracks: dict):
    """Prints a table of tracks to the terminal."""
    # Create table header
    data = [["Name", "Artists", "Length", "ID", "Spotify URL"]]

    # Convert dictionary to list
    for track in tracks.values():
        row = [
            short.shorten_track(track["name"]),
            short.shorten_artists(", ".join(track["artists"])),
            track["length"],
            track["id"],
            track["spotify-url"],
        ]
        data.append(row)

    # Print table to terminal
    print(SingleTable(data).table)
