from itertools import chain
from app.services import getDesc,getSongsByArtist,MySQLSongService,get_song_by_id,get_artists_by_genre


async def get_songs_by_artist_controller(artist: str):
    if not artist:
        return {"error": "Artist not provided"}
    
    print(f"Buscando canciones del artista: {artist}")
    res = getSongsByArtist(artist)
    
    if not res:
        return {"error": "No songs found for this artist"}
    
    return {"data": res}


async def get_artist_desc_controller(artist: str):
    if not artist:
        return {"error": "Artist not provided"}
    
    print(f"Obteniendo descripción del artista: {artist}")
    res = getDesc(artist)

    if not res or isinstance(res, dict) and res.get("message"):
        return {"error": "Artist not found"}
    
    return {"data": res}

async def get_artist_user_prefences_controller(email: str):
    if not email:
        return {"error": "Email not provided"}
    
    # get user
    user = await MySQLSongService.get_user_by_email(email)
    # get songs listened
    likes = await MySQLSongService.get_likes_by_user(user[0]["id_user"])
    songs_liked = []
    for like in likes:
        song = get_song_by_id(like["song_mongo_id"])
        if song:
            songs_liked.append(song)
    
    # get genres
    genres = [genre for song in songs_liked if song.get("genres") for genre in song["genres"]]
    filter_genres = list({genre["genre"] for genre in genres})
    # get artist by genre
    artists = []
    for genre in filter_genres:
        artist = get_artists_by_genre(genre)
        if not artist:
            return {"error": "Artists not found"}
        
        artists.append(artist)

    return list(chain.from_iterable(artists))