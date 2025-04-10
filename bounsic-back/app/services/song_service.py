from pickletools import pylong
from pymongo.errors import PyMongoError
from app.provider import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME
from azure.storage.blob import BlobServiceClient
from app.provider import db
from app.provider import DatabaseFacade
import re
from bson import ObjectId
from datetime import datetime


def getSongByTitle(song_title:str):
    songs_collection = db["songs"]
    song = songs_collection.find_one({"title": song_title})
    if song:
        if "_id" in song:
            song["_id"] = str(song["_id"])
        return song
    else:
        return {"message": "Song not found"}
    
def normalize_string(s: str) -> str:
    """Quita espacios y convierte a minúsculas para normalizar un string."""
    return re.sub(r"\s+", "", s).lower()

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
    # Perform a database operation
    results = db_facade.execute_query("SELECT VERSION()")
    if results:
        version = results.fetchone()
        print(f"MySQL Version: {version[0]}")
        return version[0]
    else:
        return None
    
def insert_song(body: dict):
    try:
        # Insertar la canción
        result = db["songs"].insert_one({
            "artist": body["artist"],
            "title": body["title"],
            "album": body["album"],
            "img_url": body["img_url"],
            "mp3_url": body["mp3_url"],
            "release_year": body["release_year"],
            "genres": body.get("genres", []),
            "fingerprint": body.get("fingerprint", [])
        })

        song_id = result.inserted_id

        # Buscar si ya existe el álbum por nombre
        album = db["albums"].find_one({"name": body["album"]})

        if album:
            # Si existe, insertar el ID de la canción al arreglo de songs
            db["albums"].update_one(
                {"_id": album["_id"]},
                {"$push": {"songs": {"song_id": song_id}}}
            )

        return {"message": "Song inserted", "song_id": str(song_id)}

    except PyMongoError as e:
        return {"error": "Database error", "details": str(e)}


