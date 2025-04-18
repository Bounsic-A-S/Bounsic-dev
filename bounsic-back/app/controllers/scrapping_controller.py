from fastapi import HTTPException
from app.services import scrappingBueno, descargar_audio,buscar_en_youtube, get_lyrics
import os
def get_youtube_scrapping_request(url :str):
    if not url:
        raise HTTPException(status_code=400, detail="La URL es obligatoria")
    scrapping_response = scrappingBueno(url)
    print(scrapping_response)
    if not scrapping_response:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    download_response = descargar_audio(url)
    print(download_response)
    if not download_response:
        raise HTTPException(status_code=404, detail="No se encontraron datos")
    
    audio_path = download_response.get("audio")  
    image_path = download_response.get("thumbnail") 
    if os.path.exists(audio_path):
        os.remove(audio_path)

    if os.path.exists(image_path):
        os.remove(image_path)
    return scrapping_response,download_response

def get_youtube_download_request(url:str):
    if not url:
        raise HTTPException(status_code=400, detail="La URL es obligatoria")
    download_response = descargar_audio(url)
    if not download_response:
        raise HTTPException(status_code=404,content={"detail": "No se pudo descargar el audio"})
    return download_response

def search_youtube_request(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="El término de búsqueda es obligatorio")
    search_response = buscar_en_youtube(query)
    if not search_response:
        raise HTTPException(status_code=404, detail="No se encontraron resultados")
    return search_response

def get_song_lyrics(song_name: str, artist: str):
    if not song_name:
        raise HTTPException(status_code=400, detail="El nombre de canción es necesario")
    if not artist:
        raise HTTPException(status_code=400, detail="El nombre del artista es necesario")
    lyric_response = get_lyrics(song_name, artist)
    if not lyric_response:
        raise HTTPException(status_code=404, detail="No se encontró la letra de la canción")
    return lyric_response