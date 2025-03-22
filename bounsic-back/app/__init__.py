# app/__init__.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from pathlib import Path


# Cargar variables de entorno desde .env.dev
dotenv_path = Path(__file__).resolve().parent.parent / "env" / ".env.dev"
if not load_dotenv(dotenv_path):
    print(f"⚠️ No se pudo cargar el archivo {dotenv_path}")

app = FastAPI()


# Leer variables de entorno
env_host = os.getenv("HOST", "127.0.0.1")
app_port = int(os.getenv("APP_PORT", 8000))
debug_mode = os.getenv("DEBUG", "False") == "True"
env_mode = "debug" if debug_mode else "production"
os.environ["PYTHONPYCACHEPREFIX"] = os.path.abspath("./.pycache_project")

print(f"Servidor corriendo en: http://{env_host}:{app_port} (modo: {env_mode})")

# Opcional: Importar y registrar routers aquí
from app.api.routes import bert_router, crawl_router, scrapping_router,song_router

app.include_router(bert_router, prefix="/bert", tags=["BERT NLP"])
app.include_router(crawl_router, prefix="/crawl", tags=["Crawling"])
app.include_router(scrapping_router, prefix="/scrapping", tags=["Scrapping"])
app.include_router(song_router, prefix="/song", tags=["Song"])

