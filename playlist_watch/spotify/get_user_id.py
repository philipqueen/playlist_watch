import requests

from playlist_watch.spotify.urls import USER_URL

spotify_id_to_name = {}

def get_user_id(spotify_id: str, headers: dict[str, str]) -> str:
    if not spotify_id in spotify_id_to_name:
        response = requests.get(f'{USER_URL}{spotify_id}', headers=headers)
        user_data = response.json()
        spotify_id_to_name[spotify_id] = user_data['display_name']
    return spotify_id_to_name[spotify_id]