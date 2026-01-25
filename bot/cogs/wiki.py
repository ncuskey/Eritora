import discord
from discord.ext import commands
import os
import re
from bot import config
import git

class WikiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = git.Repo(config.REPO_PATH)

    @commands.command()
    async def create(self, ctx, filename: str, *, content: str):
        """Creates a new wiki page. Usage: !wiki create MyPage This is the content."""
        
        # 1. Clean filename
        clean_name = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
        if not clean_name:
            await ctx.send("❌ Internal Error: Invalid filename.")
            return

        file_path = os.path.join(config.REPO_PATH, "docs", "community", f"{clean_name}.md")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 2. Write File
        try:
            with open(file_path, "w") as f:
                f.write(f"# {filename}\n\n{content}\n\n*Created by {ctx.author.name} from Discord*")
            
            # 3. Git Commit & Push
            self.repo.index.add([file_path])
            self.repo.index.commit(f"feat: Discord user {ctx.author.name} created {clean_name}.md")
            origin = self.repo.remotes.origin
            origin.push()
            
            await ctx.send(f"✅ Created page: `docs/community/{clean_name}.md`\n(Site will rebuild in ~1 min)")
            
        except Exception as e:
            await ctx.send(f"❌ Error creating page: {e}")

async def setup(bot):
    await bot.add_cog(WikiCog(bot))
