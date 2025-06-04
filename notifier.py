import os
import logging
import requests
from token_manager import get_token
from state_manager import load_state, was_notified_today, mark_notified

logger = logging.getLogger(__name__)
CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")

HEADERS = {"Client-ID": CLIENT_ID, "Authorization": ""}

def get_user_id(username, access_token):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"
    url = f"https://api.twitch.tv/helix/users?login={username}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        logger.error(f"Failed to get user ID for {username}: {res.text}")
        return None
    data = res.json()
    if "data" not in data or not data["data"]:
        logger.error(f"No user data returned for {username}: {data}")
        return None
    return data["data"][0]["id"]

def get_stream_info(user_id, access_token):
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"
    url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        logger.error(f"Failed to get stream info for user_id {user_id}: {res.text}")
        return None
    data = res.json()
    if "data" not in data or not data["data"]:
        return None
    return data["data"][0]

def send_discord_notification(webhook_url, streamer_name, stream_title, stream_url):
    content = f"🔴 **{streamer_name}** is live!\nTitle: {stream_title}\nWatch here: {stream_url}"
    res = requests.post(webhook_url, json={"content": content})
    if res.status_code not in [200, 204]:
        logger.error(f"Failed to send Discord notification: {res.text}")

def notify_if_live(config, discord_webhook_url):
    access_token = get_token()
    state = load_state()

    for streamer in config["streamers"]:
        name = streamer["name"]
        blocked_categories = [cat.lower() for cat in streamer.get("blocked_categories", [])]

        if was_notified_today(state, name):
            logger.info(f"Already notified today for {name}, skipping.")
            continue

        user_id = get_user_id(name, access_token)
        if not user_id:
            continue

        stream = get_stream_info(user_id, access_token)
        if not stream:
            logger.info(f"{name} is not live.")
            continue

        category = stream.get("game_name", "").lower()
        if category in blocked_categories:
            logger.info(f"{name} is live but streaming blocked category '{category}'. Skipping notification.")
            continue

        stream_url = f"https://twitch.tv/{name}"
        send_discord_notification(discord_webhook_url, name, stream.get("title", ""), stream_url)
        logger.info(f"Sent notification for {name}.")

        mark_notified(state, name)

