from fastapi import APIRouter, HTTPException,Request, Query
from fastapi.responses import JSONResponse
from app.controllers import (
    get_song_by_artist_controller,
    get_song_by_title_controller,
    get_songs_by_genre_controller,
    get_song_image_controller,
    insert_bs_controller,insert_song_controller
)

router = APIRouter()

@router.get("/artist/{artist}")
async def get_song_by_artist(artist: str):
    print(f"Buscando canciones de: {artist}")
    res = await get_song_by_artist_controller(artist)
    if "error" in res:
        raise JSONResponse(status_code=404, detail="No se encontraron canciones para este artista")
    return JSONResponse(status_code=200,content=res)



@router.get("/title/{title}")
async def get_song_by_title(title: str):
    res = await get_song_by_title_controller(title)
    if "error" in res:
        raise JSONResponse(status_code=404, detail="No se encontró ninguna canción con este título")
    return JSONResponse(status_code=200,content=res)


@router.get("/genre/{genre}")
async def get_songs_by_genre(genre: str):
    res = await get_songs_by_genre_controller(genre)
    if "error" in res:
        raise JSONResponse(status_code=404, detail="No se encontraron canciones para este género")
    return JSONResponse(status_code=200,content=res)


@router.get("/img")
async def get_song_image(blob_name: str = Query(..., description="Nombre del blob en Azure")):
    print(blob_name)
    res = await get_song_image_controller(blob_name)
    if "error" in res:
        raise JSONResponse(status_code=404, detail="Imagen no encontrada")
    return JSONResponse(status_code=200,content=res)


@router.post("/insert/songs")
async def insert_bs():
    res = await insert_bs_controller("")
    if "error" in res:
        raise JSONResponse(status_code=500, detail="Error al insertar canciones")
    return JSONResponse(status_code=200,message= "Canciones procesadas",data=res)

@router.put("/insert/{track_name}")
async def create_song(track_name: str):
    result = await insert_song_controller(track_name)  # 👈 await aquí porque la función es async

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
    
