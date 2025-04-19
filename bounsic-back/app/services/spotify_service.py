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
    
def get_artists_by_genre(genre, limit=2):
    # Buscar artistas por género
    result = sp.search(q=f'genre:"{genre}"', type="artist", limit=limit)

    if not result['artists']['items']:
        print("No se encontraron artistas para ese género.")
        return None

    tracks_info = []

    for artist in result['artists']['items']:
        tracks_info.append({
            'artist_name': artist['name'],
            'img': artist['images'][0]['url']
        })

    return tracks_info
