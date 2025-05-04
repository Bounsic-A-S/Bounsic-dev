from app.provider import db

class Songs_db_provider:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.load_songs()

    def load_songs(self):
        try:
            songs_collection = db["songs"]
            self.songs = list(songs_collection.find({}))

            print(f"Se cargaron {len(self.songs_cache)} canciones en caché")
        except Exception as e:
            print(f"Error al cargar canciones: {e}")
            self.songs = []
    
    def get_all(self):
        return self.songs
    
    def refresh_songs(self):
        self.load_songs()    