from fastapi import HTTPException
from app.services.algorithms_service import generate_fingerprint

def fingerprint():
    # if not song?:
    #     raise HTTPException(status_code=400, detail="Song not found")
    res = generate_fingerprint()
    
    if not res:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

    return {"data": res}
