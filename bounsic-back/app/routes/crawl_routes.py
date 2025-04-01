from fastapi import APIRouter,HTTPException, Query
from app.controllers import crawl_request
from fastapi.responses import JSONResponse
router = APIRouter()

@router.get("/crawl")

async def web_crawling(url: str = Query(..., description="url to crawl")):
    print(url)
    try:
        response = crawl_request(url)
        print(response)
        if response:
            return JSONResponse(content=list(response))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))