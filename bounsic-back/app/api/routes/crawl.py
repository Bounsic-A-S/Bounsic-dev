from fastapi import APIRouter
from app.services import crawler
from fastapi.responses import JSONResponse
router = APIRouter()

@router.get("/crawl")
async def scrape_website():
    response = crawler("https://www.letras.com/kendrick-lamar")
    return JSONResponse(content=list(response))
