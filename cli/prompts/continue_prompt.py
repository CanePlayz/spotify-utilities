def continue_prompt():

    # Ask user for input as long as no valid input has been provided
    while True:

        next = input(
            "How would you like to continue? (exit/new_search/new_command): ")

        valid_inputs = ["exit", "new_search", "new_command"]

        if any(next == check for check in valid_inputs):
            return (next)
        else:
            print("Invalid input.")
