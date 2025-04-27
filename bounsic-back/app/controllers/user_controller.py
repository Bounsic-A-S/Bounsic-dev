from app.services import MySQLSongService
async def get_user_by_email_controller(email: str):
    try:
        user = await MySQLSongService.get_full_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user = user[0]
        transformed_user = {
            "id_user": user["id_user"],
            "username": user["username"],
            "name": user["name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "role": user["role"],
            "profile_img": user["profile_img"],
            "preferences": {
                "background": user["background"],
                "typography": user["typography"],
                "language": user["language"]
            }
        }
        return transformed_user

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))