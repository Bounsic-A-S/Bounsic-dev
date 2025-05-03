from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.controllers import Algoritms_controller

router = APIRouter()

@router.post("/fingerprint")
async def generate_fingerprint(request: Request):
    try:
        data = await request.json()
        songName = data.get("songName","")
        
        response = Algoritms_controller.fingerprint(songName)
        return JSONResponse(content={"response": response})
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "detail": str(e)}
        )
    