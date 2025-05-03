from itertools import chain
from app.services import Artis_service,MySQLSongService,Song_service,Spotify_service
from fastapi.responses import JSONResponse
class Artist_controller:
    @staticmethod
    async def get_songs_by_artist_controller(artist: str):
        if not artist:
            return {"error": "Artist not provided"}
        
        print(f"Buscando canciones del artista: {artist}")
        res = Artis_service.getSongsByArtist(artist)
        
        if not res:
            return {"error": "No songs found for this artist"}
        
        return {"data": res}

    @staticmethod
    async def get_artist_desc_controller(artist: str):
        if not artist:
            return {"error": "Artist not provided"}
        
        print(f"Obteniendo descripción del artista: {artist}")
        res = Artis_service.getDesc(artist)

        if not res or isinstance(res, dict) and res.get("message"):
            return {"error": "Artist not found"}
        
        return {"data": res}

    @staticmethod
    async def get_artist_user_preferences_controller(email: str):
        try:
            if not email:
                return JSONResponse(status_code=404, content={"error": "Email not provided"})
            
            # get likes
            likes = await MySQLSongService.get_likes_by_user_email(email)
            if not likes:
                return JSONResponse(status_code=404, content={"error": "No likes found for user"})

            song_ids = [like["song_mongo_id"] for like in likes]

            songs_liked = Song_service.get_songs_by_ids(song_ids)
            if not songs_liked:
                return JSONResponse(status_code=404, content={"error": "No songs found for liked IDs"})

            # get genres
            genres = {
                genre["genre"]
                for song in songs_liked if song.get("genres")
                for genre in song["genres"]
            }
            # get artists by genre
            all_artists = []
            for genre in genres:
                artists = Spotify_service.get_artists_by_genre(genre)
                if artists:
                    all_artists.extend(artists)

            if not all_artists:
                return JSONResponse(
                    status_code=404,
                    content={"error": "No artists found for user's preferences"}
                )
            return JSONResponse(
                status_code=200,
                content=all_artists
            )

        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "details": str(e)}
            )