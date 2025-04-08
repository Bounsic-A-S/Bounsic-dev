from fastapi import HTTPException
from app.services import get_album_images


def get_album_cover_controller(album_name: str, artist_name: str = None):
    try:
        data = get_album_images(album_name, artist_name)
        if not data:
            raise HTTPException(status_code=404, detail="Álbum no encontrado en Spotify.")
        
        return {
            "images": data
        }

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
