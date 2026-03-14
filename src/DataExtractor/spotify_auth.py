import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


# Define required scopes for accessing user data
load_dotenv()
SCOPE = 'user-read-private user-read-email user-library-read user-top-read user-read-recently-played playlist-read-private'
REDIRECT_URI = 'https://127.0.0.1:8080'
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']


def get_spotify_client():
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )
    try:
        print("## Authentication successful!")
        return spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        print(f"ERROR get_spotify_client: {e}")
