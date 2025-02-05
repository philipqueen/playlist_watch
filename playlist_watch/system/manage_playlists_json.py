import json
import os

playlists_file_name = "playlists.json"
playlists_file_path = f"playlist_watch/{playlists_file_name}"

def get_playlists() -> dict:
    """
    Returns dictionary of playlists from playlists.json

    Key: playlist ID
    Value: dictionary with keys "name" and "channel_id"
    """
    if not os.path.exists(playlists_file_path) or os.path.getsize(playlists_file_path) == 0:
        # Initialize the file with an empty JSON object
        with open(playlists_file_path, 'w') as f:
            json.dump({}, f)
    with open(playlists_file_path, 'r') as f:
        playlists = json.load(f)
    return playlists

def add_playlist(playlist_id: str, playlist_name: str, channel_id: int) -> None:
    playlists = get_playlists()
    playlists[playlist_id] = {"name": playlist_name, "channel_id": channel_id}
    with open(playlists_file_path, 'w') as f:
        json.dump(playlists, f)

def remove_playlist_by_id(playlist_id: str) -> None:
    playlists = get_playlists()
    if playlist_id in playlists:
        del playlists[playlist_id]
    else:
        print(f"Playlist ID '{playlist_id}' not found.")
    with open(playlists_file_path, 'w') as f:
        json.dump(playlists, f)

def remove_playlist_by_name(playlist_name: str) -> None:
    playlists = get_playlists()
    playlist_found = False
    for playlist_id, name in playlists.items():
        if name == playlist_name:
            del playlists[playlist_id]
            playlist_found = True
            break
    if not playlist_found:
        print(f"Playlist '{playlist_name}' not found.")
    with open(playlists_file_path, 'w') as f:
        json.dump(playlists, f)