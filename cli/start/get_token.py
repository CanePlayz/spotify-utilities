import env


def get_token(client_id, client_secret):
    try:
        token = env.get_token(client_id, client_secret)
    except:
        print("Wrong credentials entered.")
        return (None)
    else:
        return (token)
