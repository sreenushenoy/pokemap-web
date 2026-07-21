#!/bin/bash
# Run this once on a fresh Oracle Cloud Ubuntu ARM instance.
# Usage: bash setup.sh

set -e

REPO="https://github.com/sreenushenoy/pokemap-web.git"
APP_DIR="$HOME/pokemap-web"
SERVICE_NAME="pokemap"

echo "==> Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "==> Installing Python, git, nginx, certbot..."
sudo apt install -y python3 python3-pip git nginx certbot python3-certbot-nginx

echo "==> Cloning repo..."
if [ -d "$APP_DIR" ]; then
  echo "    Repo already exists, pulling latest..."
  git -C "$APP_DIR" pull
else
  git clone "$REPO" "$APP_DIR"
fi

echo "==> Installing Python dependencies..."
pip3 install -r "$APP_DIR/backend/requirements.txt"

echo "==> Installing systemd service..."
sudo cp "$APP_DIR/deploy/pokemap.service" /etc/systemd/system/${SERVICE_NAME}.service
sudo sed -i "s|__HOME__|$HOME|g" /etc/systemd/system/${SERVICE_NAME}.service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo "==> Configuring nginx..."
sudo cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/$SERVICE_NAME
sudo ln -sf /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/$SERVICE_NAME
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "==> Opening firewall ports (iptables)..."
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
# Persist rules across reboots
sudo apt install -y iptables-persistent
sudo netfilter-persistent save

echo ""
echo "========================================="
echo "  Done! App is running at http://$(curl -s ifconfig.me)"
echo ""
echo "  To enable HTTPS (recommended), run:"
echo "  sudo certbot --nginx -d yourdomain.com"
echo "========================================="
