import json
import os
from datetime import datetime

MESSAGE_DIR = "messages"

def setup_messages():
    if not os.path.exists(MESSAGE_DIR):
        os.makedirs(MESSAGE_DIR)

def save_message():
    pass # code

def get_messages_for_user():
    pass # code

def get_all_users():
    pass # code