from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class AddChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_channel(self, ctx, name: str):
        logger.info(f"Adding channel: {name}")

        guild = ctx.guild
        logger.info(f"Creating channel '{name}'...")
        await guild.create_text_channel(name)
        await ctx.send(f"Channel '{name}' created!")

async def setup(bot):
    await bot.add_cog(AddChannel(bot))