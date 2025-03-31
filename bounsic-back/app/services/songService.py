from app.provider.azure_imgs import AZURE_CONNECTION_STRING, AZURE_CONTAINER_NAME, AZURE_CONNECTION_KEY
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from app.provider.mongo_db import db

def getSongByTitle(song_title:str):
    songs_collection = db["songs"]
    song = songs_collection.find_one({"title": song_title})
    if song:
        if "_id" in song:
            song["_id"] = str(song["_id"])
        return song
    else:
        return {"message": "Song not found"}
    
def getSongByArtist(artist: str):
    songs_collection = db["songs"]
    songs = list(songs_collection.find({"artist": artist}))
    for song in songs:
        song["_id"] = str(song["_id"])
    return songs if songs else {"message": "No songs found for this artist"}

def getSongByTitle(title: str):
    songs_collection = db["songs"]
    song = songs_collection.find_one({"title": title})
    if song:
        song["_id"] = str(song["_id"])
        return song
    return {"message": "Song not found"}

def getSongByGenre(genre: str):
    songs_collection = db["songs"]
    songs = list(songs_collection.find({"genre": genre}))
    for song in songs:
        song["_id"] = str(song["_id"])
    return songs if songs else {"message": "No songs found for this genre"}
    


######################
def get_image(blob_name: str):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
    blob_client = container_client.get_blob_client(blob_name)
    if blob_client.exists():
        return blob_client.download_blob().readall()
    else:
        return {"message": "Image not found"}

def insert_image(file_url: str, blob_name: str):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
    
    with open(file_url, "rb") as data:
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)

    # Construir URL de acceso
    return f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{blob_name}"
