from fastapi import HTTPException, Request
from app.services import getPlaylistById,getAllPlaylists

def get_playlist_by_id_controller(playlist_id: str):
    result = getPlaylistById(playlist_id)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result)
    elif "message" in result and result["message"] == "Playlist not found":
        raise HTTPException(status_code=404, detail=result)
    
    return result

async def get_all_playlists_controller(request: Request):
    return getAllPlaylists()