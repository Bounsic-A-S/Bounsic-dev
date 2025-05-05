from fastapi import APIRouter, Path, Query
from app.controllers import Spotify_controller

router = APIRouter()

@router.get("/{album_name}/{artist_name}")
async def get_album_cover(
    album_name: str = Path(..., description="Nombre del álbum"),
    artist_name: str = Path(..., description="Nombre del artista")
):
    return await Spotify_controller.get_album_cover_controller(album_name.strip(), artist_name.strip())

@router.get("/track-info")
async def track_info(
    track_name: str = Query(..., description="Nombre de la canción a buscar")
):
    return await Spotify_controller.get_track_info_controller(track_name.strip())
