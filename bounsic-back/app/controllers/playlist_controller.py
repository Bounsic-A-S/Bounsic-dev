from fastapi import HTTPException, Request
from app.services import getPlaylistById,getAllPlaylists,create_user_playlist

def get_playlist_by_id_controller(playlist_id: str):
    result = getPlaylistById(playlist_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    elif "message" in result and result["message"] == "Playlist not found":
        raise HTTPException(status_code=404, detail=result)
    
    return result

async def get_all_playlists_controller(request: Request):
    return getAllPlaylists()


def create_user_playlist_controller(user_id: int, is_public: bool, img_url: str):
    inserted_id = create_user_playlist(user_id, is_public, img_url)

    if not inserted_id:
        raise HTTPException(status_code=500, detail="Error al crear la playlist")

    return {
        "message": "Playlist creada con éxito",
        "playlist_id": str(inserted_id)
    }