from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from app.services.songService import insert_image,getSongByTitle
from app.services import scrappingBueno, descargar_audio , buscar_en_youtube, descargar_imagen,insert_songs
import re
import json
import os

router = APIRouter()

@router.get("/title/{song_artist}")
async def getSong(song_artist:str):
    res = getSongByTitle(song_artist)
    return JSONResponse(content=res)


@router.post("/insert/songs")
async def insert_bs(request: Request):
    try:
        # Ruta del archivo JSON con las canciones
        json_path = "D:/CursoJava/Programacion/PI-2/Pi2/Bounsic-dev/bounsic-back/audios/songs_list.json"

        # Verificar si el archivo existe
        if not os.path.exists(json_path):
            return JSONResponse(status_code=400, content={"detail": "Archivo JSON no encontrado"})

        # Cargar el JSON con la lista de canciones
        with open(json_path, "r", encoding="utf-8") as f:
            songs_list = json.load(f)
        results = []  # Lista para almacenar los resultados

        for song in songs_list:
            try:
                title = song.get("title", "Desconocido")
                artist = song.get("artist", "Desconocido")
                genre = song.get("genre", "Desconocido")
                language = song.get("language", "Desconocido")

                # Construir la búsqueda en YouTube
                busqueda = f"{title} {artist}"
                video_url = buscar_en_youtube(busqueda)

                if not video_url:
                    results.append({"title": title, "artist": artist, "status": "No encontrado en YouTube"})
                    continue  # Saltar a la siguiente canción

                # Scraping de información del video
                response_scraping = scrappingBueno(video_url)
                if not response_scraping:
                    results.append({"title": title, "artist": artist, "status": "Scraping fallido"})
                    continue

                # Descargar el audio y obtener rutas separadas
                descarga = descargar_audio(video_url)

                if not descarga or not descarga.get("audio"):
                    results.append({"title": title, "artist": artist, "status": "Descarga de audio fallida"})
                    continue

                # Extraer las rutas del audio y la imagen
                audio_path = descarga.get("audio")  
                image_path = descarga.get("thumbnail")  

                pattern_mp3 = r"([^/\\]+)\.(mp3)"
                match_mp3 = re.search(pattern_mp3, audio_path)

                if not match_mp3:
                    results.append({"title": title, "artist": artist, "status": "Nombre de archivo de audio inválido"})
                    continue

                mp3_name = match_mp3.group(0)


                # Extraer el nombre del archivo de imagen
                pattern_img = r"([^/\\]+)\.(jpg|jpeg|png|gif)"
                match_img = re.search(pattern_img, image_path)

                if not match_img:
                    results.append({"title": title, "artist": artist, "status": "Nombre de archivo de imagen inválido"})
                    continue

                img_name = match_img.group(0)  

                
                # Insertar la imagen o archivo descargado
                mp3_blob_url = insert_image(audio_path, mp3_name)
                if not mp3_blob_url:
                    results.append({"title": title, "artist": artist, "status": "Fallo al insertar audio"})
                    continue

                # Insertar la imagen o archivo descargado
                img_blob_url = insert_image(image_path, img_name)
                if not img_blob_url:
                    results.append({"title": title, "artist": artist, "status": "Fallo al insertar imagen"})
                    continue
                
                if img_blob_url and mp3_blob_url:
                    mongo_song = {
                        "title": title,
                        "artist": artist,
                        "genre": genre,
                        "language": language,
                        "img_url": img_blob_url,
                        "mp3_url": mp3_blob_url
                    }
                    insert_songs(mongo_song)
                    
                # Si todo fue exitoso
                results.append({
                    "title": title,
                    "artist": artist,
                    "genre": genre,
                    "language": language,
                    "status": "inserted"
                })

            except Exception as song_error:
                results.append({"title": title, "artist": artist, "status": f"Error: {str(song_error)}"})
                continue  # No detener el proceso por un error individual
        
        #  Eliminar el archivo MP3 después de subirlo
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # Eliminar la imagen después de subirla
        if os.path.exists(image_path):
            os.remove(image_path)
            
        return JSONResponse(content={"message": "Canciones procesadas", "data": results})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    
    
