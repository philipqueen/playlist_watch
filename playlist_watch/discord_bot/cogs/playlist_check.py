from discord.ext import commands, tasks
from logging import getLogger

from playlist_watch.spotify.get_playlist_tracks import get_recent_tracks
from playlist_watch.system.manage_playlists_json import get_playlists

logger = getLogger(__name__)

test_channel_id = 1335153750637281300

time_delay_hours = 1

class PlaylistCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_playlist.start()

    @tasks.loop(seconds=60*60*time_delay_hours)
    async def check_playlist(self):
        playlists = get_playlists()
        for playlist_id, playlist_info in playlists.items():
            channel_id = playlist_info.get("channel_id", None)
            channel = self.bot.get_channel(channel_id)
            if not channel:
                logger.error(f"Channel not found: {channel_id}")
                raise ValueError(f"Channel not found: {channel_id}")    
            logger.info(f"Checking playlist {playlist_info["name"]}...")
            recent_tracks = await get_recent_tracks(playlist_id=playlist_id, time_delay_hours=time_delay_hours)
            if recent_tracks == "":
                logger.info(f"No recent tracks found in playlist {playlist_info["name"]}...")
                continue
            logger.info("Sending recent tracks message...")
            await self.send_long_message(channel, recent_tracks)

    @check_playlist.before_loop
    async def before_my_task(self):
        await self.bot.wait_until_ready()

    async def send_long_message(self, channel, content):
        max_chars = 2000
        while content:
            if len(content) <= max_chars:
                await channel.send(content)
                break
            split_index = content.rfind('\n', 0, max_chars)
            if split_index == -1:
                split_index = max_chars  # Fallback if no newline is found
            to_send = content[:split_index]
            await channel.send(to_send)
            content = content[split_index:].lstrip('\n')

async def setup(bot):
    await bot.add_cog(PlaylistCheck(bot))