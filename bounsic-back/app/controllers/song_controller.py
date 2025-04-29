from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.services import (
    getSongByTitle, getSongByArtist, getSongByGenre, get_image, 
    insert_song, get_song_by_id, get_songs_by_ids, insert_image, 
    scrappingBueno, descargar_audio, buscar_en_youtube, descargar_imagen,
    insert_one_song, MySQLSongService
)
import os, re, json, logging

async def get_song_by_id_controller(id: str):
    if not id:
        raise HTTPException(status_code=400, detail="ID inválido")
    res = get_song_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail="No se encontró canción con ese ID")
    return JSONResponse(status_code=200, content=res)

async def get_song_by_artist_controller(artist: str):
    if not artist:
        raise HTTPException(status_code=400, detail="Artista inválido")
    res = getSongByArtist(artist)
    if not res:
        raise HTTPException(status_code=404, detail="No se encontraron canciones para este artista")
    return JSONResponse(status_code=200, content={"data": res})

async def get_song_by_title_controller(title: str):
    if not title:
        raise HTTPException(status_code=400, detail="Título inválido")
    res = getSongByTitle(title)
    if not res:
        raise HTTPException(status_code=404, detail="No se encontró canción con este título")
    return JSONResponse(status_code=200, content={"data": res})

async def get_songs_by_genre_controller(genre: str):
    if not genre:
        raise HTTPException(status_code=400, detail="Género inválido")
    res = getSongByGenre(genre)
    if not res:
        raise HTTPException(status_code=404, detail="No se encontraron canciones para este género")
    return JSONResponse(status_code=200, content={"data": res})

async def get_song_image_controller(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL no proporcionada")
    res = get_image(url)
    if not res:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    return JSONResponse(status_code=200, content={"data": res})

async def insert_bs_controller(url: str):
    try:
        json_path = "D:/CursoJava/Programacion/PI-2/Pi2/Bounsic-dev/bounsic-back/images/data.json"
        if not os.path.exists(json_path):
            raise HTTPException(status_code=404, detail="Archivo JSON no encontrado")

        with open(json_path, "r", encoding="utf-8") as f:
            songs_list = json.load(f)

        results = []
        for song in songs_list:
            try:
                title = song.get("title", "Desconocido")
                artist = song.get("artist", "Desconocido")
                genre = song.get("genre", "Desconocido")
                language = song.get("language", "Desconocido")

                busqueda = f"{title} {artist}"
                video_url = buscar_en_youtube(busqueda)

                if not video_url:
                    results.append({"title": title, "artist": artist, "status": "No encontrado en YouTube"})
                    continue

                response_scraping = scrappingBueno(video_url)
                if not response_scraping:
                    results.append({"title": title, "artist": artist, "status": "Scraping fallido"})
                    continue

                descarga = descargar_audio(video_url)
                if not descarga or not descarga.get("audio"):
                    results.append({"title": title, "artist": artist, "status": "Descarga de audio fallida"})
                    continue

                audio_path = descarga.get("audio")
                image_path = descarga.get("thumbnail")

                mp3_name = re.search(r"([^/\\]+)\.mp3", audio_path).group(0)
                img_name = re.search(r"([^/\\]+)\.(jpg|jpeg|png|gif)", image_path).group(0)

                mp3_blob_url = insert_image(audio_path, mp3_name)
                img_blob_url = insert_image(image_path, img_name)

                if not mp3_blob_url or not img_blob_url:
                    results.append({"title": title, "artist": artist, "status": "Fallo al subir archivos"})
                    continue

                mongo_song = {
                    "title": title,
                    "artist": artist,
                    "genre": genre,
                    "language": language,
                    "img_url": img_blob_url,
                    "mp3_url": mp3_blob_url
                }
                insert_one_song(mongo_song)

                results.append({"title": title, "artist": artist, "status": "Insertado"})
            except Exception as song_error:
                results.append({"title": title, "artist": artist, "status": f"Error: {str(song_error)}"})

        if os.path.exists(audio_path): os.remove(audio_path)
        if os.path.exists(image_path): os.remove(image_path)

        return JSONResponse(status_code=200, content={"message": "Songs processed", "data": results})

    except Exception as e:
        logging.error(f"Error al insertar canciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al insertar canciones")

async def insert_song_controller(track_name: str):
    result = insert_song(track_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return JSONResponse(status_code=200, content=result)

async def safe_choice_recomendation(email: str):
    try:
        mysql_songs = await MySQLSongService.get_safe_choices(email)
        if not mysql_songs:
            return JSONResponse(status_code=200, content={"message": "No hay recomendaciones disponibles", "songs": []})

        song_ids = [song["song_mongo_id"] for song in mysql_songs]
        mongo_songs = get_songs_by_ids(song_ids)
        if not mongo_songs:
            return JSONResponse(status_code=200, content={"message": "No se encontraron canciones en MongoDB", "songs": []})

        mongo_map = {song["_id"]: song for song in mongo_songs}
        final_songs = []
        keys = ["_id", "artist", "title", "album", "img_url"]

        for song in mysql_songs:
            mongo_song = mongo_map.get(song["song_mongo_id"])
            if mongo_song:
                combined = {k: mongo_song.get(k) for k in keys}
                final_songs.append(combined)

        return JSONResponse(status_code=200, content={"songs": final_songs})

    except Exception as e:
        logging.error(f"Error en safe_choice_recommendation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno en la recomendación")
