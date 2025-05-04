from fastapi import HTTPException
from app.services import Crawl_service

class Crawl_controller:
    @staticmethod
    def crawl_request(url: str):
        if not url:
            raise HTTPException(status_code=400, detail="La URL es obligatoria")
        
        response = Crawl_service.crawler(url)
        
        if not response:
            raise HTTPException(status_code=404, detail="No se encontraron datos")

        return response
