from fastapi import HTTPException
from app.services.algorithms.fingerprint_service import generate_fingerprint
from app.services.algorithms.rhythm_service import get_alikes
from app.provider import db

def fingerprint(songName: str):
    # if not song?:
    #     raise HTTPException(status_code=400, detail="Song not found")
    res = generate_fingerprint(songName=songName)
    
    if not res:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

    return {"data": res}

def get_alikes(songName: str):
    # if not song?:
    #     raise HTTPException(status_code=400, detail="Song not found")
    # res = get_alikes();
    a