#!/bin/bash
# Pull latest code from GitHub and restart the service.
# Usage: bash update.sh

set -e
APP_DIR="$HOME/pokemap-web"

echo "==> Pulling latest code..."
git -C "$APP_DIR" pull

echo "==> Updating dependencies..."
pip3 install -r "$APP_DIR/backend/requirements.txt"

echo "==> Restarting service..."
sudo systemctl restart pokemap

echo "==> Done. Status:"
sudo systemctl status pokemap --no-pager
