from fastapi import APIRouter
from app.controllers import (
    get_song_by_artist_controller,
    get_song_by_title_controller,
    get_songs_by_genre_controller,
    get_song_image_controller,
    insert_song_controller
)

router = APIRouter()

@router.get("/artist/{artist}")
async def get_song_by_artist(artist: str):
    return await get_song_by_artist_controller(artist)

@router.get("/title/{title}")
async def get_song_by_title(title: str):
    return await get_song_by_title_controller(title)

@router.get("/genre/{genre}")
async def get_songs_by_genre(genre: str):
    return await get_songs_by_genre_controller(genre)

@router.get("/img/{blob_name}")
async def get_song_image(blob_name: str):
    return await get_song_image_controller(blob_name)

@router.post("/insert/{track_name}")
async def insert_song(track_name: str):
    return await insert_song_controller(track_name)
