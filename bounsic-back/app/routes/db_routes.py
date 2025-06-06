from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.controllers import Db_controller

router = APIRouter()

@router.get("/getSongsBd")
async def get_songs_bd():
    try:
        songs = await Db_controller.get_songs_request()
        return JSONResponse(content=songs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/insert/songs")
async def insert_songs_bd(request: Request):
    try:
        data = await request.json()
        response = await Db_controller.create_one_song_request(data)
        return JSONResponse(content=response, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))