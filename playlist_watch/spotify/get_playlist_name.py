import requests
import pytz

from datetime import datetime, timedelta


from playlist_watch.spotify.api_setup import SpotifyAuth
from playlist_watch.spotify.get_user_id import get_user_id
from playlist_watch.spotify.urls import PLAYLIST_URL

timezone = 'America/Denver'

def get_playlist_name(playlist_id: str, headers: dict[str, str]) -> str:
    response = requests.get(f'{PLAYLIST_URL}{playlist_id}', headers=headers)
    data = response.json()
    playlist_name = data.get('name', '')
    return playlist_name



if __name__ == "__main__":
    playlist_id = "7B3xmT5jmf7wdj8EQLq9yp"
    
    headers = SpotifyAuth.get_request_headers()
    playlist_name = get_playlist_name(playlist_id, headers)
    print(playlist_name)