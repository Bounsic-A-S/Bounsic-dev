from typing import Optional
from fastapi import HTTPException
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
    async def get_all_playlists_controller():
        return Playlist_service.getAllPlaylists()

    @staticmethod
    async def create_user_playlist_controller(user_id: int, playlist_name: str, img_url: Optional[str] = None):
        if not playlist_name:
            raise HTTPException(status_code=400, detail="El nombre de la playlist es obligatorio")

        inserted_id = await Playlist_service.create_user_playlist(user_id, playlist_name, img_url)

        if not inserted_id:
            raise HTTPException(status_code=500, detail="Error al crear la playlist")

        return {
            "message": "Playlist creada con éxito",
            "playlist_id": str(inserted_id)
        }
    @staticmethod
    async def add_song_to_playlist_controller(playlist_id: str, song_id: str):
            result = await Playlist_service.add_song_to_playlist(playlist_id, song_id)

            if "error" in result:
                raise HTTPException(status_code=400, detail=result["error"])

            return result
    @staticmethod
    async def delete_playlist_controller(playlist_id: int ):
        result = await Playlist_service.delete_playlist(playlist_id)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return result