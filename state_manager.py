import json
import os
from datetime import datetime, timezone
import logging

STATE_FILE = "data/state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def clean_state(current_streamers):
    state = load_state()
    """Remove state entries for streamers no longer configured."""
    current_names = {s["name"] for s in current_streamers}
    to_remove = [name for name in state if name not in current_names]

    for name in to_remove:
        del state[name]

    if to_remove:
        logging.info(f"Cleaned up state for removed streamers: {to_remove}")
    
    save_state(state)

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
