from app.provider.azure_imgs import AZURE_CONNECTION_STRING,AZURE_CONTAINER_NAME
from azure.storage.blob import BlobServiceClient

def insert_image(file_url : str , blob_save:str): # blob_save -> img name to save in azure
    print(file_url)
    print(blob_save)
    print(AZURE_CONNECTION_STRING)
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    with open(file_url, "rb") as data:
        blob_client = container_client.get_blob_client(blob_save)
        blob_client.upload_blob(data, overwrite=True)

    return {"message": "Img created successfully",
            "blob_url": f"https://{AZURE_CONTAINER_NAME}.blob.core.windows.net/{blob_save}"
            }