from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.services import (get_album_images, get_artist_and_genre_by_track,get_top_tracks_global)

async def get_album_cover_controller(album_name: str, artist_name: str = None):
    try:
        data = get_album_images(album_name, artist_name)
        if not data or "images" not in data or not data["images"]:
            return JSONResponse(status_code=404, content={"error": "No se encontraron imágenes para este álbum"})
        
        return JSONResponse(status_code=200, content=data)

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

async def get_track_info_controller(track_name: str):
    try:
        result = get_artist_and_genre_by_track(track_name)

        if not result:
            raise HTTPException(status_code=404, detail="Canción no encontrada en Spotify")
        
        return JSONResponse(status_code=200, content=result)

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
async def get_top_tracks_controller(limit):  
    top_tracks = get_top_tracks_global(limit=limit)

    if not top_tracks:
        return {"message": "No se encontraron los tracks más escuchados globalmente."}

    return {"top_tracks": top_tracks}