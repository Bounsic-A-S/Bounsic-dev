from typing import List
from fastapi import APIRouter, Request, HTTPException, Query  # Se agregó HTTPException
from fastapi.responses import JSONResponse
from app.services import crawler
from app.services import scrappingBueno, descargar_audio , buscar_en_youtube

router = APIRouter()

@router.post("/scraping")
async def web_scrapping(request: Request):
    data = await request.json()
    print(data)
    # response = crawler("https://www.letras.com/kendrick-lamar")
    return {"message": "funcionando!"}
    # return JSONResponse(content=list(response))

@router.get("/scrapingYutu")
async def web_scrapping1(request: Request):
    try:
        # Ejecuta el scraping
        response = scrappingBueno()

        if not response:
            raise HTTPException(status_code=404, detail="No se encontraron datos")

        # Descarga el audio
        descarga = descargar_audio("https://www.youtube.com/watch?v=_Yhyp-_hX2s")

        # Retorna la información y el estado de la descarga
        return JSONResponse(content={
            "scraping_data": response,
            "download_status": descarga
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/descarga")
async def descargaYu(url: str = Query(..., description="URL del video de YouTube")):
    try:
        if not url:
            raise HTTPException(status_code=400, detail="URL no proporcionada")

        resultado = descargar_audio(url)

        if not resultado:
            return JSONResponse(status_code=404, content={"detail": "No se pudo descargar el audio"})
        
        return JSONResponse(status_code=200, content={"message": "Se descargó el audio", "data": resultado})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})


@router.get("/scrapingYu")
async def scrap(request: Request):
    try:
        # Ejecuta el scraping
        response = scrappingBueno()

        if not response:
            raise HTTPException(status_code=404, detail="No se encontraron datos")

       
        return JSONResponse(content={
            "scraping_data": response,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/buscar-youtube")
async def buscar_youtube(query: str = Query(..., title="Término de búsqueda", description="Nombre de la canción o artista")):

    try:
        print(query)
        video_url = buscar_en_youtube(query)
        return {"query": query, "video_url": video_url}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))