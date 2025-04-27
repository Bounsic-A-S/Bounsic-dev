from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from streeming import router
from config import ALLOWED_ORIGINS
import uvicorn
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

if __name__ == "__main__":
    # Obtén la ruta de los certificados desde las variables de entorno
    cert_file = os.getenv("CERT")
    key_file = os.getenv("KEY")
    
    # Verifica que las rutas no sean nulas y existen
    if not cert_file or not key_file:
        raise ValueError("Los archivos de certificado o clave no están configurados correctamente en .env")

    # Ejecutar uvicorn con HTTPS
    uvicorn.run(app, host="0.0.0.0", port=4000, ssl_keyfile=key_file, ssl_certfile=cert_file)
