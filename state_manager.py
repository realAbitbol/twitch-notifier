import json
import os
from datetime import datetime, timezone

STATE_FILE = "data/state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def has_already_notified_today(streamer):
    state = load_state()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return state.get(streamer) == today

def mark_notified(streamer):
    state = load_state()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    state[streamer] = today
    save_state(state)
