from terminaltables import SingleTable


def main(albums):

    # Create table header
    data = [["Album ID", "Album Name", "Artists", "Spotify URL"]]

    # Convert dictionary to list
    for i in albums:

        # Check if album is an actual album
        if albums[i]["type"] == "album":

            row = [albums[i]["id"], albums[i]["name"], ", ".join(
                albums[i]["artists"]), albums[i]["spotify-url"]]
            data.append(row)

    print(SingleTable(data).table)
