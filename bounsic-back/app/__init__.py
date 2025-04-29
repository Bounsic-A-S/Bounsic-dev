from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / "env" / ".env.dev"
if not load_dotenv(dotenv_path):
    print(f"⚠️ No se pudo cargar el archivo {dotenv_path}")

app = FastAPI()

# CORS setup
origins = [
    "http://localhost:4200", #dev
    "https://bounsic-front.azurewebsites.net", #prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

env_host = os.getenv("HOST", "127.0.0.1")
app_port = int(os.getenv("APP_PORT", 8000))
debug_mode = os.getenv("DEBUG", "False") == "True"
env_mode = "debug" if debug_mode else "production"
os.environ["PYTHONPYCACHEPREFIX"] = os.path.abspath("./.pycache_project")

print(f"Servidor corriendo en: http://{env_host}:{app_port} (modo: {env_mode})")


# Opcional: Importar y registrar routers aquí
from app.routes import algorithms_router, bert_router, crawl_router, scrapping_router, song_router, db_router, health_router, artist_router, spotify_router, playlist_router, mysql_router,user_router


# app.include_router(bert_router, prefix="/bert", tags=["BERT NLP"])
app.include_router(crawl_router, prefix="/crawl", tags=["Crawling"])
app.include_router(scrapping_router, prefix="/scrapping", tags=["Scrapping"])
app.include_router(song_router, prefix="/song", tags=["Song"])
app.include_router(db_router, prefix="/db", tags=["dbMongo"])
app.include_router(health_router, prefix="/health", tags=["Health Chck App"])
app.include_router(artist_router, prefix="/artist", tags=["Artist"])
app.include_router(spotify_router, prefix="/spotify", tags=["Spotify"])
app.include_router(playlist_router, prefix="/playlist", tags=["Playlist"])
app.include_router(algorithms_router, prefix="/algorithms", tags=["Algorithms"])
app.include_router(mysql_router, prefix="/mysql", tags=["Mysql"])
app.include_router(user_router, prefix="/user", tags=["User"])

