from app.provider import db
import random

def get_all_songs():
    try:
        songs_collection = db["songs"]
        
        # Excluir los campos 'fingerprint' y 'genres'
        songs_cursor = songs_collection.find({}, {"fingerprint": 0, "genres": 0})
        songs = list(songs_cursor)

        for song in songs:
            song["_id"] = str(song["_id"])

        return songs
    except Exception as e:
        print(f"Error al obtener canciones: {e}")
        return []

def get_all_data_songs():
    songs_collection = db["songs"]
    songs = list(songs_collection.find({}))
    return songs

def insert_one_song(data):
    try:
        mock_data = {
            "artist": data.get("artist", "Unknown Artist"),
            "img_url": data.get("img_url", "https://example.com/default.jpg"),
            "mp3_url": data.get("mp3_url", "https://example.com/default.mp3"),
            "release_year": data.get("release_year", 2100),
            "title": data.get("title", "Unknown Title"),
        }
        result = db.songs.insert_one(mock_data)
        if result.inserted_id:
            return {"message": "Song added successfully", "id": str(result.inserted_id)}
        else:
            return {"error": "Insertion failed"}
        
    except Exception as e:
        return {"error": "Database error", "details": str(e)}
    
def get_random_songs(size: int):
    songs_collection = db["songs"]
    songs = list(songs_collection.aggregate([
        { "$sample": { "size": size } }
    ]))
    return songs

def get_random_song_by_album(album_name: str):
    albums_collection = db["albums"]
    
    album = albums_collection.find_one({ "name": album_name })
    
    if album and len(album) > 4: # Validar que es un album y no un sencillo
        return random.choice(album["songs"])
    else:
        return None
    
def get_relative_genres(keyword: str):
    songs_collection = db["songs"]

    songs = list(songs_collection.find({
        "genres.genre": { "$regex": keyword, "$options": "i" }
    }))

    return songs
