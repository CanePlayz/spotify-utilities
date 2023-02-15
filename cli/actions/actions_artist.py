def actions_artist(artist):
    valid = False

    while valid is False:

        prompt = input(
            "What would you like to do? (print_albums/print_tracks): ")

        if prompt != "print_albums" and prompt != "print_tracks":
            print("Invalid input.")
        else:
            valid = True
            if prompt == "print_albums":
                artist.print_albums()
            elif prompt == "print_tracks":
                artist.print_tracks()
