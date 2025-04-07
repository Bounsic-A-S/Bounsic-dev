from pymongo.errors import PyMongoError
from app.provider import db
import re

collection = db["artists"]

def normalize_string(s: str) -> str:
    """Quita espacios y convierte a minúsculas para normalizar un string."""
    return re.sub(r"\s+", "", s).lower()

def getSongsByArtist(artist_name: str):
    try:
        normalized_artist = normalize_string(artist_name)
        artist = collection.find_one({
            "$expr": {
                "$eq": [
                    {"$toLower": {"$replaceAll": {"input": "$artist_name", "find": " ", "replacement": ""}}},
                    normalized_artist
                ]
            }
        })

        if artist and "songs" in artist:
            for song in artist["songs"]:
                if isinstance(song, dict) and "_id" in song and "$oid" in song["_id"]:
                    song["_id"] = song["_id"]["$oid"]
            return artist["songs"]

        return {"message": "No songs found for this artist"}

    except PyMongoError as e:
        return {"error": "Database error", "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}

def getDesc(artist_name: str):
    try:
        normalized_artist = normalize_string(artist_name)
        artist = collection.find_one({
            "$expr": {
                "$eq": [
                    {"$toLower": {"$replaceAll": {"input": "$artist_name", "find": " ", "replacement": ""}}},
                    normalized_artist
                ]
            }
        })

        if artist and "desc" in artist:
            return {"desc": artist["desc"]}

        return {"message": "Description not found for this artist"}

    except PyMongoError as e:
        return {"error": "Database error", "details": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}
