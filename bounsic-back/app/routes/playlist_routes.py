from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pymongo.errors import PyMongoError
from app.controllers import get_playlist_by_id_controller

router = APIRouter()

@router.get("/{playlist_id}")
def get_playlist_by_id(playlist_id: str):
    try:
        if not ObjectId.is_valid(playlist_id):
            raise HTTPException(status_code=400, detail="ID de playlist inválido.")

        playlist = get_playlist_by_id_controller(playlist_id)

        if not playlist:
            raise HTTPException(status_code=404, detail="Playlist no encontrada.")

        return playlist

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Error al acceder a la base de datos: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
