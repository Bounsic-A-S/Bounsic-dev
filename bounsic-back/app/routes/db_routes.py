from fastapi import APIRouter, Request, HTTPException, Query  # Se agregó HTTPException
from fastapi.responses import JSONResponse
from app.services import get_songs, insert_songs

router = APIRouter()

@router.get("/getSongsBd")
async def get_songs_bd():
    try:
        print('holi')
        songs = get_songs()
        return JSONResponse(content=songs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/insert/songs")
async def insert_songs_bd(request: Request):
    try:
        data = await request.json()
        response = insert_songs(data)
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))