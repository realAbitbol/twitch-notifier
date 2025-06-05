import requests
import json
import logging
from token_manager import get_token
from state_manager import has_already_notified_today, mark_notified, clean_state    

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

def send_discord_notification(webhook_url, streamer, category, title):
    content = f"🔴 **{streamer}** is live!\nCategory: {category}\nTitle: {title}\nWatch here: https://twitch.tv/{streamer}"
    requests.post(webhook_url, json={"content": content})

def notify_if_live(config):
    token = get_token(config)
    streamers = json.loads(config["STREAMERS_CONFIG"])
    client_id = config["TWITCH_CLIENT_ID"]
    webhook = config["DISCORD_WEBHOOK_URL"]

    clean_state(streamers)

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

        if info:
            current_game = info.get("game_name", "").strip()
            current_game_lower = current_game.lower()
            blocked_lower = [b.lower() for b in blocked]

            if current_game_lower not in blocked_lower:
                logging.info(f"Sending Discord notification for {name} - Game: '{current_game}' | Title: '{info.get('title', '')}'")
                send_discord_notification(webhook, name, current_game, info.get("title", ""))
                mark_notified(name)
            else:
                logging.info(f"{name} is live but streaming a blocked category: '{current_game}'")
        else:
            logging.info(f"{name} is currently offline.")



