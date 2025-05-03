from typing import Dict, List
from fastapi import HTTPException
from app.services import get_top_tracks_lastfm,get_titles_only,top_12_more_listen



async def get_lastfm_top_tracks(limit: int = 12):
    try:
        return await get_top_tracks_lastfm(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def procesar_top_12_songs(limit: int = 12):
    try:
        tracks = await get_top_tracks_lastfm(limit)
        # Convertimos el formato esperado por top_12_more_listen
        songs = [{"title": track["name"]} for track in tracks]
        await top_12_more_listen(songs)
        return {"message": f"{len(songs)} canciones procesadas correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar canciones: {str(e)}")