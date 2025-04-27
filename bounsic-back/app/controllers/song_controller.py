from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.services import (
    getSongByArtist, getSongByTitle, getSongByGenre,
    get_album_images, insert_song
)
import os
import json
import logging

async def get_song_by_artist_controller(artist: str):
    if not artist:
        raise HTTPException(status_code=400, detail="Artist not valid")

    songs = getSongByArtist(artist)
    if isinstance(songs, dict) and "message" in songs:
        return JSONResponse(status_code=404, content=songs)
    
    return JSONResponse(status_code=200, content={"songs": songs})

async def get_song_by_title_controller(title: str):
    if not title:
        raise HTTPException(status_code=400, detail="Title not valid")

    songs = getSongByTitle(title)
    if isinstance(songs, dict) and "message" in songs:
        return JSONResponse(status_code=404, content=songs)

    return JSONResponse(status_code=200, content={"songs": songs})

async def get_songs_by_genre_controller(genre: str):
    if not genre:
        raise HTTPException(status_code=400, detail="Genre not valid")

    songs = getSongByGenre(genre)
    if isinstance(songs, dict) and "message" in songs:
        return JSONResponse(status_code=404, content=songs)

    return JSONResponse(status_code=200, content={"songs": songs})

async def get_song_image_controller(blob_name: str):
    if not blob_name:
        raise HTTPException(status_code=400, detail="Blob name not provided")

    image_data = get_album_images(blob_name)
    if not image_data:
        return JSONResponse(status_code=404, content={"message": "Image not found"})
    
    return JSONResponse(status_code=200, content={"image": image_data})

async def insert_song_controller(track_name: str):
    if not track_name:
        raise HTTPException(status_code=400, detail="Track name is required")
    
    result = insert_song(track_name)
    if "error" in result:
        return JSONResponse(status_code=500, content=result)

    return JSONResponse(status_code=201, content=result)
