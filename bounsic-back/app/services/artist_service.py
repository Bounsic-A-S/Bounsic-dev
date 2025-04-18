from pymongo.errors import PyMongoError
from app.provider import db
import re
from bson import ObjectId

collection = db["artists"]

def normalize_string(s: str) -> str:
    """Removes spaces and converts to lowercase to normalize a string."""
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
            song_ids_str = artist["songs"]
            if isinstance(song_ids_str, str):
                import json
                song_ids_str = json.loads(song_ids_str)

            song_ids = [ObjectId(song_id) for song_id in song_ids_str]

            songs_collection = db["songs"]
            songs_cursor = songs_collection.find({"_id": {"$in": song_ids}}, {"title": 1})

            song_titles = [song["title"] for song in songs_cursor]

            return song_titles if song_titles else {"message": "No song titles found"}

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
