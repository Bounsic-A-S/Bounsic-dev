from fastapi import HTTPException, Request
from app.services import Playlist_service

class Playlist_controller:
    @staticmethod
    async def get_playlist_by_id_controller(playlist_id: str):
        result = Playlist_service.getPlaylistById(playlist_id)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result)
        elif "message" in result and result["message"] == "Playlist not found":
            raise HTTPException(status_code=404, detail=result)
        
        return result
    @staticmethod
    async def get_all_playlists_controller(request: Request):
        return Playlist_service.getAllPlaylists()