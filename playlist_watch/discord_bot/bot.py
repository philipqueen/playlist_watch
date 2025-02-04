import discord
from discord.ext import commands
from logging import getLogger
import os

logger = getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(bot))

async def load_extensions():
    await bot.load_extension('cogs.hello')
    await bot.load_extension('cogs.playlist_check')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv('TOKEN'))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())