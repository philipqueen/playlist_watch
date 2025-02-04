import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

async def send_message(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)

@bot.command()
async def post(ctx):
    await send_message(1335153750637281300, "Hello, this is a message!")

bot.run(os.getenv('TOKEN'))
