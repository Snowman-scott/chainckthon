#placeholder
# SECURE MESSENGER MINI EXAMPLE
# This demonstrates the core cryptography concepts for secure messaging

import cryptography

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

print("=" * 60)
print("SECURE MESSENGER - CRYPTOGRAPHY DEMO")
print("=" * 60)

# ============================================================================
# STEP 1: KEY GENERATION (happens once per user at registration)
# ============================================================================
print("\n[STEP 1] Generating encryption keys for Alice and Bob...\n")

# Alice generates her key pair
alice_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
alice_public_key = alice_private_key.public_key()

# Bob generates his key pair
bob_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
bob_public_key = bob_private_key.public_key()

print("✓ Alice has generated her private key (keeps secret)")
print("✓ Alice has generated her public key (shares with others)")
print("✓ Bob has generated his private key (keeps secret)")
print("✓ Bob has generated his public key (shares with others)")

# ============================================================================
# STEP 2: ALICE SENDS AN ENCRYPTED MESSAGE TO BOB
# ============================================================================
print("\n" + "=" * 60)
print("[STEP 2] Alice wants to send Bob a secure message")
print("=" * 60)

# The message Alice wants to send
original_message = "Hey Bob! Meet me at the hackathon at 3pm. This is secret!"
print(f"\nAlice's original message:\n  '{original_message}'")

# Generate a random symmetric key (AES)
# This is used because symmetric encryption is MUCH faster than asymmetric
symmetric_key = os.urandom(32)  # 256-bit key for AES-256
print(f"\n✓ Alice generates a random symmetric key: {symmetric_key.hex()[:32]}...")

# Encrypt the symmetric key with Bob's PUBLIC key
# Only Bob can decrypt this with his PRIVATE key
encrypted_symmetric_key = bob_public_key.encrypt(
    symmetric_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print(f"✓ Alice encrypts the symmetric key using Bob's PUBLIC key")
print(f"  Encrypted key: {encrypted_symmetric_key.hex()[:32]}...")

# Encrypt the actual message with the symmetric key (AES)
iv = os.urandom(16)  # Initialization vector for AES
cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))
encryptor = cipher.encryptor()

# Pad message to be multiple of 16 bytes (AES block size)
padded_message = original_message + " " * (16 - len(original_message) % 16)
encrypted_message = encryptor.update(padded_message.encode()) + encryptor.finalize()

print(f"✓ Alice encrypts the message using the symmetric key (AES)")
print(f"  Encrypted message: {encrypted_message.hex()[:32]}...")

# ============================================================================
# STEP 3: TRANSMISSION (This is what goes over the network)
# ============================================================================
print("\n" + "=" * 60)
print("[STEP 3] Data transmitted over network")
print("=" * 60)

transmission_package = {
    "encrypted_key": encrypted_symmetric_key,
    "encrypted_message": encrypted_message,
    "iv": iv,
    "sender": "Alice"
}

print("\nPackage sent contains:")
print("  1. Encrypted symmetric key (only Bob can decrypt)")
print("  2. Encrypted message (encrypted with symmetric key)")
print("  3. Initialization Vector (needed for AES decryption)")
print("  4. Sender information")
print("\n⚠️  Even if intercepted, the attacker cannot read the message!")

# ============================================================================
# STEP 4: BOB RECEIVES AND DECRYPTS THE MESSAGE
# ============================================================================
print("\n" + "=" * 60)
print("[STEP 4] Bob receives and decrypts the message")
print("=" * 60)

# Bob decrypts the symmetric key using his PRIVATE key
received_encrypted_key = transmission_package["encrypted_key"]
decrypted_symmetric_key = bob_private_key.decrypt(
    received_encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print(f"\n✓ Bob decrypts the symmetric key using his PRIVATE key")
print(f"  Decrypted key: {decrypted_symmetric_key.hex()[:32]}...")

# Bob decrypts the message using the symmetric key
received_encrypted_message = transmission_package["encrypted_message"]
received_iv = transmission_package["iv"]

cipher = Cipher(algorithms.AES(decrypted_symmetric_key), modes.CBC(received_iv))
decryptor = cipher.decryptor()
decrypted_padded = decryptor.update(received_encrypted_message) + decryptor.finalize()
decrypted_message = decrypted_padded.decode().strip()

print(f"✓ Bob decrypts the message using the symmetric key")
print(f"\nBob's decrypted message:\n  '{decrypted_message}'")

# Verify it matches
print("\n" + "=" * 60)
if decrypted_message == original_message:
    print("✅ SUCCESS! Message received securely!")
else:
    print("❌ ERROR: Message doesn't match!")
print("=" * 60)
