from typing import Optional
from fastapi import APIRouter, Body, HTTPException
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.controllers import Playlist_controller

router = APIRouter()


@router.get("/all")
async def get_all_playlists():
    return await Playlist_controller.get_all_playlists_controller()

@router.get("/{playlist_id}")
async def get_playlist_by_id(playlist_id: str):
    try:
        if not ObjectId.is_valid(playlist_id):
            raise HTTPException(status_code=400, detail="ID de playlist inválido.")

        playlist = await Playlist_controller.get_playlist_by_id_controller(playlist_id)

        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist no encontrada.")

        return playlist

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error al acceder a la base de datos: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
@router.post("/create")
async def create_playlist(
    user_id: int = Body(..., embed=True),
    playlist_name: str = Body(..., embed=True),  
    img_url: Optional[str] = Body(None, embed=True)  
):
    return await Playlist_controller.create_user_playlist_controller(user_id, playlist_name, img_url)

    
@router.post("/add-song")
async def add_song_to_playlist(
    playlist_id: str = Body(..., description="ID de la playlist"),
    song_id: str = Body(..., description="ID de la canción")
):
    return await Playlist_controller.add_song_to_playlist_controller(playlist_id, song_id)

@router.delete("/delete")
async def delete_playlist(
     playlist_id: int = Body(..., embed=True),
):
    return await Playlist_controller.delete_playlist_controller(playlist_id)