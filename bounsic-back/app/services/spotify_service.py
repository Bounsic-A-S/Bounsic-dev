from app.provider import sp

def get_album_images(album_name, artist_name=None):
    query = f"{album_name} {artist_name or ''}".strip()

    try:
        result = sp.search(q=query, type="album", limit=1)

        if not result.get('albums', {}).get('items'):
            print(f"No se encontró el álbum: {album_name}")
            return None

        album = result['albums']['items'][0]
        return album.get('images', [])
    
    except Exception as e:
        print(f"Error al obtener imágenes del álbum: {e}")
        return None

def get_artist_and_genre_by_track(track_name):
    try:
        result = sp.search(q=track_name, type="track", limit=1)

        if not result.get('tracks', {}).get('items'):
            print(f"No se encontró la canción: {track_name}")
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
    
    except Exception as e:
        print(f"Error al obtener información del track: {e}")
        return None

def get_artists_by_genre(genre, limit=2):
    try:
        result = sp.search(q=f'genre:"{genre}"', type="artist", limit=limit)

        if not result.get('artists', {}).get('items'):
            print(f"No se encontraron artistas para el género: {genre}")
            return None

        tracks_info = []
        for artist in result['artists']['items']:
            tracks_info.append({
                'artist_name': artist['name'],
                'img': artist['images'][0]['url'] if artist['images'] else None
            })

        return tracks_info
    
    except Exception as e:
        print(f"Error al obtener artistas del género: {e}")
        return None

def get_playlist_id_by_name(playlist_name):
    try:
        result = sp.search(playlist_name, type="playlist")  # Asegúrate de que esta función devuelva un diccionario válido
        
        if not result.get('playlists', {}).get('items'):
            print(f"Error: No se encontraron listas de reproducción con el nombre: {playlist_name}")
            return None

        playlist_id = result['playlists']['items'][0]['id']
        return playlist_id
    
    except Exception as e:
        print(f"Error al obtener el ID de la playlist: {e}")
        return None

def get_top_tracks_global(limit=12):
    playlist_name = "Top 50 Global"
    
    # Obtener el ID de la playlist
    playlist_id =  "37i9dQZEVXbMDoHDwVN2tF"#get_playlist_id_by_name(playlist_name)
    print(f"Playlist ID: {playlist_id}")

    
    if playlist_id:
        try:
            # Obtener los primeros 50 tracks de la playlist
            result = sp.playlist_tracks(playlist_id, limit=limit)
            
            if not result.get('items'):
                print("No se encontraron tracks en el top global.")
                return None

            top_tracks = []

            # Extraer la información relevante de las canciones
            for item in result['items']:
                track = item['track']
                top_tracks.append({
                    'track_name': track['name'],
                    'artist_name': track['artists'][0]['name'],
                    'album_name': track['album']['name'],
                    'album_images': track['album']['images']
                })
            
            return top_tracks
        
        except Exception as e:
            print(f"Error al obtener los tracks: {e}")
            return None
    else:
        print("No se pudo obtener el ID de la playlist.")
        return None
