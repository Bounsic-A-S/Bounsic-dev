from app.provider import sp
def get_album_images(album_name, artist_name=None):
    query = f"{album_name} {artist_name or ''}".strip()
    print(f"Buscando portada de álbum: {query}")
    
    result = sp.search(q=query, type="album", limit=1)
    
    print("\n>>> Respuesta de Spotify:")
    print(result)
    
    if not result['albums']['items']:
        print(f"No se encontró el álbum: {query}")
        return
    
    album = result['albums']['items'][0]
    print(f"\nÁlbum encontrado: {album['name']} - {album['artists'][0]['name']}")
    
    return album['images']
