from app.provider import sp

class Spotify_service:
    
    @staticmethod
    def get_album_images(album_name, artist_name=None):
        query = f"{album_name} {artist_name or ''}".strip()
        
        result = sp.search(q=query, type="album", limit=1)
        
        if not result['albums']['items']:
            print(" No se encontró el álbum.")
            return None

        album = result['albums']['items'][0]
    
        
        return album['images']

    @staticmethod
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
    
    @staticmethod   
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

    @staticmethod
    def get_track_details(track_name, artist_name=None):
        """
        Obtiene detalles de una canción: imagen del álbum, año de lanzamiento y géneros.
        
        Args:
            track_name (str): Nombre de la canción.
            artist_name (str, optional): Nombre del artista (opcional para mayor precisión).
        
        Returns:
            dict: Diccionario con:
                - 'image_url' (str): URL de la imagen del álbum.
                - 'release_year' (str): Año de lanzamiento (ej: "1982").
                - 'genres' (list): Lista de géneros asociados al artista.
                - 'artist' (str): Nombre del artista principal.
                - 'album' (str): Nombre del álbum.
            None: Si no se encuentra la canción.
        """
        query = f"track:{track_name}"
        if artist_name:
            query += f" artist:{artist_name}"
        
        result = sp.search(q=query, type="track", limit=1)
        
        if not result['tracks']['items']:
            print(f"No se encontró la canción: {track_name}")
            return None
        
        track = result['tracks']['items'][0]
        album = track['album']
        
        # Obtener géneros del artista principal
        artist_id = track['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        genres = artist_info.get('genres', [])
        
        # Obtener año de lanzamiento (formato: "YYYY-MM-DD" -> extraer solo el año)
        release_year = album['release_date'].split('-')[0] if album.get('release_date') else "Desconocido"
        
        return {
            'image_url': album['images'][0]['url'] if album.get('images') else None,
            'release_year': release_year,
            'genres': genres,
            'artist': track['artists'][0]['name'],
            'album': album['name'],
            'track_name': track['name']
        }

    @staticmethod
    def get_artist_info(artist_name: str):
        """
        Obtiene información completa de un artista desde Spotify y la formatea
        para coincidir con tu esquema de MongoDB.
        
        Args:
            artist_name (str): Nombre del artista a buscar
        
        Returns:
            dict: {
                "name": str,               # Nombre real
                "artist_name": str,        # Nombre artístico (puede ser igual)
                "country": str,            # País (del primer mercado disponible)
                "desc": str,              # Géneros como descripción
                "albums": list,           # Lista vacía (se llena después)
                "spotify_data": {         # Datos adicionales de Spotify
                    "genres": list,
                    "popularity": int,
                    "image_url": str
                }
            }
            None: Si no se encuentra el artista
        """
        try:
            # Buscar artista en Spotify
            result = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
            if not result['artists']['items']:
                print(f"No se encontró el artista: {artist_name}")
                return None

            artist = result['artists']['items'][0]
            artist_id = artist['id']
            
            # Obtener detalles completos del artista
            artist_details = sp.artist(artist_id)

            # Formatear según tu esquema
            artist_data = {
                "name": artist_details.get('name', artist_name),
                "artist_name": artist_details.get('name', artist_name),
                "country": artist_details.get('country', 
                        artist_details.get('markets', [''])[0] if artist_details.get('markets') else ''),
                "desc": ", ".join(artist_details.get('genres', ['Sin descripción'])),
                "albums": []  # Se poblará después con album_ids
            }

            return artist_data

        except Exception as e:
            print(f"Error al obtener artista de Spotify: {str(e)}")
            return None
        
    @staticmethod
    def get_album_info(album_name: str, artist_name: str = None):
        """
        Obtiene información de un álbum desde Spotify y la formatea para tu esquema MongoDB
        
        Args:
            album_name (str): Nombre del álbum
            artist_name (str, optional): Nombre del artista para búsqueda más precisa
        
        Returns:
            dict: {
                "name": str,               # Nombre del álbum
                "release_year": int,       # Año de lanzamiento
                "img_url": str,            # URL de la imagen principal
                "artist": {                # Información básica del artista
                    "spotify_id": str,     # ID en Spotify (para referencia)
                    "name": str            # Nombre del artista
                },
                "spotify_data": {          # Datos adicionales
                    "tracks": list,        # Lista de canciones
                    "genres": list,        # Géneros asociados
                    "album_id": str        # ID en Spotify
                }
            }
            None: Si no se encuentra el álbum
        """
        try:
            # Construir query de búsqueda
            query = f"album:{album_name}"
            if artist_name:
                query += f" artist:{artist_name}"
            
            # Buscar en Spotify
            result = sp.search(q=query, type='album', limit=1)
            if not result['albums']['items']:
                print(f"No se encontró el álbum: {album_name}")
                return None

            album = result['albums']['items'][0]
            album_id = album['id']
            
            # Obtener detalles completos del álbum
            album_details = sp.album(album_id)
            
            # Obtener todas las canciones del álbum
            tracks = []
            for track in album_details['tracks']['items']:
                tracks.append({
                    "name": track['name'],
                    "duration_ms": track['duration_ms'],
                    "spotify_id": track['id']
                })

            # Extraer año de lanzamiento (solo el año)
            release_date = album_details.get('release_date', '')
            release_year = int(release_date.split('-')[0]) if release_date else 0

            # Formatear según tu esquema
            album_data = {
                "name": album_details['name'],
                "release_year": release_year,
                "img_url": album_details['images'][0]['url'] if album_details['images'] else None,
                "artist": album_details['artists'][0]['name'],
                "songs": tracks,
                "total_songs": album_details['total_tracks']
            }

            return album_data

        except Exception as e:
            print(f"Error al obtener álbum de Spotify: {str(e)}")
            return None