import requests
import pytz

from datetime import datetime, timedelta


from playlist_watch.spotify.api_setup import SpotifyAuth
from playlist_watch.spotify.get_user_id import get_user_id
from playlist_watch.spotify.urls import PLAYLIST_URL

timezone = 'America/Denver'

def get_playlist_tracks(playlist_id: str, headers: dict[str, str]) -> tuple[str, list[dict]]:
    response = requests.get(f'{PLAYLIST_URL}{playlist_id}', headers=headers)
    data = response.json()
    playlist_name = data.get('name', '')
    tracks = data.get('tracks', {}).get('items', [])
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
    if recent_tracks == recent_tracks_header:
        print("No recent tracks found.")
        recent_tracks = ""
    return recent_tracks

def get_recent_tracks(playlist_id: str = "7B3xmT5jmf7wdj8EQLq9yp", time_delay_hours: float = 1) -> str:
    headers = SpotifyAuth.get_request_headers()
    playlist_name, tracks = get_playlist_tracks(playlist_id, headers)
    return recent_tracks_str(tracks=tracks, playlist_name=playlist_name, headers=headers, max_delay_hours=time_delay_hours)

if __name__ == "__main__":
    playlist_id = "7B3xmT5jmf7wdj8EQLq9yp"
    
    headers = SpotifyAuth.get_request_headers()
    playlist_name, tracks = get_playlist_tracks(playlist_id, headers)
    print(recent_tracks_str(tracks=tracks, playlist_name=playlist_name, headers=headers, max_delay_hours=24))