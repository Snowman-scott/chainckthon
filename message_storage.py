# message_storage.py
# Message Storage Module - FIXED VERSION

import json
import os
import tempfile
import re
from datetime import datetime

# Optional dependency for file locking
try:
    from filelock import FileLock, Timeout as FileLockTimeout
except Exception:
    FileLock = None
    FileLockTimeout = None

MESSAGE_DIR = "messages"
USER_DIR = "Users"  # Changed from Users.json to Users directory

def setup_messages():
    """Create messages directory if it doesn't exist"""
    os.makedirs(MESSAGE_DIR, exist_ok=True)
    os.makedirs(USER_DIR, exist_ok=True)


def sanitize_username(username):
    """
    Ensure username is safe to embed in a filename.
    Returns a normalized (lowercased) safe username string.
    """
    if not isinstance(username, str):
        raise TypeError(f"username must be a string, got {type(username).__name__}")

    if '/' in username or '\\' in username or '..' in username:
        raise ValueError("username contains path separators or traversal sequences")

    if not re.fullmatch(r"[A-Za-z0-9_-]+", username):
        raise ValueError("username contains invalid characters; allowed: letters, numbers, underscore, hyphen")

    return username.lower()


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
    if not isinstance(message_package, dict):
        raise TypeError(f"message_package must be a dict, got {type(message_package).__name__}")

    required_keys = ['from_user', 'to_user', 'encrypted_message', 'encrypted_key', 'nonce', 'timestamp']
    missing = [k for k in required_keys if k not in message_package]
    if missing:
        raise ValueError(f"message_package is missing required keys: {', '.join(missing)}")

    bad_values = [k for k in required_keys if not isinstance(message_package.get(k), str) or not message_package.get(k).strip()]
    if bad_values:
        raise ValueError(f"The following keys must be non-empty strings: {', '.join(bad_values)}")

    try:
        datetime.fromisoformat(message_package['timestamp'])
    except Exception:
        raise ValueError(f"timestamp is not a valid ISO-8601 string: {message_package.get('timestamp')!r}")

    setup_messages()

    recipient = sanitize_username(message_package['to_user'])
    message_file = os.path.join(MESSAGE_DIR, f"{recipient}.json")

    # Simple file locking if available
    if FileLock is not None:
        lock_path = message_file + ".lock"
        lock_timeout_seconds = 5

        try:
            with FileLock(lock_path, timeout=lock_timeout_seconds):
                _write_message(message_file, message_package)
        except FileLockTimeout:
            raise TimeoutError(f"Could not acquire file lock for {message_file!r} within {lock_timeout_seconds} seconds")
    else:
        # No locking available, write directly
        _write_message(message_file, message_package)


def _write_message(message_file, message_package):
    """Helper function to write message to file"""
    if os.path.exists(message_file):
        try:
            with open(message_file, 'r') as f:
                messages = json.load(f)
        except json.JSONDecodeError:
            messages = []
    else:
        messages = []

    messages.append(message_package)

    # Atomic write using temp file
    target_dir = os.path.dirname(message_file) or "."
    fd, tmp_path = tempfile.mkstemp(prefix="msg_", dir=target_dir, text=True)
    try:
        with os.fdopen(fd, 'w') as tmpf:
            json.dump(messages, tmpf, indent=2)
            tmpf.flush()
            os.fsync(tmpf.fileno())

        os.replace(tmp_path, message_file)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


def get_messages_for_user(username):
    """
    Get all messages for a specific user.
    
    Args:
        username (str): The username to get messages for
    
    Returns:
        list: List of message dictionaries, or empty list if no messages
    """
    setup_messages()

    safe_username = sanitize_username(username)
    message_file = os.path.join(MESSAGE_DIR, f"{safe_username}.json")
    
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
    Get a user's public key from their individual user file.
    
    Args:
        username (str): The username to look up
    
    Returns:
        str: Public key in PEM format, or None if user not found
    """
    user_file = os.path.join(USER_DIR, f"{username}.json")
    
    if not os.path.exists(user_file):
        return None
    
    try:
        with open(user_file, 'r') as f:
            user_data = json.load(f)
        return user_data.get('public_key')
    except (json.JSONDecodeError, KeyError, IOError):
        return None


def get_all_users():
    """
    Get a list of all registered usernames.
    
    Returns:
        list: List of usernames
    """
    if not os.path.exists(USER_DIR):
        return []
    
    try:
        users = []
        for filename in os.listdir(USER_DIR):
            if filename.endswith('.json'):
                username = filename[:-5]  # Remove .json extension
                users.append(username)
        return users
    except Exception:
        return []


def clear_messages_for_user(username):
    """
    Clear all messages for a user (optional utility function).
    
    Args:
        username (str): Username to clear messages for
    """
    safe_username = sanitize_username(username)
    message_file = os.path.join(MESSAGE_DIR, f"{safe_username}.json")

    if os.path.exists(message_file):
        os.remove(message_file)


# ============================================
# DEMO/TEST
# ============================================
"""
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
    try:
        save_message(test_message)
        print("✓ Message saved")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\nRetrieving messages for bob...")
    messages = get_messages_for_user('bob')
    print(f"Found {len(messages)} message(s)")
    
    print("\n✓ Message storage working!")
    """