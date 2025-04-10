from bson import ObjectId
from app.provider import db
from pymongo.errors import PyMongoError



def getPlaylistById(playlist_id: str):
    try:
        playlists_collection = db["playlists"]
        songs_collection = db["songs"]

        playlist_obj_id = ObjectId(playlist_id)

        playlist = playlists_collection.find_one({"_id": playlist_obj_id})
        if not playlist:
            return {"message": "Playlist not found"}

        song_ids = [song["song_id"] for song in playlist.get("songs", [])]

        songs = list(songs_collection.find({"_id": {"$in": song_ids}}))

        for song in songs:
            song["_id"] = str(song["_id"])

        return {
            "playlist_id": str(playlist["_id"]),
            "songs": songs,
            "isPublic": playlist.get("isPublic", False),
            "img_url": playlist.get("img_url", ""),
            "updated_at": playlist.get("updated_at")
        }

    except PyMongoError as e:
        return {"error": "Database error", "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}

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