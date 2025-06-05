import requests
import json
import logging
from token_manager import get_token
from state_manager import has_already_notified_today, mark_notified

def get_user_id(token, username, client_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": client_id
    }
    res = requests.get(f"https://api.twitch.tv/helix/users?login={username}", headers=headers)
    res.raise_for_status()
    data = res.json()
    return data["data"][0]["id"] if data["data"] else None

def get_stream_info(token, user_id, client_id):
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": client_id
    }
    res = requests.get(f"https://api.twitch.tv/helix/streams?user_id={user_id}", headers=headers)
    res.raise_for_status()
    data = res.json()
    return data["data"][0] if data["data"] else None

def send_discord_notification(webhook_url, streamer, category):
    content = f"🔔 **{streamer}** is live! Playing **{category}**"
    requests.post(webhook_url, json={"content": content})

def notify_if_live(config):
    token = get_token(config)
    streamers = json.loads(config["STREAMERS_CONFIG"])
    client_id = config["TWITCH_CLIENT_ID"]
    webhook = config["DISCORD_WEBHOOK_URL"]

    for s in streamers:
        name = s["name"]
        blocked = s.get("blocked_categories", [])

        logging.info(f"Checking {name}...")

        if has_already_notified_today(name):
            logging.info(f"Already notified for {name} today.")
            continue

        user_id = get_user_id(token, name, client_id)
        if not user_id:
            logging.warning(f"User ID not found for {name}")
            continue

        info = get_stream_info(token, user_id, client_id)
        if info and info["game_name"] not in blocked:
            send_discord_notification(webhook, name, info["game_name"])
            mark_notified(name)
        else:
            logging.info(f"{name} isn't live or is streaming a blocked category.")
