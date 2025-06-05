import os
import configparser

CONFIG_PATH = os.getenv("CONFIG_INI_PATH", "config.ini")

def load_config():
    config = {}

    # Load .ini file if it exists
    parser = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        parser.read(CONFIG_PATH)

        config['CHECK_INTERVAL_MINUTES'] = parser.getint('general', 'check_interval_minutes', fallback=None)
        config['TWITCH_CLIENT_ID'] = parser.get('twitch', 'client_id', fallback=None)
        config['TWITCH_CLIENT_SECRET'] = parser.get('twitch', 'client_secret', fallback=None)
        config['DISCORD_WEBHOOK_URL'] = parser.get('discord', 'webhook', fallback=None)
        config['STREAMERS_CONFIG'] = parser.get('streamers', 'config', fallback=None)

    # Fallback to environment variables if not set
    config['CHECK_INTERVAL_MINUTES'] = config['CHECK_INTERVAL_MINUTES'] or int(os.getenv("CHECK_INTERVAL_MINUTES", 1))
    config['TWITCH_CLIENT_ID'] = config['TWITCH_CLIENT_ID'] or os.getenv("TWITCH_CLIENT_ID")
    config['TWITCH_CLIENT_SECRET'] = config['TWITCH_CLIENT_SECRET'] or os.getenv("TWITCH_CLIENT_SECRET")
    config['DISCORD_WEBHOOK_URL'] = config['DISCORD_WEBHOOK_URL'] or os.getenv("DISCORD_WEBHOOK_URL")
    config['STREAMERS_CONFIG'] = config['STREAMERS_CONFIG'] or os.getenv("STREAMERS_CONFIG", "[]")

    return config
