from fastapi import HTTPException
from app.services import get_top_tracks_lastfm

async def get_lastfm_top_tracks(limit: int = 12):
    try:
        return await get_top_tracks_lastfm(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
