from app.services import get_all_songs,insert_one_song
from fastapi import HTTPException

def get_songs_request():
    songs = get_all_songs()
    if not songs:
        raise HTTPException(status_code=404, detail="No songs found")
    return songs

def create_one_song_request():
    insert_result = insert_one_song()
    return insert_result






