from .continue_prompt import continue_prompt


def actions_artist(artist):

    # Ask user for input as long as no valid input has been provided
    while True:

        action = input(
            "What would you like to do? (print_info/print_albums/print_tracks): ")

        valid_inputs = ["print_info", "print_albums", "print_tracks"]

        if any(action == check for check in valid_inputs):
            return (action)
        else:
            print("Invalid input.")


def actions_album(album):

    # Ask user for input as long as no valid input has been provided
    while True:

        action = input(
            "What would you like to do? (print_info/print_tracks): ")

        valid_inputs = ["print_info", "print_tracks"]

        if any(action == check for check in valid_inputs):
            return (action)
        else:
            print("Invalid input.")
