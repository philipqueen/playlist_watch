from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class CheckPermissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def check_permissions(self, ctx):
        logger.info("Checking permissions...")
        permissions = ctx.channel.permissions_for(ctx.guild.me)
        if permissions.manage_channels:
            await ctx.send("I have permission to manage channels!")
        else:
            await ctx.send("I don't have permission to manage channels.")

async def setup(bot):
    await bot.add_cog(CheckPermissions(bot))