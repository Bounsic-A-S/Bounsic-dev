from fastapi import HTTPException
from app.services import Scrapping_service
import os

class Scrapping_controler:
    @staticmethod
    async def get_youtube_scrapping_request(url :str):
        if not url:
            raise HTTPException(status_code=400, detail="La URL es obligatoria")
        scrapping_response = Scrapping_service.scrappingBueno(url)
        if not scrapping_response:
            raise HTTPException(status_code=404, detail="No se encontraron datos")
        download_response = Scrapping_service.descargar_audio(url)
        if not download_response:
            raise HTTPException(status_code=404, detail="No se encontraron datos")
        
        audio_path = download_response.get("audio")  
        image_path = download_response.get("thumbnail") 
        if os.path.exists(audio_path):
            os.remove(audio_path)

        if os.path.exists(image_path):
            os.remove(image_path)
        return scrapping_response,download_response

    @staticmethod
    async def get_youtube_download_request(url:str):
        if not url:
            raise HTTPException(status_code=400, detail="La URL es obligatoria")
        download_response = Scrapping_service.descargar_audio(url)
        if not download_response:
            raise HTTPException(status_code=404,content={"detail": "No se pudo descargar el audio"})
        return download_response
    @staticmethod
    async def search_youtube_request(query: str):
        if not query:
            raise HTTPException(status_code=400, detail="El término de búsqueda es obligatorio")
        search_response =  Scrapping_service.buscar_en_youtube(query)
        if not search_response:
            raise HTTPException(status_code=404, detail="No se encontraron resultados")
        return search_response
    
    @staticmethod
    async def get_song_lyrics(song_name: str, artist: str):
        if not song_name:
            raise HTTPException(status_code=400, detail="El nombre de canción es necesario")
        if not artist:
            raise HTTPException(status_code=400, detail="El nombre del artista es necesario")
        lyric_response =await  Scrapping_service.get_lyrics(song_name, artist)
        if not lyric_response:
            raise HTTPException(status_code=404, detail="No se encontró la letra de la canción")
        return lyric_response