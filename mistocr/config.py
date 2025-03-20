"""
Configuration module for mistocr.

Handles secure storage and retrieval of API keys using keyring.
"""

import os
import keyring
import getpass
from pathlib import Path

# Constants
SERVICE_NAME = "mistocr"
API_KEY_NAME = "mistral_api_key"
CONFIG_DIR = Path.home() / ".config" / "mistocr"


def ensure_config_dir():
    """Ensure the config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def get_api_key():
    """
    Get the Mistral API key.
    
    First checks environment variable, then keyring.
    Returns None if not found.
    """
    # Check environment variable first
    api_key = os.environ.get("MISTRAL_API_KEY")
    if api_key:
        return api_key
    
    # Check keyring
    api_key = keyring.get_password(SERVICE_NAME, API_KEY_NAME)
    return api_key


def store_api_key(api_key):
    """
    Store the Mistral API key securely.
    
    Args:
        api_key: The API key to store
    """
    ensure_config_dir()
    keyring.set_password(SERVICE_NAME, API_KEY_NAME, api_key)
    return True


def prompt_for_api_key():
    """Prompt the user for their API key and store it."""
    print("Mistral API key not found. You'll only need to enter this once.")
    api_key = getpass.getpass("Enter your Mistral API key: ")
    
    if api_key:
        store_api_key(api_key)
        print("API key stored securely.")
        return api_key
    return None


def ensure_api_key():
    """
    Ensure we have an API key, prompting if necessary.
    
    Returns:
        str: The API key
    """
    api_key = get_api_key()
    if not api_key:
        api_key = prompt_for_api_key()
    return api_key 