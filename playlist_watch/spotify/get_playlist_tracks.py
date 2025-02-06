import asyncio
import aiohttp
import pytz

from datetime import datetime, timedelta


from playlist_watch.spotify.api_setup import SpotifyAuth
from playlist_watch.spotify.get_user_id import get_user_id
from playlist_watch.spotify.urls import PLAYLIST_URL

timezone = 'America/Denver'

async def get_recent_playlist_tracks(playlist_id: str, headers: dict[str, str], num_tracks_to_get: int = 20) -> tuple[str, list[dict]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{PLAYLIST_URL}{playlist_id}', headers=headers) as response:
            data = await response.json()
            playlist_name = data.get('name', '')
            total_tracks = data.get('tracks', {}).get('total', 0)

        offset = max(total_tracks - num_tracks_to_get, 0)
        
        async with session.get(f'{PLAYLIST_URL}{playlist_id}/tracks?limit={num_tracks_to_get}&offset={offset}', headers=headers) as response:
            data = await response.json()
            tracks = data.get('items', [])

    return playlist_name, tracks

def recent_tracks_str(tracks: list[dict], playlist_name: str, headers: dict[str, str], max_delay_hours: float = 1) -> str:
    recent_tracks_header = f"Recently added tracks to {playlist_name}:\n"
    recent_tracks = recent_tracks_header
    for track in tracks:
        if track["track"] is None:
            print("error reading track")
            print(track)
            continue
        track_name = track['track']['name']
        track_artist = track['track']['artists'][0]['name']
        added_by = track['added_by']['id']
        added_by_name = get_user_id(added_by, headers)
        time_added = track['added_at']
        utc_time = datetime.strptime(time_added, '%Y-%m-%dT%H:%M:%SZ')
        utc_time = pytz.utc.localize(utc_time)
        if utc_time >= datetime.now(pytz.utc) - timedelta(hours=max_delay_hours):
            local_time = utc_time.astimezone(pytz.timezone(timezone))
            time_added_formatted = local_time.strftime('%I:%M %p, %A %B %d')
            recent_tracks += f"{added_by_name} added **{track_name}** by *{track_artist}* to '{playlist_name}' at {time_added_formatted}\n"
        else:
            print(f"track {track_name} added by {added_by_name} at {time_added} is too old")
    if recent_tracks == recent_tracks_header:
        print("No recent tracks found.")
        recent_tracks = ""
    return recent_tracks

async def get_recent_tracks(playlist_id: str = "7B3xmT5jmf7wdj8EQLq9yp", time_delay_hours: float = 1) -> str:
    headers = SpotifyAuth.get_request_headers()
    playlist_name, tracks = await get_recent_playlist_tracks(playlist_id, headers)
    return recent_tracks_str(tracks=tracks, playlist_name=playlist_name, headers=headers, max_delay_hours=time_delay_hours)

if __name__ == "__main__":
    playlist_id = "7B3xmT5jmf7wdj8EQLq9yp"
    
    headers = SpotifyAuth.get_request_headers()
    playlist_name, tracks = asyncio.run(get_recent_playlist_tracks(playlist_id, headers))
    print(recent_tracks_str(tracks=tracks, playlist_name=playlist_name, headers=headers, max_delay_hours=24))