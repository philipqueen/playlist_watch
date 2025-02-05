import discord
from discord.ext import commands
import logging
import re

from playlist_watch.spotify.get_playlist_name import playlist_name_from_id
from playlist_watch.system.manage_playlists_json import add_playlist

logger = logging.getLogger(__name__)

class AddPlaylist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, playlist_url: str):
        logger.info(f"Adding playlist: {playlist_url}")
        # Extract the playlist ID from the URL
        match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
        if not match:
            await ctx.send("Invalid Spotify playlist URL.")
            return
        
        playlist_id = match.group(1)
        playlist_name = playlist_name_from_id(playlist_id)

        guild = ctx.guild
        logger.info(f"Creating channel '{playlist_name}'...")
        category = discord.utils.get(guild.categories, name='Playlists')
        new_channel = await guild.create_text_channel(playlist_name, category=category)
        await ctx.send(f"Channel '{playlist_name}' created!")

        logger.info("Adding playlist to JSON...")
        add_playlist(playlist_id=playlist_id, playlist_name=playlist_name, channel_id=new_channel.id)

async def setup(bot):
    await bot.add_cog(AddPlaylist(bot))