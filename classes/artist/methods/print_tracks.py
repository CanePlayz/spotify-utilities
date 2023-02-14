from terminaltables import SingleTable

import utilities.short_strings as short


def main(tracks):

    # Create table header
    data = [["Name", "Artists",
             "Album", "Length", "ID", "Spotify URL"]]

    # Convert dictionary to list
    for i in tracks:

        # Limit the number of artists to 4
        artists_limited = []
        if len(tracks[i]["artists"]) > 4:
            limit = 4
        else:
            limit = len(tracks[i]["artists"])
        for j in range(0, limit):
            artists_limited.append(tracks[i]["artists"][j])

        row = [short.track(tracks[i]["name"]),
               ", ".join(artists_limited), tracks[i]["album"],
               tracks[i]["length"],
               tracks[i]["id"],
               tracks[i]["spotify-url"]]

        data.append(row)

    print(SingleTable(data).table)
