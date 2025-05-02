from fastapi import APIRouter, Query
from app.controllers.lastfm_controller import get_lastfm_top_tracks

router = APIRouter()

@router.get("/top-tracks")
async def obtener_top_tracks(limit: int = Query(12, ge=1, le=50)):
    return await get_lastfm_top_tracks(limit)
