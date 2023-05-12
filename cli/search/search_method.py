from InquirerPy.prompts import ListPrompt as select
from cli.prompts.style import style


def search_method(token):
    """Ask the user which search method they want to use."""
    # Ask user for input
    method = select(
        message="How would you like to search?",
        choices=["By ID", "By name"],
        instruction="(Use arrow keys)",
        style=style,
    ).execute()

    return method
