import json
import os
import time
import requests

TOKEN_FILE = "/app/data/token.json"
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TOKEN_URL = "https://id.twitch.tv/oauth2/token"

def load_token():
    if not os.path.exists(TOKEN_FILE):
        return None
    try:
        with open(TOKEN_FILE, "r") as f:
            token = json.load(f)
        return token
    except Exception:
        return None

def save_token(token_data):
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)

def token_expired(token_data):
    expires_at = token_data.get("obtained_at", 0) + token_data.get("expires_in", 0)
    return time.time() > expires_at - 60  # refresh 1 min before expiry

def request_new_token():
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    res = requests.post(TOKEN_URL, params=params)
    res.raise_for_status()
    data = res.json()
    data["obtained_at"] = time.time()
    save_token(data)
    return data

def get_token():
    token = load_token()
    if not token or token_expired(token):
        token = request_new_token()
    return token["access_token"]

