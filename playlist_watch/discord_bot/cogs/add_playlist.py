import discord
from discord.ext import commands
import re


class AddPlaylist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addplaylist(self, ctx, playlist_url: str):
        # Extract the playlist ID from the URL
        match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
        if not match:
            await ctx.send("Invalid Spotify playlist URL.")
            return
        
        playlist_id = match.group(1)
        playlist = self.sp.playlist(playlist_id)
        playlist_name = playlist['name']

        # Create a new text channel with the playlist name
        guild = ctx.guild
        await guild.create_text_channel(playlist_name)
        await ctx.send(f"Channel '{playlist_name}' created!")

async def setup(bot):
    await bot.add_cog(AddPlaylist(bot))