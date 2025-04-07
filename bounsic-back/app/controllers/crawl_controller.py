from fastapi import HTTPException
from app.services import crawler

def crawl_request(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="La URL es obligatoria")
    
    response = crawler(url)
    
    if not response:
        raise HTTPException(status_code=404, detail="No se encontraron datos")

    return response
