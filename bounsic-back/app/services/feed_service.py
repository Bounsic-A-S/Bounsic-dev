from app.services import get_alikes, getSongByTitle, getSongByArtist, getSongByGenre, get_song_by_id
from mysql_service import MySQLSongService

def get_feed_recomendations(user_id: str):
    size = 16
    liked_songs = MySQLSongService.get_random_likes(user_id, size/2)
    latest_songs = [] # get latest songs reproductions
    songs = []

    for i in range(size/2):
        songs.append(get_song_by_id(liked_songs[i]["song_mongo_id"]))
        # songs.append(get_song_by_id(latest_songs[i]))


    # {'_id': '67f7dead113e278a2622c2b4', 
    # 'artist': 'Ariana Grande', 
    # 'title': 'positions', 
    # 'album': 'Positions', 
    # 'img_url': 'https://i.scdn.co/image/ab67616d0000b2735ef878a782c987d38d82b605', 
    # 'mp3_url': 'C:\\Users\\angie\\OneDrive\\Documentos\\AngieSextoSemestre\\ProyectoIntegrador2\\Bounsic\\bounsic-back\\app\\services\\audios\\Ariana Grande - positions (official video).mp3', 
    # 'release_year': 2020, 
    # 'genres': [{'genre': 'pop'}], 
    # 'fingerprint': []}
    for i in range(size):
        if (i % 3 == 0): # Fingerprint based
            get_alikes(song_name=songs[i]["title"])

        elif (i & 2 == 0): # Artist bases
            # Tomar album de la cancion y devolver una cancion aleatoria de ese album
            # o
            # Tomar cancion aleatoria del mismo artista
            s

        else: # Genre based
            # Buscar canciones con mismos generos
            curr_song = songs[i]
            



