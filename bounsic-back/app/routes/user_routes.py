from fastapi import APIRouter , Request
from app.controllers import get_user_by_email_controller,set_background_controller

router = APIRouter()# Create an instance of the controller

# USERS
@router.get("/{email}")
async def get_user_by_email(email: str):
    return await get_user_by_email_controller(email)

@router.put("/background/{id}")
async def set_background(id: int , request: Request):
    req = await request.json()
    background = req.get("background")
    return await set_background_controller(id,background)

@router.put("/typography/{id}")
async def set_typography(id: str , request: Request):
    req = await request.json()
    typography = req.get("typography")
    return await set_typography_controller(id,typography)

@router.put("/language/{id}")
async def set_language(id: str , request: Request):
    req = await request.json()
    language = req.get("language")
    return await set_language_controller(id,language)

