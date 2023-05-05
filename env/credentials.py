import base64

import requests
from cryptography.fernet import Fernet

import api.exceptions as exceptions


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


def enter_credentials():
    """Prompts the user to enter their client ID and client secret."""
    # Prompt the user to enter their client ID and client secret
    client_id = input("Enter your client ID: ")
    client_secret = input("Enter your client secret: ")

    # Check if the user entered a client ID and client secret
    if not client_id.strip() or not client_secret.strip():
        print("Error: Invalid client ID or secret.")
        return

    # Generate a key to encrypt the credentials
    key = Fernet.generate_key()
    save_fernet_key(key)

    # Encrypt the credentials
    fernet = Fernet(key)
    credentials = f"{client_id}:{client_secret}"
    encrypted_credentials = fernet.encrypt(credentials.encode())

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

    # Split the credentials into client ID and secret
    client_id, client_secret = decrypted_credentials.split(":")
    return client_id, client_secret


def get_token(client_id, client_secret):
    """Retrieves the access token from Spotify's API."""
    # Prepare the client ID and client secret for the request
    client_credentials = f"{client_id}:{client_secret}"
    b64_token = base64.b64encode(client_credentials.encode()).decode()

    # Make request to Spotify's API
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {b64_token}",
        },
    )

    # Return the response
    if response.status_code != 200:
        raise exceptions.APIError(response.status_code)
    return response.json()["access_token"]
