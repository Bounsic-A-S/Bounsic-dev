from fastapi import APIRouter,HTTPException
from app.services import crawler
from fastapi.responses import JSONResponse
router = APIRouter()

@router.get("/crawl")
async def web_crawling(url: str):
    try:
        response = crawler(url)
        print(response)
        if response:
            return JSONResponse(content=response)
        if not response:
            raise HTTPException(status_code=404, detail="No se encontraron datos")
        return JSONResponse(content=list(response))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))