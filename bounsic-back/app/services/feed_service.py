from app.services import get_alikes, getSongByTitle, getSongByArtist, getSongByGenre, get_song_by_id
from .mysql_service import MySQLSongService
from .db_service import get_all_songs, get_random_songs, get_random_song_by_album, get_relative_genres

def get_feed_recomendations(user_id: str):
    size = 16 # size of recomendation (pair number)
    liked_songs = MySQLSongService.get_random_likes(user_id, size//2)
    latest_songs = [] # get latest songs reproductions
    songs = [] # songs to evaluate
    res_songs = [] # final recomendations
    database_songs = get_all_songs()

    for i in range(size//2):
        if (i < len(liked_songs)):
            songs.append(get_song_by_id(liked_songs[i]["song_mongo_id"]))
        if (i < len(latest_songs)):
            songs.append(get_song_by_id(latest_songs[i]))

    for s in songs:
        if (i % 3 == 0): # Artist bases
            # Tomar album de la cancion y devolver una cancion aleatoria de ese album
            temp = get_random_song_by_album(s["album"])
            temp = get_song_by_id(temp)
            res_songs.append(temp)

            # O Tomar cancion aleatoria del mismo artista
            if (temp is None):
                res_songs.append(get_random_songs(1))

        elif (i & 2 == 0): # Fingerprint based
            alikes = get_alikes(target_song=s, database_songs=database_songs, size=1)
            res_songs += alikes

        else: # Genre based
            # Buscar canciones con mismos generos
            genres = s["genres"]

            curr_song = s

    if (len(songs) < size):
        songs += get_random_songs(size - len(songs))            



