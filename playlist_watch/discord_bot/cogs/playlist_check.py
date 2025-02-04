from discord.ext import commands, tasks
from logging import getLogger

from playlist_watch.spotify.get_playlist_tracks import get_recent_tracks

logger = getLogger(__name__)

test_channel_id = 1335153750637281300

class PlaylistCheck(commands.Cog):
    def __init__(self, bot, channel_id: int = test_channel_id):
        self.bot = bot
        self.channel_id = channel_id
        self.check_playlist.start()

    @tasks.loop(seconds=60*60)
    async def check_playlist(self):
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            logger.error(f"Channel not found: {self.channel_id}")
            raise ValueError(f"Channel not found: {self.channel_id}")
        logger.info("Checking playlist...")
        recent_tracks = get_recent_tracks()
        if recent_tracks == "":
            logger.info("No recent tracks found.")
            return
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