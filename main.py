#!/usr/bin/env python3
# main.py
# E2E Encrypted Messaging App - Main Entry Point

import os
import time
from auth import log_in, sign_up, clear_terminal
from messaging import send_message_ui, check_inbox_ui
from message_storage import setup_messages

def main_menu(session):
    """
    Display main menu and handle user choices.
    
    Args:
        session (dict): User session from auth.py
    """
    while True:
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print(f"\nWelcome, {session['username']}!")
        print("\n" + "="*40)
        print("1. Send Message")
        print("2. Check Inbox")
        print("3. Logout")
        print("="*40)
        
        choice = input("\nChoose an option (1-3): ").strip()
        
        if choice == '1':
            send_message_ui(session)
        elif choice == '2':
            check_inbox_ui(session)
        elif choice == '3':
            print("\n✓ Logged out successfully!")
            time.sleep(1)
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")
            time.sleep(1)

def main():
    """Main application entry point"""
    clear_terminal()
    
    # Setup
    # Setup
    try:
        setup_messages()
    except Exception as e:
        print(f"Failed to initialize message storage: {e}")
        print("Please check permissions and try again.")
        return
    
    while True:
        clear_terminal()
        print("=== E2E Encrypted Messaging App ===")
        print("\n" + "="*40)
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        print("="*40)
        
        choice = input("\nChoose an option (1-3): ").strip()
        
        if choice == '1':
            session = log_in()
            if session:
                main_menu(session)
        elif choice == '2':
            username = sign_up()
            if username:
                print("\nAccount created! Please log in.")
                time.sleep(2)
        elif choice == '3':
            print("\nGoodbye! 👋")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye! 👋")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please restart the application.")