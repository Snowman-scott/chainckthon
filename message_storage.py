# message_storage.py
# Message Storage Module - For your friend to complete

import json
import os
from datetime import datetime

MESSAGE_DIR = "messages"
USER_DB = "Users.json"

def setup_messages():
    """Create messages directory if it doesn't exist"""
    if not os.path.exists(MESSAGE_DIR):
        os.makedirs(MESSAGE_DIR)

def save_message(message_package):
    """
    Save an encrypted message to storage.
    
    Args:
        message_package (dict): Contains:
            - from_user: sender's username
            - to_user: recipient's username
            - encrypted_message: base64 encoded encrypted message
            - encrypted_key: base64 encoded encrypted AES key
            - nonce: base64 encoded nonce
            - timestamp: ISO format timestamp
    """
    setup_messages()
    
    # Create a file for the recipient if it doesn't exist
    recipient = message_package['to_user']
    message_file = os.path.join(MESSAGE_DIR, f"{recipient}.json")
    
    # Load existing messages
    if os.path.exists(message_file):
        with open(message_file, 'r') as f:
            messages = json.load(f)
    else:
        messages = []
    
    # Add new message
    messages.append(message_package)
    
    # Save back to file
    with open(message_file, 'w') as f:
        json.dump(messages, f, indent=2)

def get_messages_for_user(username):
    """
    Get all messages for a specific user.
    
    Args:
        username (str): The username to get messages for
    
    Returns:
        list: List of message dictionaries, or empty list if no messages
    """
    setup_messages()
    
    message_file = os.path.join(MESSAGE_DIR, f"{username}.json")
    
    if not os.path.exists(message_file):
        return []
    
    try:
        with open(message_file, 'r') as f:
            messages = json.load(f)
        return messages
    except json.JSONDecodeError:
        return []

def get_user_public_key(username):
    """
    Get a user's public key from the Users.json database.
    
    Args:
        username (str): The username to look up
    
    Returns:
        str: Public key in PEM format, or None if user not found
    """
    if not os.path.exists(USER_DB):
        return None
    
    try:
        with open(USER_DB, 'r') as f:
            users = json.load(f)
        
        if username in users:
            return users[username]['public_key']
        else:
            return None
    except (json.JSONDecodeError, KeyError):
        return None

def get_all_users():
    """
    Get a list of all registered usernames.
    
    Returns:
        list: List of usernames
    """
    if not os.path.exists(USER_DB):
        return []
    
    try:
        with open(USER_DB, 'r') as f:
            users = json.load(f)
        return list(users.keys())
    except json.JSONDecodeError:
        return []

def clear_messages_for_user(username):
    """
    Clear all messages for a user (optional utility function).
    
    Args:
        username (str): Username to clear messages for
    """
    message_file = os.path.join(MESSAGE_DIR, f"{username}.json")
    
    if os.path.exists(message_file):
        os.remove(message_file)

# ============================================
# DEMO/TEST
# ============================================

if __name__ == "__main__":
    print("=== Message Storage Demo ===")
    setup_messages()
    
    # Test message
    test_message = {
        'from_user': 'alice',
        'to_user': 'bob',
        'encrypted_message': 'test_encrypted_data',
        'encrypted_key': 'test_encrypted_key',
        'nonce': 'test_nonce',
        'timestamp': datetime.now().isoformat()
    }
    
    print("Saving test message...")
    save_message(test_message)
    
    print("Retrieving messages for bob...")
    messages = get_messages_for_user('bob')
    print(f"Found {len(messages)} message(s)")
    
    print("\n✓ Message storage working!")