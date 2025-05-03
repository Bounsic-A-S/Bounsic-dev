from pymongo.errors import PyMongoError
from app.provider import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME
from azure.storage.blob import BlobServiceClient
from app.provider import db
from app.provider import DatabaseFacade
import re
from bson import ObjectId
from app.services import scrappingBueno,buscar_en_youtube,descargar_audio
from app.services.spotify_service import get_artist_and_genre_by_track, get_album_images
from app.services.lastfm_service import get_top_tracks_lastfm


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

def normalize_string(s: str) -> str:
    """Quita espacios y convierte a minúsculas para normalizar un string."""
    return re.sub(r"\s+", "", s).lower()

def getSongByTitle(song_title:str):
    songs_collection = db["songs"]
    song = songs_collection.find_one({"title": song_title})
    if song:
        if "_id" in song:
            song["_id"] = str(song["_id"])
        return song
    else:
        return {"message": "Song not found"}
    
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

def getSongByArtist(artist: str):
    try:
        songs_collection = db["songs"]
        normalized_artist = normalize_string(artist)
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
    
def getSongByTitle(title: str):
    try:
        songs_collection = db["songs"]
        normalized_title = normalize_string(title)
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

def get_image(blob_name: str):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
    blob_client = container_client.get_blob_client(blob_name)
    if blob_client.exists():
        return blob_client.download_blob().readall()
    else:
        return {"message": "Image not found"}

def insert_image(file_url: str, blob_name: str):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
    
    with open(file_url, "rb") as data:
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)

    # Construir URL de acceso
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{blob_name}"

def mysql_db():
    db_facade = DatabaseFacade()
    results = db_facade.execute_query("SELECT VERSION()")
    if results:
        version = results.fetchone()
        print(f"MySQL Version: {version[0]}")
        return version[0]
    else:
        return None
    
def insert_song(track_name: str):
    try:
        song_data = generar_song_data(track_name)

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

def generar_song_data(track_name):
    video_url = buscar_en_youtube(track_name)
    if not video_url:
        print("No se encontró el video en YouTube.")
        return None

    metadata = scrappingBueno(video_url)
    info_extra = get_artist_and_genre_by_track(track_name)

    if not metadata or not info_extra:
        print("No se pudo obtener metadata o info extra.")
        return None

    imagenes_album = get_album_images(info_extra["album"], info_extra["artist_name"])
    img_url = imagenes_album[0]["url"] if imagenes_album else None

    descarga = descargar_audio(video_url)
    local_audio_path = descarga["audio"] if descarga and "audio" in descarga else None

    if not local_audio_path:
        print("No se pudo descargar el audio.")
        return None

    # Subir el archivo MP3 al Blob Storage
    # Puedes darle al blob el nombre de la canción como nombre del archivo
    audio_blob_name = f"audios/{info_extra['track_name'].replace(' ', '_')}.mp3"
    mp3_url = insert_image(local_audio_path, audio_blob_name)  # <-- Aquí se sube y devuelve la URL

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

def get_complete_top_12():
    try:
        top_tracks = get_top_tracks_lastfm()  # Devuelve lista de títulos
        if not top_tracks:
            return {"error": "No se pudieron obtener las canciones desde Last.fm"}

        result = []
        for track_name in top_tracks:
            # Verificar si ya está en la base de datos
            song = getSongByTitle(track_name)

            # Si no existe, intenta insertarla
            if song is None or song.get("message") == "Song not found":
                insert_result = insert_song(track_name)
                if "song_id" in insert_result:
                    song = getSongByTitle(track_name)
                else:
                    print(f"Error insertando canción {track_name}: {insert_result}")
                    continue  # Salta si no se pudo insertar

            # Armar respuesta
            if song:
                result.append({
                    "title": song.get("title"),
                    "album": song.get("album"),
                    "image": song.get("img_url"),
                    "audio": song.get("mp3_url")
                })

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": "Error procesando las canciones", "details": str(e)}