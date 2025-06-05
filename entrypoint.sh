#!/bin/sh
set -e

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

log "INFO: Entrypoint running..."
log "INFO: Twitch Client ID: $TWITCH_CLIENT_ID"

exec python3 -u main.py

