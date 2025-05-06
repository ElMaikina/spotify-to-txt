import os
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from concurrent.futures import ThreadPoolExecutor, as_completed

# 📄 Load credentials
print("Cargando las credenciales...")
def load_credentials(path="C:/Users/ElMaikina/Documents/Credentials/spotify-to-text.txt"):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
        if len(lines) < 4:
            raise ValueError("spotify_credentials.txt must have 4 lines: client_id, client_secret, redirect_uri, scope")
        return {
            "client_id": lines[0],
            "client_secret": lines[1],
            "redirect_uri": lines[2],
            "scope": lines[3]
        }
print("Credenciales cargadas!")

# 🧠 Authenticate with Spotify
print("Autentificando las credenciales...")
creds = load_credentials()
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=creds["client_id"],
    client_secret=creds["client_secret"],
    redirect_uri=creds["redirect_uri"],
    scope=creds["scope"]
))
print("Credenciales autentificadas!")

# 🧩 Mapper: fetch track list for album
print("Cargando los Albumes...")
def fetch_album_tracks(album_obj):
    album = album_obj['album']
    album_name = f"{album['name']} - {album['artists'][0]['name']}"
    tracks = []
    results = sp.album_tracks(album['id'])
    for item in results['items']:
        tracks.append(f"{item['track_number']:02d}. {item['name']}")
    return album_name, tracks

# 🧩 Mapper: fetch track list for playlist
print("Cargando las PlayLists...")
def fetch_playlist_tracks(playlist_obj):
    playlist_name = playlist_obj['name']
    tracks = []
    offset = 0
    while True:
        items = sp.playlist_items(playlist_obj['id'], offset=offset)
        if not items['items']:
            break
        for item in items['items']:
            track = item.get('track')
            if track:
                name = track['name']
                artist = track['artists'][0]['name']
                tracks.append(f"{artist} - {name}")
        offset += len(items['items'])
    return playlist_name, tracks

# 📁 Create a separate folder for each type
album_dir = "albums"
playl_dir = "lists"
os.makedirs(album_dir, exist_ok=True)
os.makedirs(playl_dir, exist_ok=True)

# 🧹 Reducer: write to text file
def save_album(title, tracks):
    safe_name = "".join(c for c in title if c.isalnum() or c in " -_").strip().replace(" ", "_")
    path = os.path.join(album_dir, f"{safe_name}.txt")
    with open(path, "w", encoding="utf-8") as f:
        for line in tracks:
            f.write(line + "\n")

# 🧹 Reducer: write to text file
def save_playl(title, tracks):
    safe_name = "".join(c for c in title if c.isalnum() or c in " -_").strip().replace(" ", "_")
    path = os.path.join(playl_dir, f"{safe_name}.txt")
    with open(path, "w", encoding="utf-8") as f:
        for line in tracks:
            f.write(line + "\n")
                    
# 📥 Get all saved albums
def get_all_albums():
    albums = []
    offset = 0
    while True:
        batch = sp.current_user_saved_albums(limit=50, offset=offset)
        items = batch['items']
        if not items:
            break
        albums.extend(items)
        offset += 50
    return albums

# 📥 Get all playlists
def get_all_playlists():
    playlists = []
    offset = 0
    while True:
        batch = sp.current_user_playlists(limit=50, offset=offset)
        items = batch['items']
        if not items:
            break
        playlists.extend(items)
        offset += 50
    return playlists

# 🧠 MapReduce runner
def run():
    albums = get_all_albums()
    playlists = get_all_playlists()

    print(f"🟢 Found {len(albums)} albums and {len(playlists)} playlists.")
    tasks = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        # Map albums
        album_futures = {executor.submit(fetch_album_tracks, a): a for a in albums}
        
        # Map playlists
        playlist_futures = {executor.submit(fetch_playlist_tracks, p): p for p in playlists}
        
        # Reduce: write each result to file
        for future in as_completed(album_futures):
            title, tracks = future.result()
            save_album(title, tracks)
            print(f"✅ Saved: {title}")
        
        # Reduce: write each result to file
        for future in as_completed(playlist_futures):
            title, tracks = future.result()
            save_playl(title, tracks)
            print(f"✅ Saved: {title}")

if __name__ == "__main__":
    run()
