from app.services import get_alikes, getSongByTitle, getSongByArtist, get_song_by_id
from .mysql_service import MySQLSongService
from .db_service import get_all_songs, get_random_songs, get_random_song_by_album, get_relative_genres, get_all_data_songs
from app.provider import db
import random

async def get_feed_recomendations(user_id: str):
    size = 16 # size of recomendation (pair number)
    liked_songs = await MySQLSongService.get_random_likes(user_id, size//2)
    latest_songs = await MySQLSongService.get_most_played_songs(user_id, size//2) # get latest songs reproductions
    database_songs = get_all_data_songs()
    songs = [] # songs to evaluate
    res_songs = [] # final recomendations

    for i in range(size//2):
        if (i < len(liked_songs)):
            songs.append(get_song_by_id(liked_songs[i]["song_mongo_id"]))
        if (i < len(latest_songs)):
            songs.append(get_song_by_id(latest_songs[i]["song_mongo_id"]))

    artist = 0
    finger = 0
    genre = 0
    for i in range(len(songs)):
        s = songs[i]
        print("Recomendation to: ",s["title"])
        if (i % 3 == 0): # Artist bases
            recom = artist_recomendation(s)
            res_songs.append(recom)
            print("   Artist_recom")
            print("  - ", recom["title"])

        elif (i & 2 == 0): # Fingerprint based
            alikes = get_alikes(target_song=s, database_songs=database_songs, size=1)
            if not alikes:
                print(".fill in (Alikes)")
                alikes = get_random_songs(1)
            alikes = alikes[0]
            res_songs.append(alikes)
            print("   Fingerprint_recom")
            print("  - ", alikes["title"])
            
        else: # Genre based
            recom = await genre_recomendation(s)
            res_songs.append(recom)
            print("   Genre_recom")
            print("  - ", recom["title"])
            

    if (len(songs) < size):
        res_songs += get_random_songs(size - len(songs))
    
    # Size recomendation = 16 :
    # ArtistRecom:  6
    # FingerRecom:  5
    # GenreRecom:  5

    return res_songs

async def genre_recomendation(input_song):
    temp = []
    song = None

    temp = await get_songs_by_genre(input_song)
    if temp:
        song = random.choice(temp)
    else:
        print(".fill in (Genre)")
        song = get_random_songs(1)[0]
    return song
    
def artist_recomendation(input_song):
    song_id = get_random_song_by_album(input_song["album"])
    if song_id: song = get_song_by_id(song_id["song_id"])
    else: song = None
    # O Tomar cancion aleatoria del mismo artista
    # O Tomar cancion aleatoria
    if (song is None):
        print(".fill in (Artist)")
        song = (get_random_songs(1)[0])        

    return song

async def get_songs_by_genre(input_song):
    songs_collection = db["songs"]
    songs = []
    target_genres = [genre_obj["genre"] for genre_obj in input_song.get("genres", [])]
    if (len(target_genres) > 1):
        songs = list(songs_collection.find({
            "_id": { "$ne": input_song["_id"] },
            "genres.genre": { "$in": target_genres }
        }))

    return songs
