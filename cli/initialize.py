import env as env
import cli.methods as m


def main():

    # Check if there are any saved credentials
    if env.check_for_credentials():
        client_id, client_secret = env.get_credentials()
    else:
        client_id = input("Enter your client ID: ")
        client_secret = input("Enter your client secret: ")
        f = open("credentials.txt", "w")
        f.write(client_id + "\n" + client_secret)

    # Try to get a token
    try:
        token = env.get_token(client_id, client_secret)
    except:
        print("Wrong credentials entered.")
    else:

        # Ask user if they want to search by id or name
        valid = False

        while valid == False:

            search_by = input("Search by ID or name? (id/name): ")

            if search_by == "name":
                valid = True
                m.name(token)
            elif search_by == "id":
                valid = True
                m.id(token)
            else:
                print("Invalid input.")
