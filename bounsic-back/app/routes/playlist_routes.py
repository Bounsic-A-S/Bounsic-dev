from fastapi import APIRouter, HTTPException, Request
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.controllers import Playlist_controller

router = APIRouter()


@router.get("/all")
async def get_all_playlists(request: Request):
    return await Playlist_controller.get_all_playlists_controller(request)

@router.get("/{playlist_id}")
def get_playlist_by_id(playlist_id: str):
    try:
        if not ObjectId.is_valid(playlist_id):
            raise HTTPException(status_code=400, detail="ID de playlist inválido.")

        playlist = Playlist_controller.get_playlist_by_id_controller(playlist_id)

        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist no encontrada.")

        return playlist

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error al acceder a la base de datos: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    

