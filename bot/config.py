import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# Path to the git repo root (usually current working dir)
REPO_PATH = os.getenv("REPO_PATH", ".")
# Channel ID to post updates to (As integer)
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))

if not DISCORD_TOKEN:
    print("Warning: DISCORD_TOKEN not set in environment")
