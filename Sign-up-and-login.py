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

User_db = "Users.json"
Keys_DIR = "Keys"

# clear terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Create keys if none exist
def setup():
    try:
        if not os.path.exists(Keys_DIR):
            os.makedirs(Keys_DIR)
        if not os.path.exists(User_db):
            with open(User_db, 'w') as f:
                json.dump({}, f)
    except (OSError, IOError) as e:
        print(f"Error during setup: {e}")
        raise

# Load users from Json
def load_users():
    try:
        with open(User_db, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Error: Users database is corrupted: {e}")
        raise
# Save users to users.json    
def save_users(users):
    with open(User_db, 'w') as f:
        json.dump(users, f, indent=2)

# Hash password with PBKDF2
def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(32)
    else:
        salt = base64.b64decode(salt)

    kdf =   PBKDF2HMAC(
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
        pem, password=password.encode(),
        backend=default_backend()
    )

    return private_key

# Sign up script
def sign_up():
    clear_terminal()
    print("=== E2E Encrypted Messaging App ===")
    print("\n=== SIGN UP ===")

    users = load_users()
    
    # Get username
    while True:
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print("\n=== SIGN UP ===")

        username = input("Choose a username: ").strip()
        if not username:
            print("Username cannot be empty")
            time.sleep(1.5)
        elif username in users:
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
                print("Password don't match!")
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
    print("Generating Encyption Keys")
    private_key, public_key = gen_keypair()

    # convert pub key to string
    public_key_pem = serialize_public_key(public_key)

    # Saves Encrypted Private key
    save_private_key(username, private_key, password)

    # Save user data 
    users[username] = {
        "password_hash": password_hash,
        "salt": salt,
        "public_key": public_key_pem
    }
    save_users(users)

    print(f"\n✓ Account created successfully!")
    print(f"✓ Username: {username}")
    print(f"✓ Encryption keys generated")

    return username

# Log in script
def log_in():
    clear_terminal()
    print("=== E2E Encrypted Messaging App ===")
    print("\n===LOG IN===")

    users = load_users()

    while True:
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print("\n===LOG IN===")

        username = input("Enter Username: ").strip()
        if username not in users:
            print("username not found!")
        elif username in users:
            break

    # Get password
    while True:
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print("\n===LOG IN===")

        password = input("Enter Password: ").strip()

        user_data = users[username]

        if not Verify_password(password, user_data['password_hash'], user_data['salt']):
            print("Incorrect password!")
        else:
            break

    print(f"\n✓ Logged in as {username}")

    #Load Private key
    print("=== E2E Encrypted Messaging App ===")
    print("\n===LOG IN===")
    print("\nAtempting to load private key...")
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
        los = input("\nDo you want to log in or sign up? (L/S)").strip().upper()
        if los in ['S', 'SIGN UP']:
            sign_up()
        elif los in ['L', 'LOGIN','LOG IN']:
            log_in()
        else:
            print("Please enter L or S")

    return None

# Main Execution
if __name__ == "__main__":
    print("=== E2E Encrypted Messaging App ===")
    session = log_in_and_sign_up()

    if session:
        print(f"\n✓ Logged in successfully!")
        print(f"✓ Username: {session['username']}")
        print("✓ Keys loaded and ready")
        print("\n[Ready for messaging functionality]")