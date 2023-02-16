import cli.prompts as prompts
import cli.search as search
import classes
import env as env


class CLI(object):

    def __init__(self):
        print("If you want to see all tracks or albums of an artist in the terminal, it is recommended to maximize the window.")
        print("In order to make API requests, you need to create a Spotify application. Checking for saved credentials...")

    def get_credentials(self):
        if env.check_for_credentials():
            print("Credentials found.")
            self.client_id, self.client_secret = env.retrieve_credentials()
        else:
            print(
                "No credentials found. Please enter your client ID and client secret.")
            self.client_id, self.client_secret = env.enter_credentials()
        self.get_token()

    def get_token(self):
        print("Trying to get token...")
        try:
            self.token = env.get_token(self.client_id, self.client_secret)
        except:
            print(
                "Could not retrieve token. Please check your credentials and enter them again.")
            self.client_id, self.client_secret = env.enter_credentials()
            self.get_token()
        else:
            print("Token successfully retrieved.")
            self.get_search_method()

    def get_search_method(self):
        self.type = search.search_method(self.token)
        if self.type == "id":
            self.search_by_id()
        elif self.type == "name":
            self.get_type()

    def search_by_id(self):
        search.search_by_id(self.token)

    def get_type(self):
        self.type = search.ask_for_type()
        self.search()

    def search(self):
        if self.type == "track":
            self.object = search.search_for_track(self.token)
        elif self.type == "artist":
            self.object = search.search_for_artist(self.token)
        elif self.type == "album":
            self.object = search.search_for_album(self.token)
        self.get_action()

    def get_action(self):
        # if self.type == "track":
        # self.action = actions.actions_track(self.object)
        if self.type == "artist":
            self.action = prompts.actions_artist(self.object)
        # elif self.type == "album":
            # self.action = actions.actions_album(self.object)
        self.perform_action()

    def perform_action(self):
        if self.type == "artist":
            assert isinstance(self.object, classes.Artist)
            if self.action == "print_info":
                self.object.print_artist_info()
            elif self.action == "print_albums":
                self.object.print_albums()
            elif self.action == "print_tracks":
                self.object.print_tracks()
        elif self.type == "album":
            pass
        elif self.type == "track":
            pass
        self.continue_prompt()

    def continue_prompt(self):
        next = prompts.continue_prompt()
        if next == "exit":
            exit()
        elif next == "new_search":
            self.get_search_method()
        elif next == "new_command":
            self.get_action()
