# app/services/lastfm_service.py
import httpx
from typing import List
from app.provider import API_KEY, BASE_URL
from app.services import Song_service

class LastfmService:
    @staticmethod
    async def get_top_tracks_lastfm(limit: int = 12) -> List[dict]:
        params = {
            "method": "chart.gettoptracks",
            "api_key": API_KEY,
            "format": "json",
            "limit": limit
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            tracks = data.get("tracks", {}).get("track", [])

            resultado = []
            for track in tracks:
                resultado.append({
                    "name": track["name"],
                    "artist": track["artist"]["name"],
                    "listeners": track["listeners"],
                    "url": track["url"],
                    "image": track["image"][-1]["#text"] if track["image"] else None,
                })

            return resultado
        
    @staticmethod
    async def get_titles_only(limit: int = 12) -> List[str]:
        tracks = await LastfmService.get_top_tracks_lastfm(limit)
        return [track["name"] for track in tracks]

    @staticmethod
    async def top_12_more_listen(songs):
        for song in songs:
            existing_song = Song_service.getSongByTitle(song['title'])  
            
            if existing_song.get("message") == "Song not found":
                song_data = Song_service.generar_song_data(song['title'])
                
                if song_data:
                    Song_service.insert_song(song['title'])  
                    print(f"Canción '{song['title']}' agregada correctamente.")
                else:
                    print(f"No se pudo obtener la información de la canción '{song['title']}'.")
            else:
                print(f"La canción '{song['title']}' ya existe en la base de datos.")