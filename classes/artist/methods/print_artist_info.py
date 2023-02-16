from terminaltables import SingleTable


def print_artist_info(name, id, url, info):
    data = [["Property", "Value"]]
    data.append(["Name", name])
    data.append(["ID", id])
    if info["genres"] == []:
        data.append(["Genres", "Unknown"])
    else:
        data.append(["Genres", (", ".join(info["genres"])).capitalize()])
    data.append(["Followers", info['followers']])
    data.append(["Popularity", info['popularity']])
    data.append(["Image", info['images'][0]])
    data.append(["Spotify URL", url])

    print(SingleTable(data).table)
