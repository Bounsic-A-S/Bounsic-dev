from fastapi import HTTPException
from app.services import get_album_images,get_artist_and_genre_by_track,get_artists_by_genre    


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


def get_track_info_controller(track_name: str):
    result = get_artist_and_genre_by_track(track_name)

    if not result:
        raise HTTPException(status_code=404, detail="Canción no encontrada en Spotify")

    return result