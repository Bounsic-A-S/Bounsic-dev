from typing import Dict, List
from fastapi import APIRouter, Body, Query
from app.controllers import get_lastfm_top_tracks,procesar_top_12_songs

router = APIRouter()

@router.get("/top-tracks")
async def obtener_top_tracks(limit: int = Query(12, ge=1, le=50)):
    return await get_lastfm_top_tracks(limit)

@router.post("/procesar-songs")
async def procesar_canciones(limit: int = Query(12, ge=1, le=50)):
    return await procesar_top_12_songs(limit)