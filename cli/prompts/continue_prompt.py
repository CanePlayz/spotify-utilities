from InquirerPy.prompts import ListPrompt as select

from cli.prompts.style import style


def continue_prompt():
    # Ask user for input
    proceed = select(
        message="How would you like to continue?",
        choices=["New search", "New command", "Exit"],
        instruction="(Use arrow keys)",
        style=style,
    ).execute()

    return proceed
