import time
import logging
from notifier import notify_if_live
from config_loader import load_config

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logging.info("Twitch-Notifier started.")

config = load_config()
interval = config.get("CHECK_INTERVAL_MINUTES", 5)

while True:
    try:
        notify_if_live(config)
    except Exception as e:
        logging.exception("Exception occurred:")
    time.sleep(interval * 60)
