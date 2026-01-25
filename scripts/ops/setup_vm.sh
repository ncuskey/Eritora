#!/bin/bash
set -e

APP_DIR="/var/www/wiki"
REPO_URL="https://github.com/toonight/get-shit-done-for-antigravity.git" # Placeholder, user needs to update
USER="wiki"

echo ">>> Setting up Wiki Environment..."

# 1. Install System Dependencies
echo ">>> Installing git and python3..."
sudo apt-get update
sudo apt-get install -y git python3 python3-venv python3-pip

# 2. Setup Directory Structure
echo ">>> ensuring $APP_DIR exists..."
sudo mkdir -p $APP_DIR
sudo chown -R $USER:$USER $APP_DIR || echo "User $USER not found, skipping chown (assuming current user)"

# 3. Setup Python Virtual Environment
echo ">>> Setting up venv..."
cd $APP_DIR
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 4. Install Requirements via venv
echo ">>> Installing python requirements..."
./venv/bin/pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    ./venv/bin/pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found in $APP_DIR"
fi

echo ">>> Setup Complete!"
echo "Run: source venv/bin/activate && mkdocs serve"
