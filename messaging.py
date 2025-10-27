# messaging.py
# E2E Encrypted Messenger - Messaging UI and Functions

from encryption import encrypt_message, decrypt_message
from message_storage import save_message, get_messages_for_user, get_user_public_key
from datetime import datetime
import os
import time

# ============================================
# SENDING MESSAGES
# ============================================

def send_message_ui(session):
    """
    UI/Function for sending encrypted messages.
    
    Args:
        session (dict): Current user session from auth.py containing:
            - username: Current user's username
            - private_key: Current user's private key object
            - public_key: Current user's public key (PEM string)
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== E2E Encrypted Messaging App ===")
        print("\n=== Send Message ===")
        
        # Get recipient username
        recipient_username = input("To (username): ").strip()
        if not recipient_username:
            print("❌ Recipient username cannot be empty")
            time.sleep(1.5)
            return
        
        # Get recipient's public key from Users.json
        recipient_public_key = get_user_public_key(recipient_username)
        
        if not recipient_public_key:
            print(f"❌ User '{recipient_username}' not found")
            time.sleep(1.5)
            return
        
        # Get message content
        print("\nMessage (type your message, press Enter when done):")
        message_text = input().strip()
        
        if not message_text:
            print("❌ Message cannot be empty")
            time.sleep(1.5)
            return
        
        # Encrypt the message
        print("\n🔒 Encrypting message...")
        encrypted_data = encrypt_message(message_text, recipient_public_key)
        
        # Prepare message package
        message_package = {
            'from_user': session['username'],
            'to_user': recipient_username,
            'encrypted_message': encrypted_data['encrypted_message'],
            'encrypted_key': encrypted_data['encrypted_key'],
            'nonce': encrypted_data['nonce'],
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to storage (your friend's function)
        save_message(message_package)
        
        print("✓ Message sent successfully!")
        time.sleep(1.5)
        
    except KeyboardInterrupt:
        print("\n❌ Message cancelled")
        time.sleep(1)
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        time.sleep(2)


# ============================================
# RECEIVING MESSAGES
# ============================================

def check_inbox_ui(session):
    """
    UI/Function for checking and reading encrypted messages.
    
    Args:
        session (dict): Current user session from auth.py containing:
            - username: Current user's username
            - private_key: Current user's private key object for decryption
            - public_key: Current user's public key (PEM string)
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== E2E Encrypted Messaging App ===")
        print("\n=== Your Inbox ===")
        
        # Get messages from storage (your friend's function)
        messages = get_messages_for_user(session['username'])
        
        if not messages or len(messages) == 0:
            print("\n📭 No messages yet")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n📬 You have {len(messages)} message(s)\n")
        
        # Display each message
        for idx, msg in enumerate(messages, 1):
            print(f"{'='*50}")
            print(f"Message {idx}")
            print(f"{'='*50}")
            print(f"From: {msg.get('from_user', 'Unknown')}")
            print(f"Time: {msg.get('timestamp', 'Unknown')}")
            
            try:
                # Decrypt the message
                encrypted_content = {
                    'encrypted_message': msg['encrypted_message'],
                    'encrypted_key': msg['encrypted_key'],
                    'nonce': msg['nonce']
                }
                
                decrypted_text = decrypt_message(encrypted_content, session['private_key'])
                print(f"\nMessage:\n{decrypted_text}")
                
            except Exception as e:
                print(f"\n❌ Could not decrypt this message: {e}")
            
            print()  # Blank line between messages
        
        input("Press Enter to continue...")
        
    except Exception as e:
        print(f"❌ Error checking inbox: {e}")
        time.sleep(2)


# ============================================
# HELPER FUNCTIONS
# ============================================

def send_message_programmatic(from_user_id, from_username, to_username, 
                              message_text, sender_private_key):
    """
    Send a message programmatically (for API/non-UI use).
    
    Args:
        from_user_id (str): Sender's user ID
        from_username (str): Sender's username
        to_username (str): Recipient's username
        message_text (str): Plain text message to send
        sender_private_key (str): Sender's private key
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get recipient's public key
        from message_storage import get_user_public_key
        recipient_public_key = get_user_public_key(to_username)
        
        if not recipient_public_key:
            return False
        
        # Encrypt
        encrypted_data = encrypt_message(message_text, recipient_public_key)
        
        # Prepare and save
        message_package = {
            'from_user': from_username,
            'from_user_id': from_user_id,
            'to_user': to_username,
            'encrypted_message': encrypted_data['encrypted_message'],
            'encrypted_key': encrypted_data['encrypted_key'],
            'nonce': encrypted_data['nonce'],
            'timestamp': datetime.now().isoformat()
        }
        
        save_message(message_package)
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def read_messages_programmatic(user_id, private_key):
    """
    Read messages programmatically (for API/non-UI use).
    
    Args:
        user_id (str): User's ID
        private_key (str): User's private key for decryption
    
    Returns:
        list: List of decrypted message dictionaries
    """
    try:
        messages = get_messages_for_user(user_id)
        decrypted_messages = []
        
        for msg in messages:
            try:
                encrypted_content = {
                    'encrypted_message': msg['encrypted_message'],
                    'encrypted_key': msg['encrypted_key'],
                    'nonce': msg['nonce']
                }
                
                decrypted_text = decrypt_message(encrypted_content, private_key)
                
                decrypted_messages.append({
                    'from': msg.get('from_user', 'Unknown'),
                    'message': decrypted_text,
                    'timestamp': msg.get('timestamp', 'Unknown')
                })
            except:
                # Skip messages that can't be decrypted
                continue
        
        return decrypted_messages
        
    except Exception as e:
        print(f"Error: {e}")
        return []


# ============================================
# DEMO/TEST
# ============================================

if __name__ == "__main__":
    print("This module requires auth.py and message_storage.py to run")
    print("\nImport and use these functions:")
    print("  - send_message_ui(session)")
    print("  - check_inbox_ui(session)")