import json
import os
import time

def create_ticket(username, user_id, email, summary):
    ticket_id = f"TKT{int(time.time())}"
    ticket = {
        "ticket_id": ticket_id,
        "username": username,
        "user_id": user_id,
        "email": email,
        "summary": summary,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }
    path = os.path.join(os.path.dirname(__file__), '../data/tickets.json')
    if os.path.exists(path):
        with open(path, 'r') as f:
            tickets = json.load(f)
    else:
        tickets = []
    tickets.append(ticket)
    with open(path, 'w') as f:
        json.dump(tickets, f, indent=2)
    return ticket_id
