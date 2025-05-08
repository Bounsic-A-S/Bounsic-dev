from app.services import Db_service
from fastapi import HTTPException

class Db_controller:
    @staticmethod
    async def get_songs_request():
        songs = Db_service.get_all_songs()
        if not songs:
            raise HTTPException(status_code=404, detail="No songs found")
        return songs
    
    @staticmethod
    async def create_one_song_request():
        insert_result = Db_service.insert_one_song()
        return insert_result






