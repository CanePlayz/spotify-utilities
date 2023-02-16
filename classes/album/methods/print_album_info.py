from terminaltables import SingleTable
import utilities.short_strings as short


def print_album_info(name, id, url, info):
    data = [["Property", "Value"]]
    data.append(["Name", name])
    data.append(["ID", id])
    if info["release_date"] == None:
        data.append(["Release date", "Unknown"])
    else:
        data.append(["Release date", info['release_date']])
    if len(info["artists"]) == 1:
        data.append(["Artist", info['artists'][0]])
    else:
        data.append(["Artists", ', '.join(info['artists'])])
    data.append(["Album type", info['album_type']])
    data.append(["Total tracks", info['total_tracks']])
    if info["genres"] == []:
        data.append(["Genres", "Unknown"])
    else:
        data.append(["Genres", (", ".join(info["genres"])).capitalize()])
    data.append(["Popularity", info['popularity']])
    if info["label"] == None:
        data.append(["Label", "Unknown"])
    else:
        data.append(["Label", info['label']])
    if info["images"] == []:
        data.append(["Cover", "Unknown"])
    else:
        data.append(["Cover", (info['images'][0])])
    if info["copyright"] == []:
        data.append(["Copyright", "Unknown"])
    else:
        data.append(["Copyright", short.copyright(
            ', '.join(info['copyright']))])
    data.append(["Spotify URL", url])

    print(SingleTable(data).table)
