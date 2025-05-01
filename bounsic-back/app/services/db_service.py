from app.provider import db

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