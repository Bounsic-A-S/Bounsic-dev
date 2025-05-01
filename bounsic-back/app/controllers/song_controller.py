from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.services import insert_image,getSongByTitle,getSongByArtist,getSongByGenre,get_image,insert_song, get_song_by_id, get_feed_recomendations
from app.services import scrappingBueno, descargar_audio , buscar_en_youtube, descargar_imagen,insert_one_song
from app.services import MySQLSongService
import logging
import re
import json
import os


async def get_song_by_artist_controller(artist: str):
    if not artist:
        return {"error": "Artist not valid"}
    
    print(f"Buscando canciones de: {artist}")
    res = getSongByArtist(artist)
    
    if not res:
        return {"error": "Not found any song by artist"}
    
    return {"data": res}

async def get_song_by_title_controller(title: str):
    if not title:
        return {"error": "Title not valid"}
    
    res = getSongByTitle(title)
    
    if not res:
        return {"error": "Not found any song by title"}
    
    return {"data": res}

async def get_songs_by_genre_controller(genre: str):
    if not genre:
        return {"error": "Genre not valid"}
    
    res = getSongByGenre(genre)
    
    if not res:
        return {"error": "Not found any song by genre"}
    
    return {"data": res}


async def get_song_image_controller(url: str):
    if not url:
        return {"error": "URL not provided"}
    
    print(url)
    res = get_image(url)
    
    if not res:
        return {"error": "Not found image for given URL"}
    
    return {"data": res}


async def insert_bs_controller(url:str):
    try:
        json_path = "D:/CursoJava/Programacion/PI-2/Pi2/Bounsic-dev/bounsic-back/images/data.json"

        if not os.path.exists(json_path):
            return {"error": "JSON file not found"}

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

                pattern_mp3 = r"([^/\\]+)\.(mp3)"
                match_mp3 = re.search(pattern_mp3, audio_path)

                if not match_mp3:
                    results.append({"title": title, "artist": artist, "status": "Nombre de archivo de audio inválido"})
                    continue

                mp3_name = match_mp3.group(0)


                pattern_img = r"([^/\\]+)\.(jpg|jpeg|png|gif)"
                match_img = re.search(pattern_img, image_path)

                if not match_img:
                    results.append({"title": title, "artist": artist, "status": "Nombre de archivo de imagen inválido"})
                    continue

                img_name = match_img.group(0)  

                
                mp3_blob_url = insert_image(audio_path, mp3_name)
                if not mp3_blob_url:
                    results.append({"title": title, "artist": artist, "status": "Fallo al insertar audio"})
                    continue

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
                    insert_one_song(mongo_song)
                    
                results.append({
                    "title": title,
                    "artist": artist,
                    "genre": genre,
                    "language": language,
                    "status": "inserted"
                })

            except Exception as song_error:
                results.append({"title": title, "artist": artist, "status": f"Error: {str(song_error)}"})
                continue  
        
        if os.path.exists(audio_path):
            os.remove(audio_path)

        if os.path.exists(image_path):
            os.remove(image_path)
            
        return {"message": "Songs processed", "data": results}

    except Exception as e:
        return {"error": str(e)}


    
    
async def insert_song_controller(track_name: str):
    result = insert_song(track_name)  
    return result

async def safe_choice_recomendation(email: str):
    try:
        # get user by email
        user = MySQLSongService.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_json = user[0] 
        user_id = user_json["id_user"]
        
        # get recommendations
        mysql_songs = MySQLSongService.get_safe_choices(user_id)
        if not mysql_songs:
            return JSONResponse(
                status_code=200,
                content={"message": "No recommendations available", "songs": []}
            )
        
        # look for songs in MongoDB
        final_songs = []
        for song in mysql_songs:
            # verify if exists song_mongo_id
            if "song_mongo_id" not in song:
                continue
                
            # serch song in MongoDB
            song_id_mongo = song["song_mongo_id"]
            mongo_song = get_song_by_id(song_id_mongo)
            
            if mongo_song:
                # create object
                combined_song = { 
                    **{k: v for k, v in mongo_song.items() if k != '_id'},  
                }
                final_songs.append(combined_song)
        
        return JSONResponse(
            status_code=200,
            content={
                "songs": final_songs,
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print.error(f"Error in safe_choice_recomendation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing recommendations"
        )
    
async def feed_related_recomendations(email: str):
    try:
        user = MySQLSongService.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_json = user[0] 
        user_id = user_json["id_user"]
        
        # get recommendations
        get_feed_recomendations(user_id)

        return JSONResponse(
            status_code=200,
            content={
                # "songs": final_songs,
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error en feed_related_recommendations: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno en la recomendación")