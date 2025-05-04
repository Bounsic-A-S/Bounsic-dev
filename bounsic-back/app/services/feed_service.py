from app.services import get_alikes, Song_service, Db_service
from app.services import MySQLSongService
from app.provider import db
import random
import time

async def get_feed_recomendations(user_id: str):
    ginicio = time.time()
    binicio = time.time()

    size = 16 # size of recomendation (pair number)
    ainicio = time.time()
    liked_songs = await MySQLSongService.get_random_likes(user_id, 2)
    latest_songs = await MySQLSongService.get_most_played_songs(user_id, 2) # get latest songs reproductions
    afin = time.time()
    print(f"get likes_&_lastest: {afin - ainicio:.6f} segundos")

    linicio = time.time()
    database_songs = Db_service.get_all_data_songs()
    lfin = time.time()
    print(f"get all songs: {lfin - linicio:.6f} segundos\n")
    songs = [] # songs to evaluate
    res_songs = [] # final recomendations

    for i in range(4):
        if (i < len(liked_songs)):
            songs.append(Song_service.get_song_by_id(liked_songs[i]["song_mongo_id"]))
        if (i < len(latest_songs)):
            songs.append(Song_service.get_song_by_id(latest_songs[i]["song_mongo_id"]))

    artist = 0
    finger = 0
    genre = 0

    bfin = time.time()
    print(f"Tiempo (Preparación): {bfin - binicio:.6f} segundos\n")
    for i in range(len(songs)):
        s = songs[i]
        if (i % 2 == 0): # Fingerprint based
            inicio = time.time()
            alikes = get_alikes(target_song=s, database_songs=database_songs, size=4)
            if (len(alikes) < 4):
                print(".fill in (Alikes)")
                alikes += Song_service.get_random_songs(4 - len(alikes))
            
            res_songs += alikes
            fin = time.time()
            print(f"Tiempo (Fingerprint): {fin - inicio:.6f} segundos")
            
        else: # Genre based
            inicio = time.time()
            recom = await genre_recomendation(s, 3)
            res_songs += recom
            
            fin = time.time()
            print(f"Tiempo (Genre): {fin - inicio:.6f} segundos")
        
    if liked_songs:
        inicio = time.time()
        recom = artist_recomendation(liked_songs[0], 2)
        res_songs += recom
        
        fin = time.time()
        print(f"Tiempo (Artist): {fin - inicio:.6f} segundos")
    
    if (len(res_songs) < size):
        res_songs += Db_service.get_random_songs(size - len(res_songs))
    
    # Size recomendation = 16 :
    # ArtistRecom:  5
    # FingerRecom:  5
    # GenreRecom:  6
    gfin = time.time()
    print(f"Tiempo (feed_service): {gfin - ginicio:.6f} segundos")

    print("Recomendaciones: ", len(res_songs))
    return res_songs

async def genre_recomendation(input_song, size):
    songs = []
    if (len(input_song["genres"]) < 0):
        return Song_service.get_random_songs(4)
    
    songs = await get_songs_by_genre(input_song)
    if (len(songs) > size):
        songs = random.sample(songs, size)
    else:
        print(".fill in (Genre)")
        songs += Song_service.get_random_songs(size - len(songs))
    return songs
    
def artist_recomendation(input_song, size):
    songs = []

    input_song = Song_service.get_song_by_id(input_song["song_mongo_id"])

    song_id, album_id = Db_service.get_random_song_by_album(input_song["album"])
    if song_id: 
        songs.append(Song_service.get_song_by_id(song_id["song_id"]))
        

    s = get_random_artist_song(input_song["artist"], album_id, 1)
    if (s): songs.append(s)


    # O Tomar cancion aleatoria del mismo artista
    # O Tomar cancion aleatoria
    
    # if (song is None):
    #     print(".fill in (Artist)")
    #     song = (get_random_songs(1)[0])

    return songs

def get_random_artist_song(artist: str, ex_album, size: int):
    """
    Get random song from a random album of an artist
    Args:
        artist: Artists name
        size: Number of songs
        ex_album: Album id
    """
    artists_collection = db["artists"]
    albums_col = db["albums"]
    songs_col = db["songs"]

    pipeline = [
        {"$match": {"artist_name": artist}},
        {"$unwind": "$albums"},
        {"$match": {"albums.album_id": {"$ne": ex_album}}},
        {"$sample": {"size": 1}},
        {"$project": {
            "_id": 0,
            "album_id": "$albums.album_id"
        }}
    ]
    
    album = list(artists_collection.aggregate(pipeline))

    if not album: return []

    pipeline = [
        {"$match": {"_id": album["album_id"]}},
        {"$unwind": "$songs"},
        {"$sample": {"size": 1}},
        {"$lookup": {
            "from": "songs",
            "localField": "songs.song_id",
            "foreignField": "_id",
            "as": "cancion"
        }},
        {"$unwind": "$cancion"},
        {"$project": {
            "_id": 0,
            "title": "$cancion.title",
            "artist": "$cancion.artist",
            "album": "$cancion.album",
            "mp3_url": "$cancion.mp3_url",
            "img_url": "$cancion.img_url",
            "lyrics": "$cancion.lyrics"
        }}
    ]
    songs = list(albums_col.aggregate(pipeline))
    return songs

async def get_songs_by_genre(input_song):
    songs_collection = db["songs"]
    songs = []
    target_genres = [genre_obj["genre"] for genre_obj in input_song.get("genres", [])]
    songs = list(songs_collection.find({
        "_id": { "$ne": input_song["_id"] },
        "genres.genre": { "$in": target_genres }
    }))
    return songs
