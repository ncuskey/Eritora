import asyncio
import discord
from discord.ext import commands
from bot import config

INTENTS = discord.Intents.default()
INTENTS.message_content = True

class WikiBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!wiki ", intents=INTENTS)

    async def setup_hook(self):
        # Load cogs here (deferred until created)
        await self.load_extension("bot.cogs.sync")
        # await self.load_extension("bot.cogs.wiki")
        pass

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

async def main():
    bot = WikiBot()
    if config.DISCORD_TOKEN:
        await bot.start(config.DISCORD_TOKEN)
    else:
        print("Error: DISCORD_TOKEN not found.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Check if there's a running loop to close, though run() handles most clean up
        pass
