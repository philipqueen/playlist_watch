import discord
from discord.ext import commands
import logging
import os

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(bot))

async def load_extensions():
    await bot.load_extension('cogs.hello')
    await bot.load_extension('cogs.check_permissions')
    await bot.load_extension('cogs.playlist_check')
    await bot.load_extension('cogs.add_playlist')
    await bot.load_extension('cogs.remove_playlist')
    await bot.load_extension('cogs.add_channel')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('TOKEN'))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())