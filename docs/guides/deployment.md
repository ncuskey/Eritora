# Deployment Guide

This guide covers how to deploy and maintain the Eritora system on the Linux VM.

## Initial Setup
1. **SSH into the VM**:
   ```bash
   ssh user@your-vm-ip
   ```
2. **Clone the Repo**:
   ```bash
   git clone https://github.com/ncuskey/Eritora.git wiki
   cd wiki
   ```
3. **Run Setup Script**:
   ```bash
   sudo ./scripts/ops/setup_vm.sh
   ```
4. **Configure Secrets**:
   Create `.env` inside `wiki/`:
   ```bash
   nano .env
   # Add DISCORD_TOKEN=...
   # Add CHANNEL_ID=...
   ```

## Running the Bot
The bot manages the wiki updates. It should run 24/7.

**Quick Start (nohup)**:
```bash
source venv/bin/activate
nohup python3 run_bot.py > bot.log 2>&1 &
```

**Production (Systemd Service)** - Recommended:
1. Create `/etc/systemd/system/eritora.service`:
   ```ini
   [Unit]
   Description=Eritora Wiki Bot
   After=network.target

   [Service]
   User=wiki
   WorkingDirectory=/var/www/wiki
   ExecStart=/var/www/wiki/venv/bin/python3 /var/www/wiki/run_bot.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
2. Enable and Start:
   ```bash
   sudo systemctl enable eritora
   sudo systemctl start eritora
   ```

## Updates
If you change the bot code:
1. `git pull` on the VM.
2. Restart the bot (`sudo systemctl restart eritora` or kill/restart nohup).
