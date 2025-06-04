import json
import os
from datetime import datetime

STATE_FILE = "/app/data/state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def was_notified_today(state, streamer_name):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    return state.get(streamer_name) == today

def mark_notified(state, streamer_name):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    state[streamer_name] = today
    save_state(state)

