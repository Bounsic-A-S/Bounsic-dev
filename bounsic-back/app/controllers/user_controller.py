from app.services import MySQLSongService
from fastapi import HTTPException
from fastapi.responses import JSONResponse

async def get_user_by_email_controller(email: str):
    try:
        user = await MySQLSongService.get_full_user_by_email(email)
        if not user:
            return JSONResponse(status_code=200, content=None)
        user = user[0]
        transformed_user = {
            "id_user": user["id_user"],
            "username": user["username"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "phone":user["phone"],
            "country":user["country"],
            "profile_img": user["profile_img"],
            "preferences": {
                "background": user["background"],
                "typography": user["typography"],
                "language": user["language"],
                "theme": user["theme"]

            }
        }
        return JSONResponse(
            status_code=200,
            content=transformed_user
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def set_background_controller(id: int,background:str):
    try:
        res = await MySQLSongService.update_background(id,background)
        if not res:
            return JSONResponse(status_code=404, content={"error": "Data not updated correctly"})
        return JSONResponse(
            status_code=200,
            content=res
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def set_language_controller(id: int,language:str):
    try:
        res = await MySQLSongService.update_language(id,language)
        if not res:
            return JSONResponse(status_code=404, content={"error": "Data not updated correctly"})
        return JSONResponse(
            status_code=200,
            content=res
        )
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
