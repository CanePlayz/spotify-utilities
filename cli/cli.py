import cli.prompts as prompts
import cli.search as search
import classes
import env as env
from typing import Optional


class CLI(object):
    """The main class of the CLI. It is responsible for the main loop and the flow of the program."""

    def __init__(self):
        """Initialize the CLI."""
        self.client_id: str = ""
        self.client_secret: str = ""
        self.token: str = ""  # This is the token that is used to make API requests
        self.type: str = ""  # This is the type of object the user wants to work with
        self.track: Optional[
            classes.Track
        ] = None  # This is the current track the user wants to work with
        self.artist: Optional[
            classes.Artist
        ] = None  # This is the current artist the user wants to work with
        self.album: Optional[
            classes.Album
        ] = None  # This is the current album the user wants to work with
        self.action = None  # This is the action the user currently wants to perform
        print(
            "If you want to see all tracks or albums of an artist in the terminal, it is recommended to maximize the window."
        )
        print(
            "In order to make API requests, you need to create a Spotify application. Checking for saved credentials..."
        )

    def get_credentials(self):
        """Get the credentials from files or user input."""
        # Check if credentials are saved and try to receive them
        if env.check_for_credentials():
            print("Credentials found.")
            try:
                self.client_id, self.client_secret = env.retrieve_credentials()
            except:
                print("Could not retrieve credentials. Please enter them again.")

        # If no credentials are saved, ask the user for them
        else:
            print(
                "No credentials found. Please enter your Client ID and Client Secret."
            )
            env.enter_credentials()
            self.client_id, self.client_secret = env.retrieve_credentials()

        # Continue by getting the token
        self.get_token()

    def get_token(self):
        """Receive the token from Spotify's API."""
        # Try to get the token, if the token cannot be retrieved, ask the user for their credentials again
        print("Trying to get token...")
        try:
            self.token = env.get_token(self.client_id, self.client_secret)
        except:
            print(
                "Could not retrieve token. Please check your credentials and enter them again."
            )
            env.enter_credentials()
            self.client_id, self.client_secret = env.retrieve_credentials()
            self.get_token()
        else:
            print("Token successfully retrieved.")

            # Continue by asking the user for the search method they want to use
            self.get_search_method()

    def get_search_method(self):
        """Ask the user for the search method they want to use."""
        # Ask user for input
        self.type = search.search_method(self.token)
        if self.type == "By ID":
            self.search_by_id()
        elif self.type == "By name":
            self.search_by_name()

    def search_by_id(self):
        """Search for an artist, album or track by ID."""
        search.search_by_id(self.token)

    def search_by_name(self):
        """Search for an artist, album or track by name."""
        # Ask the user what they want to search for
        self.type = search.ask_for_type()

        # Search for the object
        if self.type == "Track":
            self.track = search.search_for_tracks(self.token)
            if not self.track:
                self.get_search_method()
        elif self.type == "Artist":
            self.artist = search.search_for_artists(self.token)
            if not self.artist:
                self.get_search_method()
        elif self.type == "Album":
            self.album = search.search_for_albums(self.token)
            if not self.album:
                self.get_search_method()

        # Continues by asking the user which action they want to perform
        self.get_action()

    def get_action(self):
        """Ask the user which action they want to perform."""
        if self.type == "Track":
            pass
        elif self.type == "Artist":
            self.action = prompts.actions_artist(self.artist)
        elif self.type == "Album":
            self.action = prompts.actions_album(self.album)

        self.perform_action()

    def perform_action(self):
        if self.type == "Track":
            pass
        elif self.type == "Artist":
            if self.artist:
                if self.action == "Print info":
                    self.artist.print_artist_info()
                elif self.action == "Print albums":
                    self.artist.print_albums()
                elif self.action == "Print tracks":
                    self.artist.print_tracks()
        elif self.type == "Album":
            if self.album:
                if self.action == "Print info":
                    self.album.print_album_info()
                elif self.action == "Print tracks":
                    self.album.print_tracks()
        self.continue_prompt()

    def continue_prompt(self):
        next = prompts.continue_prompt()
        if next == "Exit":
            exit()
        elif next == "New Search":
            self.get_search_method()
        elif next == "New command":
            self.get_action()
