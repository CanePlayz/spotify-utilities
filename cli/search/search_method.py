def search_method(token):
    valid = False
    while valid is False:
        prompt = input("Search by ID or name? (id/name): ")
        if (prompt == "id") or (prompt == "name"):
            valid = True
            return (prompt)
