def print_artist_info(name, id, url, info):
    print(f"Name: {name}")
    print(f"ID: {id}")
    print(f"Spotify URL: {url}")
    if info["genres"] == []:
        print("Genres: Unknown")
    else:
        print("Genres: {}".format(", ".join(info["genres"])))
    print(f"Followers: {info['followers']}")
    print(f"Popularity: {info['popularity']}")
    if info["images"] == []:
        print("Images: Unknown")
    else:
        print(f"Images: {', '.join(info['images'])}")
