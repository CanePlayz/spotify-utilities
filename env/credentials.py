from cryptography.fernet import Fernet
from InquirerPy.prompts import ConfirmPrompt as confirm
from InquirerPy.prompts import InputPrompt as text_prompt

from cli.prompts.style import style


def check_for_credentials():
    """Checks if credentials.bin exists in the current directory."""
    try:
        with open("credentials.bin", "rb") as f:
            return True
    except FileNotFoundError:
        return False


def save_fernet_key(key):
    """Saves the Fernet key to a file."""
    with open("fernet_key.key", "wb") as key_file:
        key_file.write(key)


def load_fernet_key():
    """Loads the Fernet key from the file."""
    with open("fernet_key.key", "rb") as key_file:
        return key_file.read()


def save_encrypted_credentials(encrypted_credentials):
    """Saves the encrypted client ID and secret to a file."""
    with open("credentials.bin", "wb") as enc_file:
        enc_file.write(encrypted_credentials)


def load_encrypted_credentials():
    """Loads the encrypted client ID and secret from the file."""
    with open("credentials.bin", "rb") as enc_file:
        return enc_file.read()


def credentials_prompt():
    """Prompts the user to enter their client ID and secret."""
    # Prompt the user to enter their Client ID and Client Secret
    client_id: str = text_prompt(
        message="Please enter your Client ID:",
        style=style,
        validate=lambda result: len(result) == 32,
        invalid_message="Client ID must have a length of 32 characters.",
    ).execute()
    client_secret: str = text_prompt(
        message="Please enter your Client Secret:",
        style=style,
        validate=lambda result: len(result) == 32,
        invalid_message="Client ID must have a length of 32 characters.",
    ).execute()

    # Let the user confirm the credentials
    print(f"Your Client ID: {client_id}")
    print(f"Your Client Secret: {client_secret}")
    proceed = confirm(message="Are these correct?", style=style).execute()
    if not proceed:
        enter_credentials()

    return client_id, client_secret


def encrypt_credentials(client_id: str, client_secret: str):
    """Encrypts the client ID and secret and returns them."""
    # Generate a key to encrypt the credentials
    key = Fernet.generate_key()
    save_fernet_key(key)

    # Encrypt the credentials
    fernet = Fernet(key)
    credentials = f"{client_id}:{client_secret}"
    encrypted_credentials = fernet.encrypt(credentials.encode())

    return encrypted_credentials


def enter_credentials():
    """Prompts the user to enter their Client ID and Client Secret,
    encrypts them and saves them to credentials.bin."""
    # Prompt the user to enter their Client ID and Client Secret
    client_id, client_secret = credentials_prompt()

    # Encrypt the credentials
    encrypted_credentials = encrypt_credentials(client_id, client_secret)

    # Write the encrypted credentials to credentials.bin
    save_encrypted_credentials(encrypted_credentials)


def retrieve_credentials():
    """Retrieves the client ID and client secret from credentials.bin."""
    # Load the files
    key = load_fernet_key()
    encrypted_credentials = load_encrypted_credentials()

    # Decrypt the credentials
    fernet = Fernet(key)
    decrypted_credentials = fernet.decrypt(encrypted_credentials).decode()

    # Try to split the credentials into client ID and secret
    try:
        client_id, client_secret = decrypted_credentials.split(":")
        return client_id, client_secret
    except ValueError:
        raise
