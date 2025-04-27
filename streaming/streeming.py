import logging
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import StreamingResponse
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError, AzureError
from typing import Optional
from dotenv import load_dotenv
import os
from config import ALLOWED_ORIGINS

load_dotenv()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Conexión a Azure Blob Storage
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

@router.get("/stream/{blob_name}")
async def stream_audio(
    request: Request,
    blob_name: str,
    range: Optional[str] = Header(None)
):
    try:
        # Verificación de origen (modificada para permitir local si no hay origin)
        origin = request.headers.get('origin')
        if origin is not None and origin not in ALLOWED_ORIGINS:
            raise HTTPException(status_code=403, detail="Origen no permitido")

        # Conexión con Azure
        blob_client = container_client.get_blob_client(blob_name)

        # Propiedades del blob
        blob_props = blob_client.get_blob_properties()
        file_size = blob_props.size
        start, end = 0, file_size - 1

        if range:
            parts = range.replace("bytes=", "").split("-")
            start = int(parts[0])
            end = int(parts[1]) if parts[1] else file_size - 1

        if start >= file_size or end >= file_size or start > end:
            raise HTTPException(
                status_code=416,
                detail=f"Rango inválido. Tamaño del archivo: {file_size} bytes"
            )

        # Descarga del fragmento
        chunk_size = end - start + 1
        stream = blob_client.download_blob(offset=start, length=chunk_size)

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(chunk_size),
            "Content-Type": "audio/mpeg",
            "Cache-Control": "public, max-age=600",  # 10 minutos de caché
        }

        if origin:
            headers["Access-Control-Allow-Origin"] = origin
            headers["Access-Control-Expose-Headers"] = "Content-Range, Accept-Ranges, Content-Length"

        return StreamingResponse(
            stream.chunks(),
            status_code=206 if range else 200,
            headers=headers,
            media_type="audio/mpeg"
        )

    except ResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    except AzureError as e:
        logger.error(f"Error de Azure: {str(e)}")
        raise HTTPException(status_code=502, detail="Error al conectar con el almacenamiento")
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
