from app.provider.azure_imgs import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME, AZURE_CONNECTION_KEY
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

def generate_sas_token(blob_name: str,blob_service_client:BlobServiceClient) -> str:
    sas_token = generate_blob_sas(
        account_name=blob_service_client.account_name,
        container_name=AZURE_CONTAINER_NAME,
        blob_name=blob_name,
        account_key=AZURE_CONNECTION_KEY,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    return sas_token

def insert_image(file_url: str, blob_name: str):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
    
    with open(file_url, "rb") as data:
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)

    sas_token = generate_sas_token(blob_name,blob_service_client)

    # Construir URL de acceso
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{blob_name}?{sas_token}"

    return {
        "message": "Img created successfully",
        "blob_url": blob_url
    }
