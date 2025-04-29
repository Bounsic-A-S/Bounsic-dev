from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.services import insert_image,getSongByTitle,getSongByArtist,getSongByGenre,get_image,insert_song, get_song_by_id, get_songs_by_ids
from app.services import scrappingBueno, descargar_audio , buscar_en_youtube, descargar_imagen,insert_one_song , get_album_images, get_artist_and_genre_by_track, get_track_details
from app.services import MySQLSongService, generate_fingerprint, insert_song_mongo, add_song_to_album, add_album_to_artist, insert_album, add_artist_to_album,insert_artist, searchAlbum,searchArtist, get_artist_info, get_album_info, search_song_exact
import re
import json
import os
import logging
import traceback
import unicodedata
from bson import ObjectId

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
        json_path = "D:/CursoJava/Programacion/PI-2/Pi2/Bounsic-dev/bounsic-back/audios/data.json"

        if not os.path.exists(json_path):
            raise HTTPException(status_code=404, detail="Archivo JSON no encontrado")

        with open(json_path, "r", encoding="utf-8") as f:
            songs_list = json.load(f)
        results = []  
    
        for song in songs_list:
            try:
                titleE = song['title']
                artistE = song['artist']
                
                busqueda = f"{titleE} {artistE}"
                youtube_search = buscar_en_youtube(busqueda)

                title = youtube_search['title']
                artist = youtube_search['artist']

                video_url = youtube_search['url']

                result = await process_song_and_album(title, artist)
                # Ensure the result is JSON serializable
                return serialize_for_json({
                    "status": "success",
                    "data": result
                })
            except Exception as e:
                return serialize_for_json({
                    "status": "error",
                    "error": str(e)
                })
            
        return serialize_for_json({"message": "Songs processed", "data": results})

    except Exception as e:
        logging.error(f"Error al insertar canciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno al insertar canciones")

async def insert_song_controller(track_name: str):
    result = insert_song(track_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return JSONResponse(status_code=200, content=result)

# Helper function to convert ObjectIds to strings for JSON serialization
def serialize_for_json(obj):
    """Convert MongoDB ObjectIds to strings in a dict or list"""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    else:
        return obj
    

def clean_artist_name(artist: str) -> str:
    """
    Limpia el nombre del artista tomando solo el primer nombre antes de 'x', '&', 'feat.', etc.
    """
    separators = ['x', 'X', '&', 'feat.', 'Feat.', 'FEAT.', ',', ';']
    for sep in separators:
        if sep in artist:
            return artist.split(sep)[0].strip()
    return artist.strip()


def clean_song_title(title: str) -> str:
    """
    Limpia el nombre de la canción, extrayendo solo el título real.
    """
    # Quitar corchetes [] y paréntesis ()
    title = re.sub(r'\[.*?\]|\(.*?\)', '', title)
    
    # Si hay '|', tomar solo lo anterior
    if '|' in title:
        title = title.split('|')[0]
    
    # Si hay '-', tomar lo que está después del ÚLTIMO guion
    if '-' in title:
        parts = title.split('-')
        # Elimina partes que son artistas (usualmente antes del título)
        title = parts[-1]

    # Ahora eliminar palabras residuales tipo álbumes
    extra_words = ['Visualizer', 'Official', 'Audio', 'Video', 'Lyric', 'Lyrics', 'Album', 'Remix']
    for word in extra_words:
        title = title.replace(word, '')
    
    # Quitar espacios dobles y espacios extra
    title = re.sub(r'\s+', ' ', title)
    
    return title.strip()



# Fixed process_song_and_album function
async def process_song_and_album(title: str, artist: str):
    """
    Procesa una canción y descarga todo su álbum, con vinculaciones completas.
    """
    result = {
        "status": "success",
        "album": "",
        "artist": artist,
        "processed_songs": [],
        "failed_songs": [],
        "album_id": None,
        "artist_id": None
    }

    try:
        
        cleanTitle = clean_song_title(title)
        cleanArtist = clean_artist_name(artist)

        # 1. Obtener metadata de la canción desde Spotify
        spotify_data = get_track_details(cleanTitle, cleanArtist)

        print(spotify_data)
        if not spotify_data:
            result["status"] = "error"
            result["error"] = "No se pudo obtener metadata de Spotify"
            return serialize_for_json(result)

        album_name = spotify_data["album"]
        result["album"] = album_name

        # 2. Verificar/insertar artista
        artist_info = get_artist_info(cleanArtist)
        artist_db = searchArtist(cleanArtist)
        
        if not artist_db:
            # Insertar nuevo artista
            artist_id = insert_artist(
                name=artist_info["name"],
                artist_name=artist_info["artist_name"],
                country=artist_info["country"],
                desc=artist_info["desc"],
            )
            result["artist_id"] = artist_id
        else:
            result["artist_id"] = artist_db["_id"]

        # 3. Verificar/insertar álbum
        album_db = searchAlbum(album_name, result["artist_id"])
        album_info = get_album_info(album_name, cleanArtist)
        print(album_info)
        
        if not album_db:
            # Insertar nuevo álbum
            album_id = insert_album(
                name=album_info["name"],
                release_year=album_info["release_year"],
                img_url=album_info["img_url"],
                artist_id=result["artist_id"]
            )
            result["album_id"] = album_id
            
            # Vincular álbum al artista
            add_album_to_artist(result["artist_id"], result["album_id"])
            add_artist_to_album(result["artist_id"], result["album_id"])
        else:
            result["album_id"] = album_db["_id"]
        
        for track in album_info["songs"]:
            track_title = track["name"]
            
            # Verificar si la canción ya existe
            existing_song_id = search_song_exact(track_title, artist)
            if existing_song_id:
                song_id = existing_song_id
            else:
                song_result = await process_single_song(track_title, cleanArtist, spotify_data)
                if song_result["status"] != "success":
                    result["failed_songs"].append({
                        "title": track_title,
                        "error": song_result.get("error", "unknown_error")
                    })
                    continue
                
                song_id = song_result["song_id"]
            
            # CONVERSIÓN SEGURA A ObjectId
            try:
                if isinstance(song_id, dict):
                    # Si es diccionario, extraer el song_id
                    song_id = song_id.get("song_id", song_id.get("_id"))
                
                if isinstance(song_id, ObjectId):
                    song_id_obj = song_id
                else:
                    song_id_obj = ObjectId(song_id)
            except:
                result["failed_songs"].append({
                    "title": track_title,
                    "error": f"invalid_song_id: {song_id}"
                })
                continue

            # Agregar canción al álbum
            add_song_to_album(result["album_id"], song_id_obj)
            
            result["processed_songs"].append({
                "title": track_title,
                "status": "inserted" if not existing_song_id else "already_exists",
                "song_id": str(song_id_obj)
            })
        
        return serialize_for_json(result)
    except Exception as e:
        print(f"Error processing album: {str(e)}")
        traceback.print_exc()
        result["status"] = "error"
        result["error"] = str(e)
        return serialize_for_json(result)
    

async def process_single_song(title: str, artist: str, spotify_data: dict = None):
    try:
        if not spotify_data:
            spotify_data = get_track_details(title, artist)
            if not spotify_data:
                return {"status": "error", "error": "no_spotify_data"}

        # Descargar audio
        youtube_data = buscar_en_youtube(f"{title} {artist}")
        if not youtube_data:
            return {"status": "error", "error": "youtube_not_found"}
        
        

        # Generar nombre seguro para el blob
        safe_name = f"{sanitize_filename(artist)}_{sanitize_filename(title)}.mp3"
        print(f"Generated safe filename: {safe_name}")
        download_result = await descargar_audio(youtube_data["url"] , safe_name)
        if not download_result or not download_result.get("audio"):
            return {"status": "error", "error": "download_failed"}
        print('llega')
        audio_path = download_result["audio"]
        print(audio_path)
        # Verificar que el archivo existe y tiene contenido
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            return {"status": "error", "error": "empty_audio_file"}

        print("blob")
        # Subir a Azure (sin await si insert_image no es async)
        mp3_blob_url = await insert_image(audio_path, safe_name)
        
        if not mp3_blob_url:
            return {"status": "error", "error": "blob_upload_failed"}

        fingerprint = await generate_fingerprint(audio_path)
        
        song_data = {
            "title": title,
            "artist": artist,
            "album": spotify_data["album"],
            "genres": [{"genre": g} for g in spotify_data["genres"]],
            "img_url": spotify_data["image_url"],
            "mp3_url": mp3_blob_url,
            "release_year": spotify_data["release_year"],
            "fingerprint": fingerprint
        }
        
        song_id = insert_song_mongo(song_data)
        
        # Limpieza
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # Devuelve DIRECTAMENTE el ID, no un diccionario
        return {"status": "success", "song_id": song_id}

    except Exception as e:
        return {"status": "error", "error": str(e)}

def sanitize_filename(name: str) -> str:
    """Limpia nombres para usar en archivos, manejando caracteres Unicode."""
    # Normalizar caracteres Unicode (convertir acentos a formas básicas)
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    
    # Reemplazar caracteres no alfanuméricos por guion bajo
    sanitized_name = re.sub(r'[^\w\s-]', '', name)
    
    # Reemplazar espacios, guiones y múltiples guiones bajos con un solo guion bajo
    sanitized_name = re.sub(r'[-\s_]+', '_', sanitized_name)
    
    # Eliminar espacios en blanco al inicio y final
    sanitized_name = sanitized_name.strip('_')
    
    # Limitar la longitud del nombre
    sanitized_name = sanitized_name[:255]
    
    return sanitized_name

# Helper function to convert ObjectIds to strings for JSON serialization
def serialize_for_json(obj):
    """Convert MongoDB ObjectIds to strings in a dict or list"""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_json(item) for item in obj]
    else:
        return obj
    

def clean_artist_name(artist: str) -> str:
    """
    Limpia el nombre del artista tomando solo el primer nombre antes de 'x', '&', 'feat.', etc.
    """
    separators = ['x', 'X', '&', 'feat.', 'Feat.', 'FEAT.', ',', ';']
    for sep in separators:
        if sep in artist:
            return artist.split(sep)[0].strip()
    return artist.strip()


def clean_song_title(title: str) -> str:
    """
    Limpia el nombre de la canción, extrayendo solo el título real.
    """
    # Quitar corchetes [] y paréntesis ()
    title = re.sub(r'\[.*?\]|\(.*?\)', '', title)
    
    # Si hay '|', tomar solo lo anterior
    if '|' in title:
        title = title.split('|')[0]
    
    # Si hay '-', tomar lo que está después del ÚLTIMO guion
    if '-' in title:
        parts = title.split('-')
        # Elimina partes que son artistas (usualmente antes del título)
        title = parts[-1]

    # Ahora eliminar palabras residuales tipo álbumes
    extra_words = ['Visualizer', 'Official', 'Audio', 'Video', 'Lyric', 'Lyrics', 'Album', 'Remix']
    for word in extra_words:
        title = title.replace(word, '')
    
    # Quitar espacios dobles y espacios extra
    title = re.sub(r'\s+', ' ', title)
    
    return title.strip()



# Fixed process_song_and_album function
async def process_song_and_album(title: str, artist: str):
    """
    Procesa una canción y descarga todo su álbum, con vinculaciones completas.
    """
    result = {
        "status": "success",
        "album": "",
        "artist": artist,
        "processed_songs": [],
        "failed_songs": [],
        "album_id": None,
        "artist_id": None
    }

    try:
        
        cleanTitle = clean_song_title(title)
        cleanArtist = clean_artist_name(artist)

        # 1. Obtener metadata de la canción desde Spotify
        spotify_data = get_track_details(cleanTitle, cleanArtist)

        print(spotify_data)
        if not spotify_data:
            result["status"] = "error"
            result["error"] = "No se pudo obtener metadata de Spotify"
            return serialize_for_json(result)

        album_name = spotify_data["album"]
        result["album"] = album_name

        # 2. Verificar/insertar artista
        artist_info = get_artist_info(cleanArtist)
        artist_db = searchArtist(cleanArtist)
        
        if not artist_db:
            # Insertar nuevo artista
            artist_id = insert_artist(
                name=artist_info["name"],
                artist_name=artist_info["artist_name"],
                country=artist_info["country"],
                desc=artist_info["desc"],
            )
            result["artist_id"] = artist_id
        else:
            result["artist_id"] = artist_db["_id"]

        # 3. Verificar/insertar álbum
        album_db = searchAlbum(album_name, result["artist_id"])
        album_info = get_album_info(album_name, cleanArtist)
        print(album_info)
        
        if not album_db:
            # Insertar nuevo álbum
            album_id = insert_album(
                name=album_info["name"],
                release_year=album_info["release_year"],
                img_url=album_info["img_url"],
                artist_id=result["artist_id"]
            )
            result["album_id"] = album_id
            
            # Vincular álbum al artista
            add_album_to_artist(result["artist_id"], result["album_id"])
            add_artist_to_album(result["artist_id"], result["album_id"])
        else:
            result["album_id"] = album_db["_id"]
        
        for track in album_info["songs"]:
            track_title = track["name"]
            
            # Verificar si la canción ya existe
            existing_song_id = search_song_exact(track_title, artist)
            if existing_song_id:
                song_id = existing_song_id
            else:
                song_result = await process_single_song(track_title, cleanArtist, spotify_data)
                if song_result["status"] != "success":
                    result["failed_songs"].append({
                        "title": track_title,
                        "error": song_result.get("error", "unknown_error")
                    })
                    continue
                
                song_id = song_result["song_id"]
            
            # CONVERSIÓN SEGURA A ObjectId
            try:
                if isinstance(song_id, dict):
                    # Si es diccionario, extraer el song_id
                    song_id = song_id.get("song_id", song_id.get("_id"))
                
                if isinstance(song_id, ObjectId):
                    song_id_obj = song_id
                else:
                    song_id_obj = ObjectId(song_id)
            except:
                result["failed_songs"].append({
                    "title": track_title,
                    "error": f"invalid_song_id: {song_id}"
                })
                continue

            # Agregar canción al álbum
            add_song_to_album(result["album_id"], song_id_obj)
            
            result["processed_songs"].append({
                "title": track_title,
                "status": "inserted" if not existing_song_id else "already_exists",
                "song_id": str(song_id_obj)
            })
        
        return serialize_for_json(result)
    except Exception as e:
        print(f"Error processing album: {str(e)}")
        traceback.print_exc()
        result["status"] = "error"
        result["error"] = str(e)
        return serialize_for_json(result)
    

async def process_single_song(title: str, artist: str, spotify_data: dict = None):
    try:
        if not spotify_data:
            spotify_data = get_track_details(title, artist)
            if not spotify_data:
                return {"status": "error", "error": "no_spotify_data"}

        # Descargar audio
        youtube_data = buscar_en_youtube(f"{title} {artist}")
        if not youtube_data:
            return {"status": "error", "error": "youtube_not_found"}
        
        

        # Generar nombre seguro para el blob
        safe_name = f"{sanitize_filename(artist)}_{sanitize_filename(title)}.mp3"
        print(f"Generated safe filename: {safe_name}")
        download_result = await descargar_audio(youtube_data["url"] , safe_name)
        if not download_result or not download_result.get("audio"):
            return {"status": "error", "error": "download_failed"}
        print('llega')
        audio_path = download_result["audio"]
        print(audio_path)
        # Verificar que el archivo existe y tiene contenido
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            return {"status": "error", "error": "empty_audio_file"}

        print("blob")
        # Subir a Azure (sin await si insert_image no es async)
        mp3_blob_url = await insert_image(audio_path, safe_name)
        
        if not mp3_blob_url:
            return {"status": "error", "error": "blob_upload_failed"}

        fingerprint = await generate_fingerprint(audio_path)
        
        song_data = {
            "title": title,
            "artist": artist,
            "album": spotify_data["album"],
            "genres": [{"genre": g} for g in spotify_data["genres"]],
            "img_url": spotify_data["image_url"],
            "mp3_url": mp3_blob_url,
            "release_year": spotify_data["release_year"],
            "fingerprint": fingerprint
        }
        
        song_id = insert_song_mongo(song_data)
        
        # Limpieza
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # Devuelve DIRECTAMENTE el ID, no un diccionario
        return {"status": "success", "song_id": song_id}

    except Exception as e:
        return {"status": "error", "error": str(e)}

def sanitize_filename(name: str) -> str:
    """Limpia nombres para usar en archivos, manejando caracteres Unicode."""
    # Normalizar caracteres Unicode (convertir acentos a formas básicas)
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    
    # Reemplazar caracteres no alfanuméricos por guion bajo
    sanitized_name = re.sub(r'[^\w\s-]', '', name)
    
    # Reemplazar espacios, guiones y múltiples guiones bajos con un solo guion bajo
    sanitized_name = re.sub(r'[-\s_]+', '_', sanitized_name)
    
    # Eliminar espacios en blanco al inicio y final
    sanitized_name = sanitized_name.strip('_')
    
    # Limitar la longitud del nombre
    sanitized_name = sanitized_name[:255]
    
    return sanitized_name

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
