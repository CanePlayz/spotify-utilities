from .continue_prompt import continue_prompt
from InquirerPy.prompts import ListPrompt as select
from cli.prompts.style import style


def actions_album():
    """Ask user for input on what to do with the album object."""
    # Ask user for input
    selected_action = select(
        message="What would you like to do?",
        choices=["Print info", "Print tracks"],
        instruction="(Use arrow keys)",
        style=style,
    ).execute()

    return selected_action


def actions_artist():
    """Ask user for input on what to do with the artist object."""
    # Ask user for input
    selected_action = select(
        message="What would you like to do?",
        choices=["Print info", "Print albums", "Print tracks"],
        instruction="(Use arrow keys)",
        style=style,
    ).execute()

    return selected_action


def actions_track():
    """Ask user for input on what to do with the track object."""
    # Ask user for input
    selected_action = select(
        message="What would you like to do?",
        choices=["Print info"],
        instruction="(Use arrow keys)",
        style=style,
    ).execute()

    return selected_action
