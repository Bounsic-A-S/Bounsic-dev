from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from app.controllers import get_youtube_scrapping_request,get_youtube_download_request,search_youtube_request

router = APIRouter()

@router.get("/youtube")
async def web_scrapping(url: str = Query(..., title="URL del video de YouTube")):

    try:
        scrapping_response,download_response = get_youtube_scrapping_request(url)

        return JSONResponse(content={
            "scraping_data": scrapping_response,
            "download_status": download_response
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/download")
async def descarga_yu(url: str = Query(..., description="URL del video de YouTube")):
    try:
        result = get_youtube_download_request(url)
        return JSONResponse(status_code=200, content={"message": "Se descargó el audio", "data": result})

    except Exception as e:
        return HTTPException(status_code=500, content={"detail": str(e)})
    
@router.get("/youtube/search")
async def buscar_youtube(q: str = Query(..., title="Término de búsqueda", description="Nombre de la canción o artista")):
    try:
        video_url = search_youtube_request(q)
        return {"query": q, "video_url": video_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))