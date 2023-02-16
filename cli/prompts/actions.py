from .continue_prompt import continue_prompt


def actions_artist(artist):

    # Ask user for input as long as no valid input has been provided
    valid = False

    while valid is False:

        prompt = input(
            "What would you like to do? (print_info/print_albums/print_tracks): ")

        if (prompt != "print_info") and (prompt != "print_albums") and (prompt != "print_tracks"):
            print("Invalid input.")

        # Perform action based on input
        else:
            valid = True
            if prompt == "print_info":
                artist.print_artist_info()
            elif prompt == "print_albums":
                artist.print_albums()
            elif prompt == "print_tracks":
                artist.print_tracks()
