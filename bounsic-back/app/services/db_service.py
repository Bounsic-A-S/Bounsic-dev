from app.provider import db

def get_all_songs():
    songs_collection = db["songs"]
    print(db.list_collection_names())
    songs = list(songs_collection.find({}, {"_id": 0}))
    return songs

def get_all_songs_mongo():
    songs_collection = db["songs"]
    songs = list(songs_collection.find())  # Esto incluye _id automáticamente
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