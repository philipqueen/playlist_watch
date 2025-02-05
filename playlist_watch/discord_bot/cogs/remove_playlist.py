from discord.ext import commands
import re

from playlist_watch.spotify.get_playlist_name import playlist_name_from_id
from playlist_watch.system.manage_playlists_json import remove_playlist_by_id, remove_playlist_by_name


class RemovePlaylist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remove(self, ctx, playlist_identifier: str):
        # Extract the playlist ID from the URL
        match = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_identifier)
        if not match:
            remove_playlist_by_name(playlist_identifier)
            await ctx.send(f"Playlist '{playlist_identifier}' removed!")
        else:
            playlist_id = match.group(1)
            remove_playlist_by_id(playlist_id)
            await ctx.send(f"Playlist '{playlist_name_from_id(playlist_id)}' removed!")

async def setup(bot):
    await bot.add_cog(RemovePlaylist(bot))