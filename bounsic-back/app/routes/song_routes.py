from fastapi import APIRouter, Request
from app.controllers import (
    get_song_by_artist_controller,
    get_song_by_title_controller,
    get_songs_by_genre_controller,
    get_song_by_id_controller,
    get_song_image_controller,
    insert_bs_controller,
    insert_song_controller,
    safe_choice_recomendation,
    get_most_listened
)

router = APIRouter()

@router.get("/id/{id}")
async def get_song_by_id(id: str):
    return await get_song_by_id_controller(id)

@router.get("/artist/{artist}")
async def get_song_by_artist(artist: str):
    return await get_song_by_artist_controller(artist)

@router.get("/title/{title}")
async def get_song_by_title(title: str):
    return await get_song_by_title_controller(title)

@router.get("/genre/{genre}")
async def get_songs_by_genre(genre: str):
    return await get_songs_by_genre_controller(genre)

@router.get("/img")
async def get_song_image(blob_name: str):
    return await get_song_image_controller(blob_name)

@router.post("/insert")
async def insert_bs():
    return await insert_bs_controller("")

@router.put("/insert/{track_name}")
async def create_song(track_name: str):
    return await insert_song_controller(track_name)

@router.post("/safeChoice")
async def get_safe_choice(request: Request):
    data = await request.json()
    user_email = data.get("email")
    return await safe_choice_recomendation(user_email)

@router.post("/lastMonth")
async def get_most_listenes(request : Request):
    data = await request.json()
    user_email = data.get("email")
    return await get_most_listened(user_email)
