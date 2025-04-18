from app.services import getDesc,getSongsByArtist


async def get_songs_by_artist_controller(artist: str):
    if not artist:
        return {"error": "Artist not provided"}
    
    print(f"Buscando canciones del artista: {artist}")
    res = getSongsByArtist(artist)
    
    if not res:
        return {"error": "No songs found for this artist"}
    
    return {"data": res}


async def get_artist_desc_controller(artist: str):
    if not artist:
        return {"error": "Artist not provided"}
    
    print(f"Obteniendo descripción del artista: {artist}")
    res = getDesc(artist)

    if not res or isinstance(res, dict) and res.get("message"):
        return {"error": "Artist not found"}
    
    return {"data": res}
