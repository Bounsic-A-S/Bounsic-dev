import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "e873f0ae04bd4ea7ae99523409cbf29d"
client_secret = "2cc6c6f926284fcab5487389fcdbd556"

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_album_images(album_name, artist_name=None):
    query = f"{album_name} {artist_name or ''}".strip()
    print(f"Buscando portada de álbum: {query}")
    
    result = sp.search(q=query, type="album", limit=1)
    
    print("\n>>> Respuesta de Spotify:")
    print(result)
    
    if not result['albums']['items']:
        print(f"No se encontró el álbum: {query}")
        return
    
    album = result['albums']['items'][0]
    print(f"\nÁlbum encontrado: {album['name']} - {album['artists'][0]['name']}")
    
    return album['images']
