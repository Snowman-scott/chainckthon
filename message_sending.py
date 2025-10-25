from cryptography.fernet import Fernet

# Generate a key (do this once and store securely)

key = Fernet.generate_key()
cipher = Fernet(key)

print(key)
print(cipher)

# Enter the message
message = input(b"Enter message")
message = "hello"
print(message)

# Encrypt the message
encrypted = cipher.encrypt(message)
print(encrypted)

# Decrypt the message
decrypted = cipher.decrypt(encrypted)
print(decrypted)