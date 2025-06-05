import os
import json
import requests

TOKEN_FILE="data/token.json"

def get_token(config):
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)
        return token_data["access_token"]

    res = requests.post("https://id.twitch.tv/oauth2/token", params={
        "client_id": config["TWITCH_CLIENT_ID"],
        "client_secret": config["TWITCH_CLIENT_SECRET"],
        "grant_type": "client_credentials"
    })
    token_data = res.json()
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
    return token_data["access_token"]
