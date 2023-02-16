def continue_prompt():

    # Ask user for input as long as no valid input has been provided
    valid = False

    while valid is False:

        prompt = input(
            "How would you like to continue? (exit/new_search/new_command): ")

        if (prompt == "exit") and (prompt == "new_search") and (prompt == "new_command"):
            return (prompt)
        else:
            print("Invalid input.")
