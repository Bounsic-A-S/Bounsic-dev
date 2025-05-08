from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
from main import app  # Asegúrate de que 'main.py' tiene tu app FastAPI

async def run():
    # Configurar Hypercorn sin SSL (HTTP/2 sin cifrado solo es válido para desarrollo local)
    config = Config()
    config.bind = ["0.0.0.0:4000"]  # Cambiado a 0.0.0.0 para aceptar conexiones externas
    config.workers = 2
    config.alpn_protocols = ["h2"]  # Activa HTTP/2
    config.use_http2 = True  # Habilita HTTP/2
    config.insecure_bind = ["0.0.0.0:4000"]  # Permite HTTP/2 sin TLS

    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(run())
