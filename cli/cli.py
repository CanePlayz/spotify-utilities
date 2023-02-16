import cli.prompts as prompts
import cli.search as search
import cli.start as start


class CLI(object):

    def get_credentials(self):
        self.client_id, self.client_secret = start.get_credentials()
        self.get_token()

    def get_token(self):
        print("Trying to get token...")
        self.token = start.get_token(self.client_id, self.client_secret)
        if self.token == None:
            self.get_credentials()
            self.get_token()
        else:
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
        self.continue_prompt()

    def continue_prompt(self):
        next = prompts.continue_prompt()
        if next == "exit":
            exit()
        elif next == "new_search":
            self.search_method()
        elif next == "new_command":
            self.get_action()
