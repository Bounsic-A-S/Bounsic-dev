from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
async def health_check():
    try:
        return JSONResponse(content={"health":"ok","status":"200"})
    except Exception as e:
        return JSONResponse(content={"health":"damaged","status":"500"})