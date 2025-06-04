import os
import time
import logging
import json
from notifier import notify_if_live

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL_MINUTES", "5"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable is required")

def load_config():
    config_str = os.getenv("STREAMERS_CONFIG")
    if not config_str:
        logging.error("STREAMERS_CONFIG env variable not set or empty!")
        return {"streamers": []}
    try:
        streamers = json.loads(config_str)
        return {"streamers": streamers}
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in STREAMERS_CONFIG: {e}")
        return {"streamers": []}

def main():
    logging.info(f"Scheduler started. Checking every {CHECK_INTERVAL} minute(s).")
    config = load_config()

    while True:
        try:
            logging.info("Checking stream statuses...")
            notify_if_live(config, DISCORD_WEBHOOK_URL)
        except Exception:
            logging.exception("Exception in main loop")
        time.sleep(CHECK_INTERVAL * 60)

if __name__ == "__main__":
    main()

