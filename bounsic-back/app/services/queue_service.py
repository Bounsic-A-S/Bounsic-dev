import random
from typing import Set
from app.services import get_alikes, Song_service, Feed_service
from app.provider import Songs_db_provider
import time
from bson import ObjectId

class Queue_service:

    @staticmethod    
    async def get_queue(seed_song, size=25):
        inserted_ids = set()
        inserted_ids.add(seed_song["_id"])
        res_songs = [] # final recomendations
        next_seed = seed_song
        while size > 0:
            recoms, size = await Queue_service.generate_recomemdations(next_seed, size, inserted_ids)
            next_seed = recoms[-1]
            random.shuffle(recoms)
            res_songs += recoms

        print("Recomendaciones: ", len(res_songs))
        return res_songs
    
    @staticmethod
    async def generate_recomemdations(seed_song, size, inserted_ids: Set[ObjectId]):
        songs_provider = Songs_db_provider()
        alikes = get_alikes(target_song=seed_song, database_songs=songs_provider.get_all(), size=2, inserted_ids=inserted_ids)
        genrecom = await Feed_service.genre_recomendation(seed_song, 4, inserted_ids, fill=False)
        artistrecom = Feed_service.artist_recomendation(seed_song, 2, inserted_ids)
        
        recoms = alikes + genrecom + artistrecom
        size -= len(recoms)

        return recoms, size