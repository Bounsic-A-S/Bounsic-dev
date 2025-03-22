from fastapi import APIRouter,Request
from fastapi.responses import JSONResponse
from app.provider.azure_imgs import AZURE_CONNECTION_STRING,AZURE_CONTAINER_NAME
from azure.storage.blob import BlobServiceClient
from app.services.songService import insert_image
import re

router = APIRouter()

@router.post("/img")
async def upload_(request : Request):
    data = await request.json()  # Obtener el JSON de la solicitud
    image_url = data.get("url", "")
    
    if not image_url:
        return JSONResponse(status_code=400, content={"detail": "Debe proporcionar una URL de imagen"})
    pattern = r"([^/\\]+)\.(jpg|jpeg|png|gif)"
    match = re.search(pattern, image_url)

    if not match:
        return JSONResponse(status_code=400, content={"detail": "URL de imagen no válida"})

    blob_name = match.group(0)

    response = insert_image(image_url,blob_name)  # Llama a la función del modelo
    return JSONResponse(content=response)


    
