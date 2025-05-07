from typing import Optional
from fastapi import HTTPException, Request
from app.services import getPlaylistById,getAllPlaylists,create_user_playlist,add_song_to_playlist

def get_playlist_by_id_controller(playlist_id: str):
    result = getPlaylistById(playlist_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    elif "message" in result and result["message"] == "Playlist not found":
        raise HTTPException(status_code=404, detail=result)
    
    return result

async def get_all_playlists_controller(request: Request):
    return getAllPlaylists()



async def create_user_playlist_controller(user_id: int, playlist_name: str, img_url: Optional[str] = None):
    if not playlist_name:
        raise HTTPException(status_code=400, detail="El nombre de la playlist es obligatorio")

    inserted_id = await create_user_playlist(user_id, playlist_name, img_url)

    if not inserted_id:
        raise HTTPException(status_code=500, detail="Error al crear la playlist")

    return {
        "message": "Playlist creada con éxito",
        "playlist_id": str(inserted_id)
    }

async def add_song_to_playlist_controller(playlist_id: str, user_id: int, song_id: str):
        result = await add_song_to_playlist(playlist_id, user_id, song_id)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result