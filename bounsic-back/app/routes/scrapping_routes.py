from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import JSONResponse
from app.controllers import Scrapping_controler

router = APIRouter()

@router.get("/youtube")
async def web_scrapping(url: str = Query(..., title="URL del video de YouTube")):
    try:
        scrapping_response, download_response = await Scrapping_controler.get_youtube_scrapping_request(url)
        return JSONResponse(content={
            "scraping_data": scrapping_response
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

        
@router.get("/download")
async def descarga_yu(url: str = Query(..., description="URL del video de YouTube")):
    try:
        result = await Scrapping_controler.get_youtube_download_request(url)
        return JSONResponse(status_code=200, content={"message": "Se descargó el audio", "data": result})

    except Exception as e:
        return HTTPException(status_code=500, content={"detail": str(e)})
    
@router.get("/youtube/search")
async def buscar_youtube(q: str = Query(..., title="Término de búsqueda", description="Nombre de la canción o artista")):
    try:
        video_url = await Scrapping_controler.search_youtube_request(q)
        return {"query": q, "video_url": video_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getlyric/{song}/{artist}")
async def buscar_letra(song: str, artist: str):
    try:
        lyric = await Scrapping_controler.get_song_lyrics(song_name=song, artist=artist)
        return JSONResponse(content=lyric)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))