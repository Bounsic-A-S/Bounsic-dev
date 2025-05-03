from app.provider import AZURE_CONNECTION_STRING, AZUREE_CONTAINER_NAME_IMGS
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
import traceback
import uuid
from fastapi import UploadFile, File, HTTPException


async def insert_usr_image(file: UploadFile = File(...)) -> str:
    """
    Sube un archivo a Azure Blob Storage (versión corregida)
    
    Args:
        file_path: Ruta local del archivo
        blob_name: Nombre del blob en Azure
        
    Returns:
        URL pública del blob o None si falla
    """
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZUREE_CONTAINER_NAME_IMGS)

    try:
        # Nombre único
        blob_name = f"{uuid.uuid4()}-{file.filename}"

        # Subir archivo
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(await file.read(), overwrite=True)

        blob_url = blob_client.url
        return blob_url

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")

    except AzureError as azure_error:
        print(f"Error de Azure al subir {blob_name}: {str(azure_error)}")
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"Error inesperado al subir {blob_name}: {str(e)}")
        traceback.print_exc()
        return None