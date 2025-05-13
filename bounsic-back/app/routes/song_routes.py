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

@router.get("/search/{title}")
async def get_song_by_title(title: str):
    return await Song_controller.search_songs_controller(title)

@router.get("/genre/{genre}")
async def get_songs_by_genre(genre: str):
    return await Song_controller.get_songs_by_genre_controller(genre)

@router.get("/img")
async def get_song_image(blob_name: str):
    return await Song_controller.get_song_image_controller(blob_name)

@router.post("/insert")
async def insert_bs(request: Request):
    data = await request.json()
    artist= data.get("artist")
    title= data.get("title")
    print(artist , title)
    return await Song_controller.insert_bs_controller(artist, title)

@router.put("/insert/{track_name}")
async def create_song(track_name: str):
    return await Song_controller.insert_song_controller(track_name)

@router.put("/update/lyrics")
async def update_lyrics():
    return await Song_controller.update_lyrics_controller()

@router.put("/update/lyrics_analysis")
async def update_lyrics_analysis():
    return await Song_controller.update_Bert_analysis()

@router.get("/diagnose/songs-db")
async def diagnose_songs_db():
    return await Song_controller.diagnose_songs_db()

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

@router.get("/top12")
async def get_top_12_songs():
    return await Song_controller.get_top_12_songs_controller()

@router.post("/player-queue")
async def get_player_queue(request : Request):
    data = await request.json()
    seed_song_id = data.get("song_id")
    return await Song_controller.player_queue(seed_song_id)

@router.post("/get/lyrics-related")
async def get_lyrics_related(request : Request):
    data = await request.json()
    seed_song_id = data.get("song_name")
    return await Song_controller.lyrics_related(seed_song_id)