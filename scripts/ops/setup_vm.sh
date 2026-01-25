#!/bin/bash
set -e

# Use current directory
APP_DIR=$(pwd)
USER=$(whoami)

echo ">>> Setting up Wiki in $APP_DIR as $USER..."

# 1. Install System Dependencies
echo ">>> Installing git and python3..."
sudo apt-get update
sudo apt-get install -y git python3 python3-venv python3-pip

# 2. Setup Python Virtual Environment
echo ">>> Setting up venv..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 3. Install Requirements via venv
echo ">>> Installing python requirements..."
./venv/bin/pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    ./venv/bin/pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found in $APP_DIR"
fi

echo ">>> Setup Complete!"
echo "Run: source venv/bin/activate && mkdocs serve"
