import classes as c
import env as env

client_id = input("Enter your client ID: ")
client_token = input("Enter your client secret: ")

auth_token = env.get_token(client_id, client_token)

ConnorPrice = c.Artist(name="Connor Price",
                       id="5zixe6AbgXPqt4c1uSl94L", token=auth_token)
MalikHarris = c.Artist(name="Malik Harris",
                       id="7B6Uk58O2DVfg1xZPKEp4n", token=auth_token)
ImagineDragons = c.Artist(name="Imagine Dragons",
                          id="53XhwfbYqKCa1cC15pYq2q", token=auth_token)

MalikHarris.fetch_albums()
MalikHarris.fetch_tracks()
