import httpx
from typing import List
from app.services import getSongByTitle,generar_song_data,insert_song

API_KEY = "022ae4a2d6f3acc9d88dde7e24ffb2d1"
BASE_URL = "http://ws.audioscrobbler.com/2.0/"

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

async def get_titles_only(limit: int = 12) -> List[str]:
    tracks = await get_top_tracks_lastfm(limit)
    return [track["name"] for track in tracks]


async def top_12_more_listen(songs):
    for song in songs:
        existing_song = getSongByTitle(song['title'])  
        
        if existing_song.get("message") == "Song not found":
            song_data = generar_song_data(song['title'])
            
            if song_data:
                insert_song(song['title'])  
                print(f"Canción '{song['title']}' agregada correctamente.")
            else:
                print(f"No se pudo obtener la información de la canción '{song['title']}'.")
        else:
            print(f"La canción '{song['title']}' ya existe en la base de datos.")


