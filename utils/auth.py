import json
import os

def load_users():
    path = os.path.join(os.path.dirname(__file__), '../data/users.json')
    with open(path, 'r') as f:
        return json.load(f)

def authenticate(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None
