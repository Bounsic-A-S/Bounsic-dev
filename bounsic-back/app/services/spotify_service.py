from app.provider import sp
def get_album_images(album_name, artist_name=None):
    query = f"{album_name} {artist_name or ''}".strip()
    
    result = sp.search(q=query, type="album", limit=1)
    
    if not result['albums']['items']:
        print(" No se encontró el álbum.")
        return None

    album = result['albums']['items'][0]
   
    
    return album['images']

def get_artist_and_genre_by_track(track_name):
    result = sp.search(q=track_name, type="track", limit=1)

    if not result['tracks']['items']:
        print("No se encontró la canción.")
        return None

    track = result['tracks']['items'][0]
    artist_id = track['artists'][0]['id']
    artist_name = track['artists'][0]['name']

    artist_info = sp.artist(artist_id)
    genres = artist_info.get('genres', [])

    album_name = track['album']['name'] if 'album' in track else None

    return {
        'track_name': track['name'],
        'artist_name': artist_name,
        'genres': genres,
        'album': album_name
    }
