#!/usr/bin/env python3
# api.py
# Flask API Backend for E2E Encrypted Messenger Web UI
# OPTIONAL - Only needed if you want to connect the React UI to Python backend

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Import your modules
from auth import (
    setup, hash_password, Verify_password, gen_keypair,
    serialize_public_key, save_private_key, Load_private_key,
    load_user, save_user, load_all_users
)
from encryption import encrypt_message, decrypt_message, EncryptionError, DecryptionError
from message_storage import (
    setup_messages, save_message, get_messages_for_user,
    get_user_public_key, get_all_users
)
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize
setup()
setup_messages()

# Store active sessions (in production, use proper session management)
active_sessions = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'E2E Messenger API is running'
    })

@app.route('/api/signup', methods=['POST'])
def signup():
    """Create a new user account"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # Validation
        if not username or len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters'}), 400
        
        if not password or len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        # Check if user exists
        all_users = load_all_users()
        if username in all_users:
            return jsonify({'error': 'Username already taken'}), 400
        
        # Create user
        password_hash, salt = hash_password(password)
        private_key, public_key = gen_keypair()
        public_key_pem = serialize_public_key(public_key)
        
        # Save user data
        user_data = {
            "username": username,
            "password_hash": password_hash,
            "salt": salt,
            "public_key": public_key_pem
        }
        save_user(username, user_data)
        save_private_key(username, private_key, password)
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'username': username
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Load user
        all_users = load_all_users()
        if username not in all_users:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        user_data = load_user(username)
        if not user_data:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Verify password
        if not Verify_password(password, user_data['password_hash'], user_data['salt']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Load private key
        try:
            private_key = Load_private_key(username, password)
        except Exception:
            return jsonify({'error': 'Failed to load encryption keys'}), 500
        
        # Create session token (in production, use proper JWT or session tokens)
        session_token = os.urandom(32).hex()
        active_sessions[session_token] = {
            'username': username,
            'private_key': private_key,
            'public_key': user_data['public_key']
        }
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'username': username,
            'session_token': session_token
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    try:
        data = request.json
        session_token = data.get('session_token')
        
        if session_token in active_sessions:
            del active_sessions[session_token]
        
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/send', methods=['POST'])
def send_message():
    """Send an encrypted message"""
    try:
        data = request.json
        session_token = data.get('session_token')
        recipient = data.get('recipient', '').strip()
        message_text = data.get('message', '').strip()
        
        # Verify session
        if session_token not in active_sessions:
            return jsonify({'error': 'Not authenticated'}), 401
        
        session = active_sessions[session_token]
        
        if not recipient or not message_text:
            return jsonify({'error': 'Recipient and message required'}), 400
        
        # Get recipient's public key
        recipient_public_key = get_user_public_key(recipient)
        if not recipient_public_key:
            return jsonify({'error': f'User {recipient} not found'}), 404
        
        # Encrypt message
        try:
            encrypted_data = encrypt_message(message_text, recipient_public_key)
        except EncryptionError as e:
            return jsonify({'error': 'Encryption failed'}), 500
        
        # Save message
        message_package = {
            'from_user': session['username'],
            'to_user': recipient,
            'encrypted_message': encrypted_data['encrypted_message'],
            'encrypted_key': encrypted_data['encrypted_key'],
            'nonce': encrypted_data['nonce'],
            'timestamp': datetime.now().isoformat()
        }
        
        save_message(message_package)
        
        return jsonify({
            'success': True,
            'message': 'Message sent successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inbox', methods=['POST'])
def get_inbox():
    """Get user's inbox with decrypted messages"""
    try:
        data = request.json
        session_token = data.get('session_token')
        
        # Verify session
        if session_token not in active_sessions:
            return jsonify({'error': 'Not authenticated'}), 401
        
        session = active_sessions[session_token]
        
        # Get messages
        messages = get_messages_for_user(session['username'])
        
        # Decrypt messages
        decrypted_messages = []
        for msg in messages:
            try:
                encrypted_content = {
                    'encrypted_message': msg['encrypted_message'],
                    'encrypted_key': msg['encrypted_key'],
                    'nonce': msg['nonce']
                }
                
                decrypted_text = decrypt_message(encrypted_content, session['private_key'])
                
                decrypted_messages.append({
                    'id': len(decrypted_messages) + 1,
                    'from': msg.get('from_user', 'Unknown'),
                    'message': decrypted_text,
                    'timestamp': msg.get('timestamp', ''),
                    'decrypted': True
                })
            except DecryptionError:
                # Skip messages that can't be decrypted
                decrypted_messages.append({
                    'id': len(decrypted_messages) + 1,
                    'from': msg.get('from_user', 'Unknown'),
                    'message': '[Unable to decrypt message]',
                    'timestamp': msg.get('timestamp', ''),
                    'decrypted': False
                })
        
        return jsonify({
            'success': True,
            'messages': decrypted_messages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def list_users():
    """Get list of all users"""
    try:
        users = get_all_users()
        return jsonify({
            'success': True,
            'users': users
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("E2E Encrypted Messenger - API Server")
    print("="*60)
    print("\nStarting Flask API server...")
    print("API will be available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  POST /api/signup    - Create account")
    print("  POST /api/login     - Login")
    print("  POST /api/logout    - Logout")
    print("  POST /api/send      - Send message")
    print("  POST /api/inbox     - Get inbox")
    print("  GET  /api/users     - List users")
    print("  GET  /api/health    - Health check")
    print("\nPress Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
