#!/bin/bash
set -e

# 1. Install Nginx and Certbot
echo ">>> Installing Nginx and Certbot..."
sudo apt-get update
sudo apt-get install -y nginx python3-certbot-nginx

# 2. Configure Nginx
echo ">>> configuring Nginx..."
sudo cp scripts/ops/nginx.conf /etc/nginx/sites-available/eritora
sudo ln -sf /etc/nginx/sites-available/eritora /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 3. Test & Reload
echo ">>> Testing Nginx Config..."
sudo nginx -t
sudo systemctl reload nginx

# 4. HTTPS Setup
echo ">>> Starting Certbot (Follow the prompts)..."
sudo certbot --nginx -d eritora.wiki -d www.eritora.wiki

echo ">>> Setup Complete! Implementation of https://eritora.wiki is live."
