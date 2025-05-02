import httpx
from typing import List

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
