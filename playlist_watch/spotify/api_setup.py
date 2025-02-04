import os
import requests
from requests.auth import HTTPBasicAuth
import time

class SpotifyAuth:
    _access_token = None
    _token_expiry = 0
    _client_id = os.getenv('SPOTIFY_ID')
    _client_secret = os.getenv('SPOTIFY_SECRET')

    @classmethod
    def get_access_token(cls) -> str:
        if time.time() >= cls._token_expiry:
            if cls._client_id is None or cls._client_secret is None:
                raise ValueError("Spotify credentials are not set in environment variables.")

            auth_response = requests.post(
                'https://accounts.spotify.com/api/token',
                data={'grant_type': 'client_credentials'},
                auth=HTTPBasicAuth(cls._client_id, cls._client_secret)
            )
            auth_data = auth_response.json()
            cls._access_token = auth_data.get('access_token')
            expires_in = auth_data.get('expires_in')
            cls._token_expiry = time.time() + expires_in - 60  # Refresh a minute early for safety

        if cls._access_token is None:
            raise ValueError("Failed to get access token.")
            
        return cls._access_token

    @classmethod
    def get_request_headers(cls) -> dict[str, str]:
        access_token = cls.get_access_token()
        return {'Authorization': f'Bearer {access_token}'}