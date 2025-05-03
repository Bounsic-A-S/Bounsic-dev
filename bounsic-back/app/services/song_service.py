from pymongo.errors import PyMongoError
from app.provider import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
from app.provider import db
from app.provider import DatabaseFacade
import re
import os
import traceback
from bson import ObjectId
from datetime import datetime
from app.services import Scrapping_service
class Song_service:
    @staticmethod
    def get_song_by_id(id:str):
        try:
            # connect to the MongoDB database
            songs_collection = db["songs"]
            
            # parsing the string id to ObjectId
            song_id = ObjectId(id)
            
            # searching for the song in the collection
            song = songs_collection.find_one({"_id": song_id})
            
            if song:
                song["_id"] = str(song["_id"])
                return song
            return None
            
        except Exception as e:
            print.error(f"Error getting song by ID {song_id}: {str(e)}")
            return None
        
    @staticmethod
    def normalize_string(s: str) -> str:
        """Quita espacios y convierte a minúsculas para normalizar un string."""
        return re.sub(r"\s+", "", s).lower()
    
    @staticmethod
    def getSongByTitle(song_title:str):
        songs_collection = db["songs"]
        song = songs_collection.find_one({"title": song_title})
        if song:
            if "_id" in song:
                song["_id"] = str(song["_id"])
            return song
        else:
            return {"message": "Song not found"}

    @staticmethod   
    def get_song_by_id(id: str):
        try:
            songs_collection = db["songs"]
            
            song_id = ObjectId(id.strip())

            song = songs_collection.find_one({"_id": song_id})
            
            if song:
                song["_id"] = str(song["_id"])  
                return song
            return None
            
        except Exception as e:
            print(f"Error getting song by ID {id}: {str(e)}")  
            return None

    @staticmethod 
    def get_songs_by_ids(ids: list[str]):
        try:
            songs_collection = db["songs"]
            
            object_ids = [ObjectId(id_) for id_ in ids if ObjectId.is_valid(id_)]
            
            songs_cursor = songs_collection.find({"_id": {"$in": object_ids}})
            songs = list(songs_cursor)

            for song in songs:
                song["_id"] = str(song["_id"])

            return songs
        except Exception as e:
            import traceback
            traceback.print_exc()
            return None
    @staticmethod
    def getSongByArtist(artist: str):
        try:
            songs_collection = db["songs"]
            normalized_artist = Song_service.normalize_string(artist)
            regex = re.compile(f"^{normalized_artist}$", re.IGNORECASE)
            songs = list(songs_collection.find({
                "$expr": {
                    "$eq": [
                        {"$toLower": {"$replaceAll": {"input": "$artist", "find": " ", "replacement": ""}}},
                        normalized_artist
                    ]
                }
            }))

            for song in songs:
                song["_id"] = str(song["_id"])

            return songs if songs else {"message": "No songs found for this artist"}

        except PyMongoError as e:
            return {"error": "Database error", "details": str(e)}
        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}
        
    @staticmethod 
    def getSongByTitle(title: str):
        try:
            songs_collection = db["songs"]
            normalized_title = Song_service.normalize_string(title)
            song = songs_collection.find_one({
                "$expr": {
                    "$eq": [
                        {"$toLower": {"$replaceAll": {"input": "$title", "find": " ", "replacement": ""}}},
                        normalized_title
                    ]
                }
            })

            if song:
                song["_id"] = str(song["_id"])
                return song

            return {"message": "Song not found"}

        except PyMongoError as e:
            return {"error": "Database error", "details": str(e)}
        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}

    @staticmethod
    def getSongByGenre(genre: str):
        try:
            songs_collection = db["songs"]
            songs = list(songs_collection.find({"genre": genre}))
            for song in songs:
                song["_id"] = str(song["_id"])
            return songs if songs else {"message": "No songs found for this genre"}
        except PyMongoError as e:
            return {"error": "Database error", "details": str(e)}
        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}

    @staticmethod
    def get_image(blob_name: str):
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        blob_client = container_client.get_blob_client(blob_name)
        if blob_client.exists():
            return blob_client.download_blob().readall()
        else:
            return {"message": "Image not found"}

    @staticmethod
    async def insert_image(file_path: str, blob_name: str) -> str:
        """
        Sube un archivo a Azure Blob Storage (versión corregida)
        
        Args:
            file_path: Ruta local del archivo
            blob_name: Nombre del blob en Azure
            
        Returns:
            URL pública del blob o None si falla
        """
        try:
            # Validaciones iniciales
            if not os.path.exists(file_path):
                print(f"Error: Archivo no encontrado: {file_path}")
                return None

            file_size = os.path.getsize(file_path)
            print(f"Subiendo archivo: {blob_name}, Tamaño: {file_size / (1024*1024):.2f} MB")

            # Configurar cliente de Azure
            blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
            container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

            # Subir archivo (versión simplificada)
            with open(file_path, "rb") as data:
                blob_client = container_client.get_blob_client(blob_name)
                
                # Usar upload_blob con overwrite=True
                blob_client.upload_blob(data, overwrite=True, blob_type="BlockBlob")
            
            print(f"Subida exitosa: {blob_name}")
            return f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{blob_name}"

        except AzureError as azure_error:
            print(f"Error de Azure al subir {blob_name}: {str(azure_error)}")
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"Error inesperado al subir {blob_name}: {str(e)}")
            traceback.print_exc()
            return None

    @staticmethod
    def mysql_db():
        db_facade = DatabaseFacade()
        results = db_facade.execute_query("SELECT VERSION()")
        if results:
            version = results.fetchone()
            print(f"MySQL Version: {version[0]}")
            return version[0]
        else:
            return None
    
    @staticmethod
    def insert_song(track_name: str):
        try:
            song_data = Song_service.generar_song_data(track_name)

            if not song_data:
                return {"error": "No se pudo generar la información de la canción"}

            result = db["songs"].insert_one(song_data)
            song_id = result.inserted_id

            album = db["albums"].find_one({"name": song_data["album"]})

            if album:
                db["albums"].update_one(
                    {"_id": album["_id"]},
                    {"$push": {"songs": {"song_id": song_id}}}
                )

            return {"message": "Song inserted", "song_id": str(song_id)}

        except PyMongoError as e:
            return {"error": "Database error", "details": str(e)}
        
    @staticmethod  
    def insert_song_mongo(song_data):
        try:

            if not song_data:
                return {"error": "No se pudo generar la información de la canción"}

            result = db["songs"].insert_one(song_data)
            song_id = result.inserted_id

            album = db["albums"].find_one({"name": song_data["album"]})

            if album:
                db["albums"].update_one(
                    {"_id": album["_id"]},
                    {"$push": {"songs": {"song_id": song_id}}}
                )

            return {"message": "Song inserted", "song_id": str(song_id)}

        except PyMongoError as e:
            return {"error": "Database error", "details": str(e)}

    @staticmethod
    def generar_song_data(track_name):
        from app.services import  Spotify_service
        video_url = Scrapping_service.buscar_en_youtube(track_name)
        if not video_url:
            print("No se encontró el video en YouTube.")
            return None

        metadata = Scrapping_service.scrappingBueno(video_url)
        info_extra = Spotify_service.get_artist_and_genre_by_track(track_name)

        if not metadata or not info_extra:
            print("No se pudo obtener metadata o info extra.")
            return None

        imagenes_album = Spotify_service.get_album_images(info_extra["album"], info_extra["artist_name"])
        img_url = imagenes_album[0]["url"] if imagenes_album else None

        descarga = Scrapping_service.descargar_audio(video_url)
        local_audio_path = descarga["audio"] if descarga and "audio" in descarga else None

        if not local_audio_path:
            print("No se pudo descargar el audio.")
            return None

        # Subir el archivo MP3 al Blob Storage
        # Puedes darle al blob el nombre de la canción como nombre del archivo
        audio_blob_name = f"audios/{info_extra['track_name'].replace(' ', '_')}.mp3"
        mp3_url = Song_service.insert_image(local_audio_path, audio_blob_name)  # <-- Aquí se sube y devuelve la URL

        release_year = int(metadata["publish_date"][:4]) if metadata.get("publish_date") and metadata["publish_date"] != "Fecha de publicación no encontrada" else 0

        song_data = {
            "artist": info_extra["artist_name"],
            "title": info_extra["track_name"],
            "album": info_extra["album"],
            "img_url": img_url,
            "mp3_url": mp3_url,  # Ahora es la URL del blob
            "release_year": release_year,
            "genres": [{"genre": g} for g in info_extra.get("genres", [])],
            "fingerprint": []
        }

        return song_data

    @staticmethod
    def searchArtist(artist_name: str):
        """
        Busca un artista por nombre exacto.
        
        Args:
            artist_name (str): Nombre del artista
        
        Returns:
            dict: Documento del artista si existe
            None: Si no existe
        """
        try:
            return db["artists"].find_one({
                "$or": [
                    {"name": artist_name},
                    {"artist_name": artist_name}
                ]
            })
        except PyMongoError:
            return None

    @staticmethod
    def searchAlbum(album_name: str, artist_id: ObjectId = None):
        """
        Busca un álbum por nombre y opcionalmente por artista.
        
        Args:
            album_name (str): Nombre del álbum
            artist_id (ObjectId, optional): ID del artista asociado
        
        Returns:
            dict: Documento del álbum si existe
            None: Si no existe
        """
        try:
            return db["albums"].find_one({
                "name": album_name,
                "artist.artist_id": artist_id  # Busca por ambos campos
            })
        except PyMongoError:
            return None

    @staticmethod     
    def search_song_exact(title: str, artist: str):
        """
        Busca una canción por título y artista exactos (case-sensitive).
        
        Args:
            title (str): Título exacto de la canción (case-sensitive)
            artist (str): Artista exacto (case-sensitive)
        
        Returns:
            dict: Documento completo de la canción si existe
            None: Si no existe o hay error
        
        """
        try:
            return db["songs"].find_one({
                "title": title,
                "artist": artist
            })
        except PyMongoError as e:
            print(f"Error en búsqueda exacta: {str(e)}")
            return None
        

    @staticmethod
    def insert_artist(name: str, artist_name: str, country: str = None, desc: str = None):
        """
        Inserta un nuevo artista en la base de datos.
        
        Args:
            name (str): Nombre del artista
            artist_name (str): Nombre artístico
            country (str, optional): País de origen
            desc (str, optional): Descripción del artista
        
        Returns:
            ObjectId: ID del artista insertado
            None: Si ocurre un error o el artista ya existe
        """
        try:
            # Verificar si el artista ya existe
            if db["artists"].find_one({"$or": [{"name": name}, {"artist_name": artist_name}]}):
                return None

            artist_data = {
                "name": name,
                "artist_name": artist_name,
                "country": country,
                "desc": desc,
                "albums": []
            }

            result = db["artists"].insert_one(artist_data)
            return result.inserted_id

        except PyMongoError:
            return None

    @staticmethod
    def insert_album(name: str, artist_id: ObjectId, release_year: int = None, img_url: str = None):
        """
        Inserta un nuevo álbum o devuelve el ID si ya existe.
        
        Args:
            name (str): Nombre del álbum
            artist_id (ObjectId): ID del artista
            release_year (int, optional): Año de lanzamiento
            img_url (str, optional): URL de la imagen del álbum
        
        Returns:
            ObjectId: ID del álbum (existente o nuevo)
            None: Si ocurre un error
        """
        try:
            # Verificar si el artista existe
            artist = db["artists"].find_one({"_id": artist_id})
            if not artist:
                return None

            # Verificar si el álbum ya existe
            existing_album = db["albums"].find_one({"name": name, "artist": artist_id})
            if existing_album:
                return existing_album["_id"]

            # Crear nuevo álbum
            album_data = {
                "name": name,
                "release_year": release_year,
                "img_url": img_url,
                "artist": artist_id,
                "songs": []
            }

            album_result = db["albums"].insert_one(album_data)
            return album_result.inserted_id

        except PyMongoError:
            return None


    @staticmethod
    def add_album_to_artist(artist_id: ObjectId, album_id: ObjectId):
        """
        Asocia un álbum existente a un artista.
        
        Args:
            artist_id (ObjectId): ID del artista
            album_id (ObjectId): ID del álbum
        
        Returns:
            bool: True si la operación fue exitosa
            False: Si ocurre un error o ya están asociados
        """
        try:
            # Verificar si ya están asociados
            artist = db["artists"].find_one({
                "_id": artist_id,
                "albums.album_id": album_id
            })
            if artist:
                return False

            # Actualizar artista
            result = db["artists"].update_one(
                {"_id": artist_id},
                {"$push": {"albums": {"album_id": album_id}}}
            )

            return result.modified_count > 0

        except PyMongoError:
            return False

    @staticmethod
    def add_artist_to_album(artist_id: ObjectId, album_id: ObjectId):
        """
        Asocia un álbum existente a un artista.
        
        Args:
            artist_id (ObjectId): ID del artista
            album_id (ObjectId): ID del álbum
        
        Returns:
            bool: True si la operación fue exitosa
            False: Si ocurre un error o ya están asociados
        """
        try:
            # Verificar si ya están asociados
            album = db["album"].find_one({
                "_id": artist_id,
                "artist.artist_id": artist_id
            })
            if album:
                return False

            # Actualizar artista
            result = db["album"].update_one(
                {"_id": album_id},
                {"$push": {"artist": {"artist_id": artist_id}}}
            )

            return result.modified_count > 0

        except PyMongoError:
            return False
        
    @staticmethod
    def add_song_to_album(album_id: ObjectId, song_id: ObjectId) -> bool:
        """
        Agrega una canción existente a un álbum, si no está ya asociada.

        Args:
            album_id (ObjectId): ID del álbum
            song_id (ObjectId): ID de la canción

        Returns:
            bool: True si se insertó, False si ya existía o hubo error
        """
        try:
            result = db["albums"].update_one(
                {"_id": album_id, "songs.song_id": {"$ne": song_id}},  # Solo si NO existe
                {"$push": {"songs": {"song_id": song_id}}}
            )

            return result.modified_count > 0  # True si de verdad modificó algo

        except PyMongoError as e:
            print(f"Error al agregar canción al álbum: {e}")
            return False

    @staticmethod
    def update_song_lyrics(song_id:ObjectId, lyrics):
        """
        Agrega un campo 'lyrics' a una canción existente en la base de datos.

        Args:
            song_id (ObjectId): ID de la canción a actualizar.
            lyrics (str): Letra de la canción a agregar.

        Returns:
            bool: True si se actualizó, False si no se modificó o hubo error.
        """
        try:
            result = db["songs"].update_one(
                {"_id":song_id},
                {"$set":{"lyrics": lyrics}}
            )
            return result.modified_count > 0

        except PyMongoError as e:
            print(f"Error al agregar letras a la canción: {e}")
            return False