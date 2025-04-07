from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.controllers.artist_controller import (
    get_songs_by_artist_controller,
    get_artist_desc_controller
)

router = APIRouter()

@router.get("/{artist}/songs")
async def get_songs_by_artist(artist: str):
    res = await get_songs_by_artist_controller(artist)
    if "error" in res:
        raise JSONResponse(status_code=404, detail="No se encontraron canciones para este artista")
    return JSONResponse(status_code=200, content=res)


@router.get("/{artist}/description")
async def get_artist_description(artist: str):
    res = await get_artist_desc_controller(artist)
    if "error" in res:
        raise JSONResponse(status_code=404, detail="No se encontró la descripción del artista")
    return JSONResponse(status_code=200, content=res)
