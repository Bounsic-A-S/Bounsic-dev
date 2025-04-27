from fastapi import APIRouter
from app.controllers import get_user_by_email_controller

router = APIRouter()# Create an instance of the controller

# USERS
@router.get("/{email}")
async def get_user_by_email(email: str):
    return await get_user_by_email_controller(email)
