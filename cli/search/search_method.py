def search_method(token):
    # Ask user for input as long as no valid input has been provided
    while True:
        method = input("Search by ID or name? (id/name): ")
        valid_inputs = ["id", "name"]
        if any(method == check for check in valid_inputs):
            return (method)
