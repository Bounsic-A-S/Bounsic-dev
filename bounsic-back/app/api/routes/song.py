from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from app.provider.azure_imgs import AZURE_CONNECTION_STRING,AZURE_CONTAINER_NAME
from azure.storage.blob import BlobServiceClient
from app.services.songService import insert_image,getSongByTitle
from app.services import scrappingBueno, descargar_audio , buscar_en_youtube, descargar_imagen
import re
import json
import os
from bson import json_util



router = APIRouter()

@router.get("/title/{song_artist}")
async def getSong(song_artist:str):
    res = getSongByTitle(song_artist)
    return JSONResponse(content=res)

@router.post("/create")
async def upload_(request : Request):
    data = await request.json()  # Obtener el JSON de la solicitud
    image_url = data.get("url", "")
    
    if not image_url:
        return JSONResponse(status_code=400, content={"detail": "Debe proporcionar una URL de imagen"})
    pattern = r"([^/\\]+)\.(jpg|jpeg|png|gif|mp3)"
    match = re.search(pattern, image_url)

    if not match:
        return JSONResponse(status_code=400, content={"detail": "URL de imagen no válida"})

    blob_name = match.group(0)

    response = insert_image(image_url,blob_name)  # Llama a la función del modelo
    return JSONResponse(content=response)


@router.post("/insert/songs")
async def insert_bs(request: Request):
    try:
        # Ruta del archivo JSON con las canciones
        json_path = "D:/CursoJava/Programacion/PI-2/Pi2/Bounsic-dev/bounsic-back/audios/songTry.json"

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

                # Descargar el audio del video
                descarga = descargar_audio(video_url)
                if not descarga:
                    results.append({"title": title, "artist": artist, "status": "Descarga de audio fallida"})
                    continue
                

                # Extraer el nombre del archivo MP3
                pattern_mp3 = r"([^/\\]+)\.(mp3)"
                match_mp3 = re.search(pattern_mp3, descarga)

                if not match_mp3:
                    results.append({"title": title, "artist": artist, "status": "Nombre de archivo de audio inválido"})
                    continue

                mp3_name = match_mp3.group(0)
                mp3_name_without_ext = mp3_name.replace(".mp3", "")  # Nombre sin extensión


                # 🔹 Descargar la imagen asociada
                descarga_image = descargar_imagen(video_url, mp3_name_without_ext)
                if not descarga_image:
                    results.append({"title": title,"artist": artist, "status": "Descarga de imagen fallida"})
                    continue

                # Extraer el nombre del archivo de imagen
                pattern_img = r"([^/\\]+)\.(jpg|jpeg|png|gif)"
                match_img = re.search(pattern_img, descarga_image)

                if not match_img:
                    results.append({"title": title, "artist": artist, "status": "Nombre de archivo de imagen inválido"})
                    continue

                img_name = match_img.group(0)  

                

                # Insertar la imagen o archivo descargado
                response = insert_image(descarga, mp3_name)
                if not response:
                    results.append({"title": title, "artist": artist, "status": "Fallo al insertar audio"})
                    continue

                # Insertar la imagen o archivo descargado
                response = insert_image(descarga_image, img_name)
                if not response:
                    results.append({"title": title, "artist": artist, "status": "Fallo al insertar imagen"})
                    continue

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

        return JSONResponse(content={"message": "Canciones procesadas", "data": results})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    
    
