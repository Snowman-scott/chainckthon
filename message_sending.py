from cryptography.fernet import Fernet

# Generate a key (do this once and store securely)

key = Fernet.generate_key()
cipher = Fernet(key)

print(f"Key generated: {len(key)} bytes")
print(cipher)

# Enter the message
message = input("Enter message: ")
print(message)
# Encrypt the message
encrypted = cipher.encrypt(message.encode())
print(encrypted)
# Decrypt the message
decrypted = cipher.decrypt(encrypted)
print(decrypted)