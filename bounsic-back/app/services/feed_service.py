from typing import Set
from app.services import get_alikes, Song_service, Db_service
from app.services import MySQLSongService
from app.provider import db
from app.provider import Songs_db_provider
import random
import time
from bson import ObjectId

class Feed_service:

    @staticmethod
    async def get_feed_recomendations(user_id: str):
        binicio = time.time()
        songs_provider = Songs_db_provider()
        size = 16 # size of recomendation
        liked_songs = []
        lastest_songs = []
        if (user_id):
            liked_songs = await MySQLSongService.get_random_likes(user_id, 2)
            lastest_songs = await MySQLSongService.get_most_played_songs(user_id, 2)

        database_songs = songs_provider.get_all()
        songs = [] # songs to evaluate
        res_songs = [] # final recomendations

        linicio = time.time()
        for s in liked_songs:
            songs.append(Song_service.get_song_by_id(s["song_mongo_id"]))
        for s in lastest_songs:
            songs.append(Song_service.get_song_by_id(s["song_mongo_id"]))
        lfin = time.time()

        bfin = time.time()
        print(f"Tiempo (Preparación): {bfin - binicio:.6f} segundos\n")

        inserted_ids = set()
        alikes_size = 4
        genres_size = 3
        artists_size = 2
        for i in range(len(songs)):
            s = songs[i]
            if (i % 2 == 0): # Fingerprint based
                alikes = get_alikes(target_song=s, database_songs=database_songs, size=alikes_size, inserted_ids=inserted_ids)
                if (len(alikes) < alikes_size):
                    alikes += random.sample(songs_provider.get_all(), alikes_size - len(alikes))
                res_songs += alikes
                
            else: # Genre based
                recom = await Feed_service.genre_recomendation(s, genres_size, inserted_ids)
                res_songs += recom
           
        if liked_songs:
            inicio = time.time()
            s = songs[0]
            recom = Feed_service.artist_recomendation(s, artists_size, inserted_ids)
            res_songs += recom
            fin = time.time()
            print(f"Tiempo (Artist): {fin - inicio:.6f} segundos")
            print("aritst: ", len(recom))
        """ 
        Fill recomendations in case
        """
        if (len(res_songs) < size):
            print(f"Fill recomendation({size - len(res_songs)}) to user: '{user_id}'")
            res_songs += random.sample(songs_provider.get_all(), size - len(res_songs))
        
        return res_songs

    @staticmethod
    async def genre_recomendation(input_song, size, inserted_ids: Set[ObjectId], fill=True):
        songs_provider = Songs_db_provider()
        songs = []
        if (len(input_song["genres"]) > 0):
            songs = await Feed_service.get_songs_by_genre(input_song, inserted_ids, songs_provider.get_all())
        
        if (len(songs) > size):
            songs = random.sample(songs, size)
        elif fill:
            songs += random.sample(songs_provider.get_all(), size - len(songs))
        return songs
        
    @staticmethod
    def artist_recomendation(input_song, size, inserted_ids: Set[ObjectId]):
        songs = []

        # input_song = Song_service.get_song_by_id(input_song["song_mongo_id"])
        
        song_id, album_id = Db_service.get_random_song_by_album(input_song["album"])
        if song_id: 
            songs.append(Song_service.get_song_by_id(song_id["song_id"]))
            

        s = Feed_service.get_random_artist_song(input_song["artist"], album_id, size-1)
        if (s): songs.append(s)

        return songs

    @staticmethod
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

    @staticmethod
    async def get_songs_by_genre(input_song, inserted_ids: Set[ObjectId], songs_data):
        input_genres = set(genre["genre"] for genre in input_song.get("genres", []))
        songs = []
        
        for s in songs_data:
            if (s["_id"] in inserted_ids):
                continue

            s_genres = set(genre["genre"] for genre in s.get("genres", []))

            if (input_genres & s_genres):
                inserted_ids.add(s["_id"])
                songs.append(s)

        return songs
