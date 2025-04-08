from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.controllers import get_album_cover_controller

router = APIRouter()

@router.get("/spotify/album-cover")
async def get_album_cover(
    album_name: str = Query(..., description="Nombre del álbum"),
    artist_name: str = Query(None, description="Nombre del artista (opcional)")
):
    print(f"Buscando portada de álbum: {album_name} de {artist_name}")
    try:
        res = get_album_cover_controller(album_name, artist_name)
        if "images" not in res or not res["images"]:
            return JSONResponse(status_code=404, content={"error": "No se encontraron imágenes para este álbum"})
        return JSONResponse(status_code=200, content=res)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
