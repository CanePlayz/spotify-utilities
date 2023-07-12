import classes
import cli.prompts as prompts
import cli.search as search
from api.credentials import *
from api.token import *


class CLI:
    """The main class of the CLI. It is responsible for the main loop and the flow of the program."""

    def __init__(self):
        """Initialize the CLI."""
        self.client_id: str = ""
        self.client_secret: str = ""
        self.token: str = ""  # The token that is used to make API requests
        self.search_type: str = ""  # The search method the user wants to use
        self.type: str = ""  # The type of object the user wants to work with
        self.track: classes.Track | None = (
            None  # The current track the user wants to work with
        )
        self.artist: classes.Artist | None = (
            None  # The current artist the user wants to work with
        )
        self.album: classes.Album | None = (
            None  # The current album the user wants to work with
        )
        self.action = None  # The action the user currently wants to perform
        print(
            "If you want to see all tracks or albums of an artist in the terminal, it is recommended to maximize the window."
        )
        print(
            "In order to make API requests, you need to create a Spotify application. Checking for saved credentials..."
        )

    def get_credentials(self):
        """Get the credentials from files or user input."""
        # Check if credentials are saved and try to receive them
        if check_for_credentials():
            print("Credentials found.")
            try:
                self.client_id, self.client_secret = retrieve_credentials()
            except:
                print("Could not retrieve credentials. Please enter them again.")

        # If no credentials are saved, ask the user for input
        else:
            print(
                "No credentials found. Please enter your Client ID and Client Secret."
            )
            enter_credentials()
            self.client_id, self.client_secret = retrieve_credentials()

        # Continue by getting the token
        self.get_token()

    def get_token(self):
        """Receive the token from Spotify's API."""
        # Try to get the token, if the token cannot be retrieved, ask the user for their credentials again
        print("Trying to get token...")
        try:
            self.token = get_token(self.client_id, self.client_secret)
        except:
            print(
                "Could not retrieve token. Please check your credentials and enter them again."
            )
            enter_credentials()
            self.client_id, self.client_secret = retrieve_credentials()
            self.get_token()
        else:
            print("Token successfully retrieved.")

            # Continue by asking the user for the search method they want to use
            self.ask_for_type()

    def ask_for_type(self):
        self.type = search.ask_for_type()
        self.get_search_method()

    def get_search_method(self):
        """Ask the user for the search method they want to use."""
        # Ask user for input
        self.search_type = search.search_method(self.token)
        if self.search_type == "By ID":
            self.search_by_id()
        elif self.search_type == "By name":
            self.search_by_name()

    def search_by_id(self):
        """Search for an artist, album or track by ID."""
        if self.type == "Album":
            self.album = search.search_for_album_by_id(self.token)
        elif self.type == "Artist":
            self.artist = search.search_for_artist_by_id(self.token)
        elif self.type == "Track":
            self.track = search.search_for_track_by_id(self.token)
        self.get_action()

    def search_by_name(self):
        """Search for an artist, album or track by name."""

        # Search for the object
        if self.type == "Track":
            self.track = search.search_for_tracks(self.token)
            if not self.track:
                self.ask_for_type()
        elif self.type == "Artist":
            self.artist = search.search_for_artists(self.token)
            if not self.artist:
                self.ask_for_type()
        elif self.type == "Album":
            self.album = search.search_for_albums(self.token)
            if not self.album:
                self.ask_for_type()

        # Continues by asking the user which action they want to perform
        self.get_action()

    def get_action(self):
        """Ask the user which action they want to perform."""
        if self.type == "Track":
            self.action = prompts.actions_track()
        elif self.type == "Artist":
            self.action = prompts.actions_artist()
        elif self.type == "Album":
            self.action = prompts.actions_album()

        self.perform_action()

    def perform_action(self):
        if self.type == "Album":
            if self.album:
                if self.action == "Print info":
                    self.album.print_album_info()
                elif self.action == "Print tracks":
                    self.album.print_tracks()
        elif self.type == "Artist":
            if self.artist:
                if self.action == "Print info":
                    self.artist.print_artist_info()
                elif self.action == "Print albums":
                    self.artist.print_albums()
                elif self.action == "Print tracks":
                    self.artist.print_tracks()
        elif self.type == "Track":
            if self.track:
                if self.action == "Print info":
                    self.track.print_track_info()
        self.continue_prompt()

    def continue_prompt(self):
        """Ask the user how they want to continue."""
        next = prompts.continue_prompt()
        if next == "New command":
            self.get_action()
        elif next == "New search":
            self.ask_for_type()
        elif next == "Exit":
            print("Exiting...")
            exit()
