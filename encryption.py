# encryption.py
# E2E Encrypted Messenger - Encryption Module

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os
import base64

# ============================================
# MESSAGE ENCRYPTION (SENDING)
# ============================================

def encrypt_message(message, recipient_public_key):
    """
    Encrypt a message for the recipient.
    Uses hybrid encryption (AES-GCM + RSA).
    
    Args:
        message (str): The plaintext message to encrypt
        recipient_public_key (str): Recipient's public key in PEM format (from Users.json)
    
    Returns:
        dict: Contains encrypted_message, encrypted_key, and nonce (all base64 encoded)
    """
    try:
        # Step 1: Generate a random AES key (32 bytes = 256 bits)
        aes_key = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(aes_key)
        
        # Step 2: Generate a random nonce (12 bytes for AES-GCM)
        nonce = os.urandom(12)
        
        # Step 3: Encrypt the message with AES-GCM
        message_bytes = message.encode('utf-8')
        encrypted_message = aesgcm.encrypt(nonce, message_bytes, None)
        
        # Step 4: Load recipient's public key (it's already in PEM format from auth.py)
        public_key = serialization.load_pem_public_key(
            recipient_public_key.encode('utf-8'),
            backend=default_backend()
        )
        
        # Step 5: Encrypt the AES key with recipient's RSA public key
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Step 6: Return everything as base64 encoded strings
        return {
            'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),
            'encrypted_key': base64.b64encode(encrypted_aes_key).decode('utf-8'),
            'nonce': base64.b64encode(nonce).decode('utf-8')
        }
        
    except Exception as e:
        # Log error internally without exposing details
        raise Exception("Failed to encrypt message")


# ============================================
# MESSAGE DECRYPTION (RECEIVING)
# ============================================

def decrypt_message(encrypted_content, my_private_key):
    """
    Decrypt a message with your private key.
    
    Args:
        encrypted_content (dict): Contains encrypted_message, encrypted_key, and nonce
        my_private_key: Your private key object (from auth.py Load_private_key)
    
    Returns:
        str: The decrypted plaintext message
    """
    try:
        # Step 1: Decode from base64
        encrypted_aes_key = base64.b64decode(encrypted_content['encrypted_key'])
        encrypted_message = base64.b64decode(encrypted_content['encrypted_message'])
        nonce = base64.b64decode(encrypted_content['nonce'])
        
        # Step 2: Decrypt the AES key with your RSA private key
        # my_private_key is already a key object from auth.py
        aes_key = my_private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Step 3: Decrypt the message with the AES key
        aesgcm = AESGCM(aes_key)
        decrypted_message = aesgcm.decrypt(nonce, encrypted_message, None)
        
        # Step 4: Convert bytes back to string
        return decrypted_message.decode('utf-8')
        
    except Exception as e:
        # Log error internally without exposing details
        raise Exception("Failed to decrypt message")


# ============================================
# DEMO/TEST
# ============================================

if __name__ == "__main__":
    print("=== E2E Encryption Demo ===\n")
    
    # Generate test keys using the same method as auth.py
    from cryptography.hazmat.primitives.asymmetric import rsa
    
    alice_private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    alice_public = alice_private.public_key()
    
    bob_private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    bob_public = bob_private.public_key()
    
    # Serialize public keys like auth.py does
    alice_public_pem = alice_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    
    bob_public_pem = bob_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    
    print("✓ Generated keys for Alice and Bob")
    
    # Alice sends a message to Bob
    message = "Hey Bob! This is a secret message 🔒"
    print(f"\nAlice's original message: {message}")
    
    encrypted = encrypt_message(message, bob_public_pem)
    print(f"✓ Message encrypted")
    print(f"  Encrypted (preview): {encrypted['encrypted_message'][:50]}...")
    
    # Bob receives and decrypts
    decrypted = decrypt_message(encrypted, bob_private)
    print(f"\n✓ Bob decrypted the message: {decrypted}")
    print(f"✓ Match: {message == decrypted}")