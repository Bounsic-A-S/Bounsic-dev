# bounsic-back/streaming.py
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import StreamingResponse
from azure.storage.blob import BlobServiceClient
from typing import Optional
import io

app = FastAPI()

# ⚠️ Coloca tu string de conexión aquí o usa variables de entorno
AZURE_CONNECTION_STRING=""
CONTAINER_NAME = ""

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

@app.get("/stream/{filename}")
async def stream_song(
    filename: str,
    range: Optional[str] = Header(None)
):
    try:
        blob_client = container_client.get_blob_client(filename)
        blob_props = blob_client.get_blob_properties()
        blob_size = blob_props.size

        # Manejo de Range Requests
        start = 0
        end = blob_size - 1

        if range:
            parts = range.replace("bytes=", "").split("-")
            start = int(parts[0])
            if parts[1]:
                end = int(parts[1])

        length = end - start + 1
        stream = blob_client.download_blob(offset=start, length=length)

        headers = {
            "Content-Range": f"bytes {start}-{end}/{blob_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(length),
            "Content-Type": "audio/mpeg"  # o el tipo correcto según tu archivo
        }

        return StreamingResponse(
            stream.chunks(),
            status_code=206 if range else 200,
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Archivo no encontrado: {e}")
