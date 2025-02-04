import os
import requests
from requests.auth import HTTPBasicAuth

def get_access_token() -> str:
    client_id = os.getenv('SPOTIFY_ID')
    client_secret = os.getenv('SPOTIFY_SECRET')

    if client_id is None or client_secret is None:
        raise ValueError("Spotify credentials are not set in environment variables.")

    auth_response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={'grant_type': 'client_credentials'},
        auth=HTTPBasicAuth(client_id, client_secret)
    )
    access_token = auth_response.json().get('access_token')
    return access_token

def get_request_headers(access_token: str | None) -> dict[str, str]:
    if access_token is None:
        access_token = get_access_token()
    return {'Authorization': f'Bearer {access_token}'}