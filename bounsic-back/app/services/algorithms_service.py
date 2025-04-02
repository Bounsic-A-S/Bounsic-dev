from app.provider import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME
from azure.storage.blob import BlobServiceClient
from app.provider import db

def test():
    return {"message": "Song not found"}