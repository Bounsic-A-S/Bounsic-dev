from fastapi import APIRouter, Request
from app.controllers import Song_controller
from app.provider import Songs_db_provider

router = APIRouter()
songs_provider = Songs_db_provider()

@router.get("/id/{id}")
async def get_song_by_id(id: str):
    return await Song_controller.get_song_by_id_controller(id)

@router.get("/songs")
async def get_songs():
    return await Song_controller.get_allSongs()

@router.get("/artist/{artist}")
async def get_song_by_artist(artist: str):
    return await Song_controller.get_song_by_artist_controller(artist)

@router.get("/title/{title}")
async def get_song_by_title(title: str):
    return await Song_controller.get_song_by_title_controller(title)

@router.get("/genre/{genre}")
async def get_songs_by_genre(genre: str):
    return await Song_controller.get_songs_by_genre_controller(genre)

@router.get("/img")
async def get_song_image(blob_name: str):
    return await Song_controller.get_song_image_controller(blob_name)

@router.post("/insert")
async def insert_bs():
    return await Song_controller.insert_bs_controller("")

@router.put("/insert/{track_name}")
async def create_song(track_name: str):
    return await Song_controller.insert_song_controller(track_name)

@router.put("/update/lyrics")
async def update_lyrics():
    return await Song_controller.update_lyrics_controller()

@router.post("/safeChoice")
async def get_safe_choice(request: Request):
    data = await request.json()
    user_email = data.get("email")
    return await Song_controller.safe_choice_recomendation(user_email)
    
@router.post("/getRelated")
async def get_related_songs(request: Request):
    data = await request.json()
    user_email = data["email"]
    return await Song_controller.feed_related_recomendations(user_email)

@router.post("/lastMonth")
async def get_most_listenes(request : Request):
    data = await request.json()
    user_email = data.get("email")
    return await Song_controller.get_most_listened(user_email)