
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.services import Song_service, Scrapping_service, Db_service , Spotify_service, MySQLSongService, generate_fingerprint,get_feed_recomendations, LastfmService
import logging
import re
import json
import os
import logging
import traceback
import unicodedata
from bson import ObjectId
import time

class Song_controller:
    @staticmethod
    async def get_song_by_id_controller(id: str):
        if not id:
            raise HTTPException(status_code=400, detail="ID inválido")
        res = Song_service.get_song_by_id(id)
        if not res:
            raise HTTPException(status_code=404, detail="No se encontró canción con ese ID")
        return JSONResponse(status_code=200, content=res)
    
    @staticmethod
    async def get_allSongs():
        res = Db_service.get_all_songs()
        if not res:
            raise HTTPException(status_code=404, detail="No se encontró canción con ese ID")
        return JSONResponse(status_code=200, content=res)

    @staticmethod
    async def get_song_by_artist_controller(artist: str):
        if not artist:
            raise HTTPException(status_code=400, detail="Artista inválido")
        res = Song_service.getSongByArtist(artist)
        if not res:
            raise HTTPException(status_code=404, detail="No se encontraron canciones para este artista")
        return JSONResponse(status_code=200, content={"data": res})

    @staticmethod
    async def get_song_by_title_controller(title: str):
        if not title:
            raise HTTPException(status_code=400, detail="Título inválido")
        res = Song_service.getSongByTitle(title)
        if not res:
            raise HTTPException(status_code=404, detail="No se encontró canción con este título")
        return JSONResponse(status_code=200, content={"data": res})

    @staticmethod
    async def get_songs_by_genre_controller(genre: str):
        if not genre:
            raise HTTPException(status_code=400, detail="Género inválido")
        res = Song_service.getSongByGenre(genre)
        if not res:
            raise HTTPException(status_code=404, detail="No se encontraron canciones para este género")
        return JSONResponse(status_code=200, content={"data": res})

    @staticmethod
    async def get_song_image_controller(url: str):
        if not url:
            raise HTTPException(status_code=400, detail="URL no proporcionada")
        res = Song_service.get_image(url)
        if not res:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        return JSONResponse(status_code=200, content={"data": res})

    @staticmethod
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
                    youtube_search = Scrapping_service.buscar_en_youtube(busqueda)

                    title = youtube_search['title']
                    artist = youtube_search['artist']

                    result = await Song_controller.process_song_and_album(title, artist)
                    # Ensure the result is JSON serializable
                    return Song_controller.serialize_for_json({
                        "status": "success",
                        "data": result
                    })
                except Exception as e:
                    return Song_controller.serialize_for_json({
                        "status": "error",
                        "error": str(e)
                    })
                
            return Song_controller.serialize_for_json({"message": "Songs processed", "data": results})

        except Exception as e:
            logging.error(f"Error al insertar canciones: {str(e)}")
            raise HTTPException(status_code=500, detail="Error interno al insertar canciones")

    @staticmethod
    async def insert_song_controller(track_name: str):
        result = Song_service.insert_song(track_name)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return JSONResponse(status_code=200, content=result)

    @staticmethod
    # Helper function to convert ObjectIds to strings for JSON serialization
    def serialize_for_json(obj):
        """Convert MongoDB ObjectIds to strings in a dict or list"""
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: Song_controller.serialize_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [Song_controller.serialize_for_json(item) for item in obj]
        else:
            return obj
        
    @staticmethod
    def clean_artist_name(artist: str) -> str:
        """
        Limpia el nombre del artista solo si detecta separadores comunes con espacios,
        para evitar cortar nombres reales como 'Charli XCX'.
        """
        # Separadores con espacios, indicando colaboración
        separators = [' x ', ' X ', ' & ', ' feat. ', ' Feat. ', ' FEAT. ', ', ', '; ']
        for sep in separators:
            if sep in artist:
                return artist.split(sep)[0].strip()
        return artist.strip()



    @staticmethod
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


    @staticmethod
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
            ainicio = time.time()
                        
            cleanTitle = Song_controller.clean_song_title(title)
            cleanArtist = Song_controller.clean_artist_name(artist)

            # 1. Obtener metadata de la canción desde Spotify
            spotify_data = Spotify_service.get_track_details(cleanTitle, cleanArtist)
            print(spotify_data)
            if not spotify_data:
                result["status"] = "error"
                result["error"] = "No se pudo obtener metadata de Spotify"
                return Song_controller.serialize_for_json(result)

            album_name = spotify_data["album"]
            result["album"] = album_name

            # 2. Verificar/insertar artista
            artist_info = Spotify_service.get_artist_info(cleanArtist)
            artist_db = Song_service.searchArtist(cleanArtist)
            
            if not artist_db:
                # Insertar nuevo artista
                artist_id = Song_service.insert_artist(
                    name=artist_info["name"],
                    artist_name=artist_info["artist_name"],
                    country=artist_info["country"],
                    desc=artist_info["desc"],
                )
                result["artist_id"] = artist_id
            else:
                result["artist_id"] = artist_db["_id"]

            # 3. Verificar/insertar álbum
            album_db = Song_service.searchAlbum(album_name, result["artist_id"])
            album_info = Spotify_service.get_album_info(album_name, cleanArtist)
            print(album_info)
            
            if not album_db:
                # Insertar nuevo álbum
                album_id = Song_service.insert_album(
                    name=album_info["name"],
                    release_year=album_info["release_year"],
                    img_url=album_info["img_url"],
                    artist_id=result["artist_id"]
                )
                result["album_id"] = album_id
                
                # Vincular álbum al artista
                Song_service.add_album_to_artist(result["artist_id"], result["album_id"])
                Song_service.add_artist_to_album(result["artist_id"], result["album_id"])
            else:
                result["album_id"] = album_db["_id"]
            
            for track in album_info["songs"]:
                track_title = track["name"]
                
                # Verificar si la canción ya existe
                existing_song_id = Song_service.search_song_exact(track_title, artist)
                if existing_song_id:
                    song_id = existing_song_id
                else:
                    song_result = await Song_controller.process_single_song(track_title, cleanArtist, spotify_data)
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
                Song_service.add_song_to_album(result["album_id"], song_id_obj)

                
                result["processed_songs"].append({
                    "title": track_title,
                    "status": "inserted" if not existing_song_id else "already_exists",
                    "song_id": str(song_id_obj)
                })
            afin = time.time()
            print(f"Time: {afin - ainicio:.6f} segundos")
            return Song_controller.serialize_for_json(result)
        except Exception as e:
            print(f"Error processing album: {str(e)}")
            traceback.print_exc()
            result["status"] = "error"
            result["error"] = str(e)
            return Song_controller.serialize_for_json(result)
        
    @staticmethod
    async def process_single_song(title: str, artist: str, spotify_data: dict = None):
        try:
            if not spotify_data:
                spotify_data = Spotify_service.get_track_details(title, artist)
                if not spotify_data:
                    return {"status": "error", "error": "no_spotify_data"}

            # Descargar audio
            youtube_data = Scrapping_service.buscar_en_youtube(f"{title} {artist}")
            if not youtube_data:
                return {"status": "error", "error": "youtube_not_found"}

            # Generar nombre seguro para el blob
            safe_name = f"{Song_controller.sanitize_filename(artist)}_{Song_controller.sanitize_filename(title)}.mp3"
            print(f"Generated safe filename: {safe_name}")
            download_result = await Scrapping_service.descargar_audio(youtube_data["url"] , safe_name)
            if not download_result or not download_result.get("audio"):
                return {"status": "error", "error": "download_failed"}
            
            audio_path = download_result["audio"]
            print(audio_path)
            # Verificar que el archivo existe y tiene contenido
            if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
                return {"status": "error", "error": "empty_audio_file"}

            print("blob")
            # Subir a Azure (sin await si insert_image no es async)
            mp3_blob_url = await Song_service.insert_image(audio_path, safe_name)
            
            if not mp3_blob_url:
                return {"status": "error", "error": "blob_upload_failed"}

            fingerprint = await generate_fingerprint(audio_path)
            scraping_letra = await Scrapping_service.get_lyrics(title,artist)
            
            song_data = {
                "title": title,
                "artist": artist,
                "album": spotify_data["album"],
                "genres": [{"genre": g} for g in spotify_data["genres"]],
                "lyrics":scraping_letra,
                "img_url": spotify_data["image_url"],
                "mp3_url": mp3_blob_url,
                "release_year": spotify_data["release_year"],
                "fingerprint": fingerprint
            }
            
            song_id = Song_service.insert_song_mongo(song_data)
            
            # Limpieza
            if os.path.exists(audio_path):
                os.remove(audio_path)

            # Devuelve DIRECTAMENTE el ID, no un diccionario
            return {"status": "success", "song_id": song_id}

        except Exception as e:
            return {"status": "error", "error": str(e)}
        


    @staticmethod
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

    @staticmethod
    async def safe_choice_recomendation(email: str):
        try:
            # Obtener canciones de reproducción segura desde MySQL
            mysql_songs = await MySQLSongService.get_safe_choices(email)
            if not mysql_songs:
                return JSONResponse(
                    status_code=200,
                    content=[]
                )

            # Obtener los IDs únicos de canciones Mongo
            song_ids = list({song["song_mongo_id"] for song in mysql_songs})
            mongo_songs = Song_service.get_songs_by_ids(song_ids)

            if not mongo_songs:
                return JSONResponse(
                    status_code=200,
                    content=[]
                )

            # Crear un mapa para acceso rápido por ID
            mongo_map = {str(song["_id"]): song for song in mongo_songs}
            keys = ["_id", "artist", "title", "album", "img_url"]

            # Combinar información de MySQL y MongoDB
            final_songs = [
                {k: mongo_map[song["song_mongo_id"]].get(k) for k in keys}
                for song in mysql_songs
                if song["song_mongo_id"] in mongo_map
            ]

            return JSONResponse(status_code=200, content=final_songs)

        except Exception as e:
            logging.error(f"Error en safe_choice_recommendation: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error interno en la recomendación")

    @staticmethod  
    async def get_most_listened(email: str):
        try:
            # Obtener historial reciente (máximo 12 canciones)
            mysql_songs = await MySQLSongService.get_history_month(email)
            if not mysql_songs:
                return JSONResponse(
                    status_code=200,
                    content=[]
                )

            # Extraer los IDs únicos de Mongo
            song_ids = list({song["song_mongo_id"] for song in mysql_songs})
            mongo_songs = Song_service.get_songs_by_ids(song_ids)

            if not mongo_songs:
                return JSONResponse(
                    status_code=200,
                    content=[]
                )

            # Mapear canciones Mongo por ID para acceso rápido
            mongo_map = {str(song["_id"]): song for song in mongo_songs}
            keys = ["_id", "artist", "title", "album", "img_url"]

            # Combinar resultados
            final_songs = [
                {k: mongo_map[song["song_mongo_id"]].get(k) for k in keys}
                for song in mysql_songs
                if song["song_mongo_id"] in mongo_map
            ]

            return JSONResponse(status_code=200, content=final_songs)

        except Exception as e:
            logging.error(f"Error en get_most_listened: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error interno en la recomendación")

    @staticmethod
    async def update_lyrics_controller():
        songs_mongo =  Db_service.get_all_songs_mongo()
        song_in = []

        for song in songs_mongo:
            try:
                _id = song["_id"]
                title = song["title"]
                artist = song["artist"]
                lyrics = await Scrapping_service.get_lyrics(title, artist)
                success =  Song_service.update_song_lyrics(_id, lyrics)
                if success:
                    print("lyrics inserted of:", title)
                    song_in.append(title)
            except Exception as e:
                print(f"Error en {title}: {str(e)}")

        return JSONResponse(status_code=200, content={"data": song_in})
    
    @staticmethod
    async def feed_related_recomendations(email: str):
        try:
            user = await MySQLSongService.get_user_by_email(email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_id = user[0]["id_user"]
            
            # get recommendations
            res_songs = await get_feed_recomendations(user_id)
            final_songs = []
            keys = ["_id", "artist", "title", "album", "img_url"]

            final_songs = [
                {k: str(song.get(k, "")) for k in keys}
                for song in res_songs
            ]

            return JSONResponse(
                status_code=200,
                content=final_songs
            )
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error en feed_related_recommendations: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error interno en la recomendación")
        
    @staticmethod
    async def get_top_12_songs_controller():
        try:
            print("llega")
            songs = await LastfmService.get_top_tracks_lastfm()
            if not songs:
                return JSONResponse(
                    status_code=404,
                    content={"message": "No se encontraron canciones desde Last.fm"}
                )

            result = []

            for track in songs[:12]:  # solo las 12 primeras canciones
                track_name = track.get("name")
                artist_name = track.get("artist")

                print(track_name, artist_name)

                if not (track_name and artist_name):
                    continue

                # Buscar en Mongo
                song =  Song_service.getSongByTitleAndArtist(track_name, artist_name)

                # Si ya está en Mongo
                if song and not song.get("message") == "Song not found":
                    result.append({
                        "_id": str(song.get("_id")),
                        "artist": song.get("artist"),
                        "title": song.get("title"),
                        "album": song.get("album"),
                        "img_url": song.get("img_url")
                    })
                    continue

                # Si no está, intentar insertar
                print("No está, se intenta insertar:", track_name, artist_name)
                insert_result = await Song_controller.process_song_and_album(track_name, artist_name)

                for s in insert_result.get("processed_songs", []):
                    song_id = s.get("song_id")
                    if not song_id:
                        continue
                    mongo_song =  Song_service.get_song_by_id(ObjectId(song_id))
                    if mongo_song:
                        result.append({
                            "_id": str(mongo_song.get("_id")),
                            "artist": mongo_song.get("artist"),
                            "title": mongo_song.get("title"),
                            "album": mongo_song.get("album"),
                            "img_url": mongo_song.get("img_url")
                        })

            return JSONResponse(
                status_code=200,
                content=result
            )

        except Exception as e:
            logging.error(f"Error en get_top_12_songs_controller: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error interno al obtener las canciones")


            
