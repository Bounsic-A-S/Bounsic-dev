from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.services import Spotify_service

class Spotify_controller:

    @staticmethod
    async def get_album_cover_controller(album_name: str, artist_name: str = None):
        try:
            data = Spotify_service.get_album_images(album_name, artist_name)
            if not data or "images" not in data or not data["images"]:
                return JSONResponse(status_code=404, content={"error": "No se encontraron imágenes para este álbum"})
            
            return JSONResponse(status_code=200, content=data)

        except HTTPException as http_err:
            raise http_err

        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
        
    @staticmethod
    async def get_track_info_controller(track_name: str):
        try:
            result = Spotify_service.get_artist_and_genre_by_track(track_name)

            if not result:
                raise HTTPException(status_code=404, detail="Canción no encontrada en Spotify")
            
            return JSONResponse(status_code=200, content=result)

        except HTTPException as http_err:
            raise http_err

        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
