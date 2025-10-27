import json
import os
import secrets
import base64
import time
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

User_DIR = "Users"  # Now it's a directory!
Keys_DIR = "Keys"

# clear terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Create directories if none exist
def setup():
    try:
        if not os.path.exists(Keys_DIR):
            os.makedirs(Keys_DIR)
        if not os.path.exists(User_DIR):  # Create Users directory
            os.makedirs(User_DIR)
    except (OSError, IOError) as e:
        print(f"Error during setup: {e}")
        raise

# Load single user from their file
def load_user(username):
    """Load a specific user's data"""
    user_file = os.path.join(User_DIR, f"{username}.json")
    try:
        with open(user_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error: User file corrupted: {e}")
        raise

# Load all users (for checking if username exists)
def load_all_users():
    """Load all usernames"""
    try:
        users = []
        if os.path.exists(User_DIR):
            for filename in os.listdir(User_DIR):
                if filename.endswith('.json'):
                    username = filename[:-5]  # Remove .json extension
                    users.append(username)
        return users
    except Exception as e:
        print(f"Error loading users: {e}")
        return []

# Save single user to their file    
def save_user(username, user_data):
    """Save a user's data to their file"""
    user_file = os.path.join(User_DIR, f"{username}.json")
    with open(user_file, 'w') as f:
        json.dump(user_data, f, indent=2)

# Hash password with PBKDF2
def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(32)
    else:
        salt = base64.b64decode(salt)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
        backend=default_backend()
    )

    password_hash = kdf.derive(password.encode())

    hash_b64 = base64.b64encode(password_hash).decode()
    salt_b64 = base64.b64encode(salt).decode()

    return hash_b64, salt_b64

# Verify passwords
def Verify_password(password, stored_hash, stored_salt):
    calculated_hash, _ = hash_password(password, stored_salt)
    return calculated_hash == stored_hash

# Gens RSA keypair
def gen_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Converts public key to string
def serialize_public_key(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem.decode()

# Save encrypted private Key
def save_private_key(username, private_key, password):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode())
    )

    key_file = os.path.join(Keys_DIR, f"{username}.key")
    with open(key_file, 'wb') as f:
        f.write(pem)

# Load encrypted private Key
def Load_private_key(username, password):
    key_file = os.path.join(Keys_DIR, f"{username}.key")

    with open(key_file, 'rb') as f:
        pem = f.read()

    private_key = serialization.load_pem_private_key(
        pem, 
        password=password.encode(),
        backend=default_backend()
    )

    return private_key

# Sign up script
def sign_up():
    clear_terminal()
    print("=== E2E Encrypted Messaging App ===")
    print("\n=== SIGN UP ===")

    all_users = load_all_users()  # Get list of all usernames
    
    # Get username
    while True:
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print("\n=== SIGN UP ===")

        username = input("Choose a username: ").strip()
        if not username:
            print("Username cannot be empty")
            time.sleep(1.5)
        elif username in all_users:  # Check against list
            print("Username already taken!")
            time.sleep(1.5)
        else:
            print(f"Username: {username}")
            break

    # Get password
    pc1 = False
    pc2 = False
    while True:
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print("\n=== SIGN UP ===")

        print(f"Username: {username}")
        password = input("Choose a password (Min 8 chars): ").strip()
        if len(password) < 8:
            print("Password must be at least 8 characters!")
            time.sleep(1.5)
            pc1 = False
        else:
            pc1 = True
        
        if pc1 != True:
            pass
        else:
            confirm = input("Confirm password: ").strip()
            if password != confirm:
                print("Passwords don't match!")
                time.sleep(1)
                pc2 = False
            else:
                pc2 = True

            if pc1 == True and pc2 == True:
                break
            else:
                print("Try again")  
                time.sleep(1)    
        
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print("\n=== SIGN UP ===")
        
    print("\nCreating account...")

    # Hash password
    password_hash, salt = hash_password(password)

    # Gen Keys
    print("Generating Encryption Keys")
    private_key, public_key = gen_keypair()

    # convert pub key to string
    public_key_pem = serialize_public_key(public_key)

    # Saves Encrypted Private key
    save_private_key(username, private_key, password)

    # Save user data to their own file
    user_data = {
        "username": username,
        "password_hash": password_hash,
        "salt": salt,
        "public_key": public_key_pem
    }
    save_user(username, user_data)  # Save to Users/username.json

    print(f"\n✓ Account created successfully!")
    print(f"✓ Username: {username}")
    print(f"✓ Encryption keys generated")

    return username

# Log in script
def log_in():
    clear_terminal()
    print("=== E2E Encrypted Messaging App ===")
    print("\n=== LOG IN ===")

    all_users = load_all_users()  # Get list of all usernames

    while True:
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print("\n=== LOG IN ===")

        username = input("Enter Username: ").strip()
        if username not in all_users:  # Check against list
            print("Username not found!")
            time.sleep(1.5)
        else:
            break

    # Load this user's data
    user_data = load_user(username)
    
    if not user_data:
        print("Error: Could not load user data!")
        return None

    # Get password
    while True:
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print("\n=== LOG IN ===")
        print(f"Username: {username}")

        password = input("Enter Password: ").strip()

        if not Verify_password(password, user_data['password_hash'], user_data['salt']):
            print("Incorrect password!")
            time.sleep(1.5)
        else:
            break

    print(f"\n✓ Logged in as {username}")

    # Load Private key
    print("\nAttempting to load private key...")
    try:
        private_key = Load_private_key(username, password)
        print("✓ Private key loaded")

        return {
            "username": username,
            "private_key": private_key,
            "public_key": user_data['public_key']
        }

    except Exception as e:
        print(f"Error loading private key: {e}")
        return None

# Log in or sign up choice
def log_in_and_sign_up():
    clear_terminal()
    setup()

    while True:
        print("=== E2E Encrypted Messaging App ===")
        los = input("\nDo you want to log in or sign up? (L/S): ").strip().upper()
        if los in ['S', 'SIGN UP']:
            result = sign_up()
            if result:
                login_now = input("\nLog in now? (Y/N): ").strip().upper()
                if login_now == 'Y':
                    continue
                else:
                    return None
        elif los in ['L', 'LOGIN', 'LOG IN']:
            session = log_in()
            if session:
                return session
            else:
                print("Login failed. Try again.")
                time.sleep(1.5)
        else:
            print("Please enter L or S")

# At the end of auth.py
if __name__ == "__main__":
    print("=== Testing Auth System ===")
    session = log_in_and_sign_up()
    if session:
        print("\n✓ Auth test successful!")
        print(f"✓ Logged in as: {session['username']}")
    else:
        print("\nAuth test ended.")


# Note to self! : Cbzm hvwg twzs obr gcas chvsfg ksfs qcrsr kwhvcih Qcdm doghs tfca OW ;Fob cih ct hwas