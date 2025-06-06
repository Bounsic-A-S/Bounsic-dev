from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from streeming import router
from config import ALLOWED_ORIGINS
import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Range", "Origin", "Content-Type"],
    expose_headers=["Content-Range", "Accept-Ranges", "Content-Length"]
)

# Incluir el router de streaming
app.include_router(router)

# Ruta para servir el HTML
@app.get("/", response_class=HTMLResponse)
async def serve_html():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
