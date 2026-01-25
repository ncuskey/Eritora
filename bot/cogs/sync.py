import asyncio
import discord
from discord.ext import commands, tasks
import git
from bot import config
import subprocess

class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = git.Repo(config.REPO_PATH)
        self.sync_loop.start()

    def cog_unload(self):
        self.sync_loop.cancel()

    @tasks.loop(minutes=1.0)
    async def sync_loop(self):
        try:
            # 1. Fetch remote changes
            for remote in self.repo.remotes:
                remote.fetch()

            # 2. Check current branch vs remote
            # Assuming 'master' - make simpler for now
            current = self.repo.head.commit
            remote_commit = self.repo.refs['origin/master'].commit

            if current != remote_commit:
                print(f"Update detected! Local: {current} | Remote: {remote_commit}")
                
                # 3. Pull changes
                origin = self.repo.remotes.origin
                origin.pull(rebase=True)
                
                # 4. Rebuild MkDocs
                subprocess.run(["mkdocs", "build"], check=True)
                
                # 5. Notify Discord
                channel = self.bot.get_channel(config.CHANNEL_ID)
                if channel:
                    msg = f"🔄 **Wiki Updated!**\nCommit: `{remote_commit.message.strip()}`\nAuthor: {remote_commit.author.name}"
                    await channel.send(msg)
                
        except Exception as e:
            print(f"Sync Logic Error: {e}")

    @sync_loop.before_loop
    async def before_sync(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(SyncCog(bot))
