from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.controllers.algorithms_controller import fingerprint

router = APIRouter()

@router.post("/fingerprint")
async def generate_fingerprint():
    res = await fingerprint()
    return JSONResponse(content={"response": res})
    