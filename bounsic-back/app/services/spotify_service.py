from app.provider import sp
def get_album_images(album_name, artist_name=None):
    query = f"{album_name} {artist_name or ''}".strip()
    print(f"🔍 Buscando álbum: {query}")
    
    result = sp.search(q=query, type="album", limit=1)
    
    if not result['albums']['items']:
        print(" No se encontró el álbum.")
        return None

    album = result['albums']['items'][0]
   
    
    return album['images']
