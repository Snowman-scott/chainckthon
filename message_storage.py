# message_storage.py
# Message Storage Module - For your friend to complete

import json
import os
import tempfile
import re
from datetime import datetime

# Optional dependency used to serialize access to message files so concurrent
# writers don't clobber each other's changes. If missing we raise a clear
# runtime error explaining how to install it.
try:
    from filelock import FileLock, Timeout as FileLockTimeout
except Exception:
    FileLock = None
    FileLockTimeout = None

MESSAGE_DIR = "messages"
USER_DB = "Users.json"

def setup_messages():
    """Create messages directory if it doesn't exist"""
    os.makedirs(MESSAGE_DIR, exist_ok=True)


def sanitize_username(username):
    """
    Ensure username is safe to embed in a filename.

    Rules:
    - Must be a str
    - Must match /^[A-Za-z0-9_-]+$/ (only alphanumeric, underscore, hyphen)
    - Must not contain path separators or traversal sequences

    Returns a normalized (lowercased) safe username string.
    Raises TypeError or ValueError on invalid input.
    """
    if not isinstance(username, str):
        raise TypeError(f"username must be a string, got {type(username).__name__}")

    if '/' in username or '\\' in username or '..' in username:
        raise ValueError("username contains path separators or traversal sequences")

    # Allow only limited safe characters
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
    # Validate incoming package early to avoid KeyError/TypeError later
    if not isinstance(message_package, dict):
        raise TypeError(f"message_package must be a dict, got {type(message_package).__name__}")

    required_keys = ['from_user', 'to_user', 'encrypted_message', 'encrypted_key', 'nonce', 'timestamp']
    missing = [k for k in required_keys if k not in message_package]
    if missing:
        raise ValueError(f"message_package is missing required keys: {', '.join(missing)}")

    # Ensure each required value is a non-empty string
    bad_values = [k for k in required_keys if not isinstance(message_package.get(k), str) or not message_package.get(k).strip()]
    if bad_values:
        raise ValueError(f"The following keys must be non-empty strings: {', '.join(bad_values)}")

    # Verify timestamp is parseable as ISO-8601
    try:
        # datetime.fromisoformat accepts many ISO-8601 variants in Python 3.7+
        datetime.fromisoformat(message_package['timestamp'])
    except Exception:
        raise ValueError(f"timestamp is not a valid ISO-8601 string: {message_package.get('timestamp')!r}")

    setup_messages()

    # Create a file for the recipient if it doesn't exist
    recipient = sanitize_username(message_package['to_user'])
    message_file = os.path.join(MESSAGE_DIR, f"{recipient}.json")

    # Use a file lock to prevent race conditions when multiple processes
    # write concurrently. This requires the 'filelock' package to be
    # installed. If it's not available, raise a helpful runtime error.
    if FileLock is None:
        raise RuntimeError("The 'filelock' package is required for safe concurrent message writes. Install it with: pip install filelock")

    lock_path = message_file + ".lock"
    lock_timeout_seconds = 5

    try:
        with FileLock(lock_path, timeout=lock_timeout_seconds):
            # Load existing messages (tolerate missing or corrupt JSON)
            if os.path.exists(message_file):
                try:
                    with open(message_file, 'r') as f:
                        messages = json.load(f)
                except json.JSONDecodeError:
                    messages = []
            else:
                messages = []

            # Append the incoming message
            messages.append(message_package)

            # Write to a temp file in the same directory then atomically
            # replace the target file to minimize the window where a
            # reader could see a partially-written file.
            target_dir = os.path.dirname(message_file) or "."
            fd, tmp_path = tempfile.mkstemp(prefix="msg_", dir=target_dir, text=True)
            try:
                with os.fdopen(fd, 'w') as tmpf:
                    json.dump(messages, tmpf, indent=2)
                    tmpf.flush()
                    os.fsync(tmpf.fileno())

                # Atomic replace
                os.replace(tmp_path, message_file)
            finally:
                # If something went wrong and tmp_path still exists, try to remove it
                if os.path.exists(tmp_path):
                    try:
                        os.remove(tmp_path)
                    except Exception:
                        pass
    except FileLockTimeout:
        raise TimeoutError(f"Could not acquire file lock for {message_file!r} within {lock_timeout_seconds} seconds")

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
    safe_username = sanitize_username(username)
    message_file = os.path.join(MESSAGE_DIR, f"{safe_username}.json")

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