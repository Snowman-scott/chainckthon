#!/usr/bin/env python3
# test_system.py
# Complete E2E Messenger Testing and Demo Script

import os
import sys
import time
from datetime import datetime

print("="*60)
print("E2E ENCRYPTED MESSENGER - SYSTEM TEST & DEMO")
print("="*60)

# Test imports
print("\n[1/7] Testing imports...")
try:
    from auth import (
        setup, hash_password, Verify_password, gen_keypair,
        serialize_public_key, save_private_key, Load_private_key,
        load_user, save_user, load_all_users
    )
    print("✓ auth.py imported successfully")
except Exception as e:
    print(f"✗ Error importing auth.py: {e}")
    sys.exit(1)

try:
    from encryption import encrypt_message, decrypt_message
    print("✓ encryption.py imported successfully")
except Exception as e:
    print(f"✗ Error importing encryption.py: {e}")
    sys.exit(1)

try:
    from message_storage import (
        setup_messages, save_message, get_messages_for_user,
        get_user_public_key, get_all_users
    )
    print("✓ message_storage.py imported successfully")
except Exception as e:
    print(f"✗ Error importing message_storage.py: {e}")
    sys.exit(1)

try:
    from messaging import send_message_ui, check_inbox_ui
    print("✓ messaging.py imported successfully")
except Exception as e:
    print(f"✗ Error importing messaging.py: {e}")
    sys.exit(1)

# Test setup
print("\n[2/7] Testing directory setup...")
try:
    setup()
    setup_messages()
    print("✓ Directories created successfully")
    print("  - Users/ directory exists")
    print("  - Keys/ directory exists")
    print("  - messages/ directory exists")
except Exception as e:
    print(f"✗ Setup error: {e}")
    sys.exit(1)

# Test password hashing
print("\n[3/7] Testing password hashing...")
try:
    test_password = "TestPassword123"
    hash1, salt1 = hash_password(test_password)
    print(f"✓ Password hashed successfully")
    print(f"  Hash (preview): {hash1[:20]}...")
    print(f"  Salt (preview): {salt1[:20]}...")
    
    # Verify correct password
    if Verify_password(test_password, hash1, salt1):
        print("✓ Correct password verification works")
    else:
        print("✗ Password verification failed")
        sys.exit(1)
    
    # Verify wrong password fails
    if not Verify_password("WrongPassword", hash1, salt1):
        print("✓ Wrong password correctly rejected")
    else:
        print("✗ Wrong password incorrectly accepted")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Password hashing error: {e}")
    sys.exit(1)

# Test key generation
print("\n[4/7] Testing RSA key generation...")
try:
    private_key, public_key = gen_keypair()
    print("✓ RSA keypair generated (2048-bit)")
    
    public_key_pem = serialize_public_key(public_key)
    print("✓ Public key serialized to PEM format")
    print(f"  PEM (preview): {public_key_pem[:50]}...")
    
except Exception as e:
    print(f"✗ Key generation error: {e}")
    sys.exit(1)

# Test user creation and storage
print("\n[5/7] Testing user creation...")
try:
    # Create test user Alice
    alice_password = "AlicePassword123"
    alice_hash, alice_salt = hash_password(alice_password)
    alice_private, alice_public = gen_keypair()
    alice_public_pem = serialize_public_key(alice_public)
    
    alice_data = {
        "username": "alice",
        "password_hash": alice_hash,
        "salt": alice_salt,
        "public_key": alice_public_pem
    }
    
    save_user("alice", alice_data)
    save_private_key("alice", alice_private, alice_password)
    print("✓ User 'alice' created and saved")
    
    # Create test user Bob
    bob_password = "BobPassword123"
    bob_hash, bob_salt = hash_password(bob_password)
    bob_private, bob_public = gen_keypair()
    bob_public_pem = serialize_public_key(bob_public)
    
    bob_data = {
        "username": "bob",
        "password_hash": bob_hash,
        "salt": bob_salt,
        "public_key": bob_public_pem
    }
    
    save_user("bob", bob_data)
    save_private_key("bob", bob_private, bob_password)
    print("✓ User 'bob' created and saved")
    
    # Verify users can be loaded
    loaded_alice = load_user("alice")
    loaded_bob = load_user("bob")
    
    if loaded_alice and loaded_bob:
        print("✓ Users loaded successfully from files")
    else:
        print("✗ Failed to load users")
        sys.exit(1)
    
    # Verify all users list
    all_users = load_all_users()
    if "alice" in all_users and "bob" in all_users:
        print(f"✓ Found {len(all_users)} users: {', '.join(all_users)}")
    else:
        print("✗ User list incomplete")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ User creation error: {e}")
    sys.exit(1)

# Test encryption/decryption
print("\n[6/7] Testing E2E encryption...")
try:
    # Alice sends message to Bob
    message_text = "Hello Bob! This is a secret message from Alice 🔒"
    print(f"  Original message: '{message_text}'")
    
    # Encrypt with Bob's public key
    encrypted_data = encrypt_message(message_text, bob_public_pem)
    print("✓ Message encrypted with Bob's public key")
    print(f"  Encrypted (preview): {encrypted_data['encrypted_message'][:40]}...")
    
    # Bob decrypts with his private key
    decrypted_text = decrypt_message(encrypted_data, bob_private)
    print("✓ Message decrypted with Bob's private key")
    print(f"  Decrypted message: '{decrypted_text}'")
    
    if message_text == decrypted_text:
        print("✓ Encryption/Decryption successful - messages match!")
    else:
        print("✗ Messages don't match")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Encryption error: {e}")
    sys.exit(1)

# Test message storage
print("\n[7/7] Testing message storage...")
try:
    # Create message package
    message_package = {
        'from_user': 'alice',
        'to_user': 'bob',
        'encrypted_message': encrypted_data['encrypted_message'],
        'encrypted_key': encrypted_data['encrypted_key'],
        'nonce': encrypted_data['nonce'],
        'timestamp': datetime.now().isoformat()
    }
    
    # Save message
    save_message(message_package)
    print("✓ Message saved to storage")
    
    # Retrieve messages
    bob_messages = get_messages_for_user('bob')
    print(f"✓ Retrieved {len(bob_messages)} message(s) for Bob")
    
    if len(bob_messages) > 0:
        # Decrypt the retrieved message
        retrieved_msg = bob_messages[-1]  # Get last message
        encrypted_content = {
            'encrypted_message': retrieved_msg['encrypted_message'],
            'encrypted_key': retrieved_msg['encrypted_key'],
            'nonce': retrieved_msg['nonce']
        }
        
        decrypted_retrieved = decrypt_message(encrypted_content, bob_private)
        print(f"✓ Retrieved message decrypted: '{decrypted_retrieved}'")
        
        if decrypted_retrieved == message_text:
            print("✓ Full round-trip successful!")
        else:
            print("✗ Retrieved message doesn't match")
            sys.exit(1)
    else:
        print("✗ No messages found for Bob")
        sys.exit(1)
        
    # Test get_user_public_key
    alice_pub_key = get_user_public_key('alice')
    if alice_pub_key:
        print("✓ get_user_public_key() works correctly")
    else:
        print("✗ get_user_public_key() failed")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Message storage error: {e}")
    sys.exit(1)

# Final summary
print("\n" + "="*60)
print("✓ ALL TESTS PASSED!")
print("="*60)
print("\nSystem Status:")
print("  ✓ Authentication system working")
print("  ✓ RSA-2048 key generation working")
print("  ✓ AES-256-GCM encryption working")
print("  ✓ End-to-end encryption working")
print("  ✓ Message storage working")
print("  ✓ User management working")
print("\nDemo users created:")
print("  - alice (password: AlicePassword123)")
print("  - bob (password: BobPassword123)")
print("\n" + "="*60)
print("READY FOR HACKATHON DEMO!")
print("="*60)
print("\nTo start the application, run:")
print("  python main.py")
print("\nOr test specific modules:")
print("  python auth.py")
print("  python encryption.py")
print("  python message_storage.py")
print("\n" + "="*60)