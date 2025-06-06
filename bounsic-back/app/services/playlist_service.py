from datetime import datetime
import logging
from typing import Optional
from bson import ObjectId
from app.provider import db
from pymongo.errors import PyMongoError


class Playlist_service:
    @staticmethod
    def getPlaylistById(playlist_id: str):
        try:
            playlists_collection = db["playlists"]
            songs_collection = db["songs"]

            playlist_obj_id = ObjectId(playlist_id)

            playlist = playlists_collection.find_one({"_id": playlist_obj_id})
            if not playlist:
                return {"message": "Playlist not found"}

            song_ids = [song["song_id"] for song in playlist.get("songs", [])]

            songs = list(songs_collection.find(
                {"_id": {"$in": song_ids}}, 
                {"fingerprint": 0, "genres": 0, "lyrics": 0}
            ))


            for song in songs:
                song["_id"] = str(song["_id"])

            return {
                "id": str(playlist["_id"]),
                "title": playlist.get("playlist_name"),
                "songs": songs,
                "isPublic": playlist.get("isPublic", False),
                "img_url": playlist.get("img_url", ""),
                "updated_at": playlist.get("updated_at").isoformat() if playlist.get("updated_at") else None
            }

        except PyMongoError as e:
            return {"error": "Database error", "details": str(e)}
        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}
        
    @staticmethod
    def getPlaylistById_libray(playlist_id: str):
        try:
            playlists_collection = db["playlists"]
            songs_collection = db["songs"]

            playlist_obj_id = ObjectId(playlist_id)

            playlist = playlists_collection.find_one({"_id": playlist_obj_id})
            if not playlist:
                return {"message": "Playlist not found"}

            song_ids = [song["song_id"] for song in playlist.get("songs", [])]

            songs = list(songs_collection.find(
                {"_id": {"$in": song_ids}}, 
                {"fingerprint": 0, "genres": 0, "lyrics": 0}
            ))


            for song in songs:
                song["_id"] = str(song["_id"])

            return {
                "id": str(playlist["_id"]),
                "title": playlist.get("playlist_name"),
                "song_count": len(songs),
                "isPublic": playlist.get("isPublic", False),
                "img_url": playlist.get("img_url", ""),
            }

        except PyMongoError as e:
            return {"error": "Database error", "details": str(e)}
        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}
        
    @staticmethod
    def getAllPlaylists():
        try:
            playlists_collection = db["playlists"]

            playlists = list(playlists_collection.find())

            for playlist in playlists:
                playlist["_id"] = str(playlist["_id"])
                if "songs" in playlist:
                    playlist["songs"] = [
                        {"song_id": str(song["song_id"])} for song in playlist["songs"]
                    ]

            return playlists
        except PyMongoError as e:
            return {"error": "Database error", "details": str(e)}
        except Exception as e:
            return {"error": "Unexpected error", "details": str(e)}
        
    @staticmethod
    async def create_user_playlist(user_id: int, playlist_name: str, img_url: Optional[str] = None):
        try:
            from  app.services import MySQLSongService
            playlist = db["playlists"]
            DEFAULT_IMAGE_URL = "https://bounsicmetadata.blob.core.windows.net/imgs/Default_Playlist_img.jpg"
            img_url = img_url.strip() if isinstance(img_url, str) and img_url else DEFAULT_IMAGE_URL

            new_playlist = {
                "playlist_name": playlist_name,
                "isPublic": True,
                "songs": [],
                "img_url": img_url,
                "updated_at": datetime.utcnow()
            }

            result = playlist.insert_one(new_playlist)
            mongo_playlist_id = str(result.inserted_id)
            print("Playlist creada en MongoDB con ID:", mongo_playlist_id)

            data = {
                "plist_name": playlist_name,
                "playlist_desc": "",  
                "playlist_mongo_id": mongo_playlist_id,
                "user_id": user_id
            }

            await MySQLSongService.insert_playlist(data)

            return mongo_playlist_id

        except Exception as e:
            logging.error(f"Error al crear la playlist: {e}")
            return None
    
    @staticmethod
    async def add_song_to_playlist(playlist_id: str, song_id: str):
            try:
                playlists = db["playlists"]
                songs = db["songs"]

                # Verificar si la canción existe
                song_exists = songs.find_one({"_id": ObjectId(song_id)})
                if not song_exists:
                    return {"error": " La canción no existe"}

                # Agregar la canción al array de la playlist
                result = playlists.update_one(
                    {"_id": ObjectId(playlist_id)},
                    {"$addToSet": {"songs":{"song_id": ObjectId(song_id)}}}
                )

                if result.modified_count == 0:
                    return {"message": "La canción ya estaba en la playlist o la playlist no existe"}

                return {
                    "message": "Canción agregada exitosamente",
                    "playlist_id": playlist_id,
                    "song_id": song_id
                }

            except PyMongoError as e:
                logging.error(f"MongoDB error al agregar canción: {e}")
                return {"error": "Error al agregar la canción a la playlist"}
            except Exception as e:
                logging.error(f"Error inesperado: {e}")
                return {"error": "Error inesperado"}
    @staticmethod
    async def delete_playlist(playlist_id: int):
        try:
            from app.services import MySQLSongService
            result = await MySQLSongService.get_playlist_by_id(playlist_id)
            if not result:
                return {"error": "Playlist not found or not owned by user."}

            if isinstance(result, list):
                result = result[0]

            playlist_mongo_id = result["playlist_mongo_id"]
            print(playlist_mongo_id)
            mongo_coll = db["playlists"]
            mongo_result = mongo_coll.delete_one({"_id": ObjectId(playlist_mongo_id)})
            if mongo_result.deleted_count <= 0:
                logging.warning(f"Playlist {playlist_mongo_id} not found in MongoDB (deleted_count=0).")

            mysql_delete_result = await MySQLSongService.delete_playlist(playlist_id)
            if not mysql_delete_result:
                return {"error": "Error deleting playlist from MySQL."}

            return {"message": "Playlist deleted successfully from both databases."}

        except Exception as e:
            logging.error(f"delete_playlist error: {e}")
            return {"error": str(e)}
