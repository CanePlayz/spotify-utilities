def print_album_info(name, id, url, info):
    print(f"Name: {name}")
    print(f"ID: {id}")
    print(f"Spotify URL: {url}")
    if info["release_date"] == None:
        print("Release date: Unknown")
    else:
        print(f"Release date: {info['release_date']}")
    print(f"Artists: {', '.join(info['artists'])}")
    print(f"Album type: {info['album_type']}")
    print(f"Total tracks: {info['total_tracks']}")
    if info["genres"] == []:
        print("Genres: Unknown")
    else:
        print("Genres: {}".format(", ".join(info["genres"])))
    print(f"Popularity: {info['popularity']}")
    if info["label"] == None:
        print("Label: Unknown")
    else:
        print(f"Label: {info['label']}")
    if info["images"] == []:
        print("Images: Unknown")
    else:
        print(f"Images: {', '.join(info['images'])}")
    if info["copyright"] == []:
        print("Copyright: Unknown")
    else:
        print(f"Copyright: {', '.join(info['copyright'])}")
    # if info["isrc"] == "":
    #     print("ISRC: Unknown")
    # else:
    #     print(f"ISRC: {info['isrc']}")
    # if info["ean"] == "":
    #     print("EAN: Unknown")
    # else:
    #     print(f"EAN: {info['ean']}")
    # if info["upc"] == "":
    #     print("UPC: Unknown")
    # else:
    #     print(f"UPC: {info['upc']}")
