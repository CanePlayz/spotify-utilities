import env


def get_credentials():
    # Check if there are any saved credentials
    if env.check_for_credentials():
        client_id, client_secret = env.get_credentials()
        return (client_id, client_secret)
    else:
        print("If you want to see all tracks or albums of an artist in the terminal, it is recommended to maximize the window.")
        print("In order to make API requests, you need to create a Spotify application.")
        client_id = input("Enter your client ID: ")
        client_secret = input("Enter your client secret: ")
        f = open("credentials.txt", "w")
        f.write(client_id + "\n" + client_secret)
        return (client_id, client_secret)
