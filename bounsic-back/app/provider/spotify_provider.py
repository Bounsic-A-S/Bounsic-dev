import os
from dotenv import load_dotenv
from pathlib import Path
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

dotenv_path = Path(__file__).resolve().parent.parent.parent / "env" / ".env.dev"
if not load_dotenv(dotenv_path):
    print(f"⚠️ No se pudo cargar el archivo {dotenv_path}")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)



