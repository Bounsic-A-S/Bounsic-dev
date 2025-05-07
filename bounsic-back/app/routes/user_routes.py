from fastapi import APIRouter , Request
from fastapi import UploadFile, Form, File, APIRouter
from app.controllers import MySQLController, User_controller

router = APIRouter()# Create an instance of the controller

# USERS
@router.get("/{email}")
async def get_user_by_email(email: str):
    return await User_controller.get_user_by_email_controller(email)

@router.put("/background/{id}")
async def set_background(id: int , request: Request):
    req = await request.json()
    background = req.get("background")
    theme = req.get("theme")
    return await User_controller.set_background_controller(id,background,theme)

@router.put("/typography/{id}")
async def set_typography(id: str , request: Request):
    req = await request.json()
    typography = req.get("typography")
    return await User_controller.set_typography_controller(id,typography)

@router.put("/language/{id}")
async def set_language(id: str , request: Request):
    req = await request.json()
    language = req.get("language")
    return await User_controller.set_language_controller(id,language)

@router.post("/register")
async def register(request: Request):
    data = await request.json()
    return await MySQLController.register_user(data)

@router.put("/update/{id}")
async def update_user(
    id: str,
    username: str = Form(...),
    phone: str = Form(...),
    country: str = Form(...),
    profile_img: UploadFile = File(None)  
):
    data = {
        "username": username,
        "phone": phone,
        "country": country,
        "profile_img": profile_img  
    }
    return await MySQLController.update_user(id, data)

# ROLES
@router.get("/roles/{user_email}")
async def get_all_roles(user_email: str):
    return await MySQLController.get_rol_by_email(user_email)

@router.post("/roles")
async def create_role(request: Request):
    data = await request.json()
    return MySQLController.create_role(data)

# PERMISSIONS


@router.post("/permissions")
async def create_permission(request: Request):
    data = await request.json()
    return MySQLController.create_permission(data)

# PREFERENCES

@router.get("/preferences/user/{user_email}")
async def get_preferences_by_user(user_email: str):
    return await MySQLController.get_preferences_by_user(user_email)


@router.put("/preferences/{user_email}")
async def update_preference(user_email: str, request: Request):
    data = await request.json()
    return MySQLController.update_preference(user_email, data)


# HISTORY

@router.patch("/sumCount")
async def sum_count_history(request: Request):
    data = await request.json()
    email = data.get("email")
    id_mongo_song = data.get("song_mongo_id")
    return  await MySQLController.sum_count_history_song(email, id_mongo_song)

@router.get("/history/user/{user_email}")
async def get_history_by_user(user_email: str):
    return await MySQLController.get_history_by_email(user_email)

@router.post("/history/create")
async def create_history(request: Request):
    data = await request.json()
    return MySQLController.create_history(data)




# PLAYLIST
@router.get("/playlists")
async def get_all_playlists():
    return await MySQLController.get_all_playlists()

@router.get("/playlists/{playlist_id}")
async def get_playlist_by_id(playlist_id: int):
    return await MySQLController.get_playlist(playlist_id)

@router.get("/playlists/user/{user_email}")
async def get_playlists_by_user(user_email: str):
    return await MySQLController.get_playlists_by_user(user_email)

@router.post("/playlists/create")
async def create_playlist(request: Request):
    data = await request.json()
    return MySQLController.create_playlist(data)

@router.put("/playlists/update")
async def update_playlist( request: Request):
    data = await request.json()
    return MySQLController.update_playlist( data)

@router.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: int):
    return await MySQLController.delete_playlist(playlist_id)

# LIKE

@router.get("/likes/{user_email}")
async def get_likes_by_user(user_email: str):
    return await MySQLController.get_likes_by_user(user_email)

@router.get("/hasLike/{user_id}/{song_id}")
async def check_like_by_user(user_id: int , song_id :str):
    return await MySQLController.check_like_by_user(user_id,song_id)

@router.post("/likes/add")
async def create_like(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    song_mongo_id = data.get("song_mongo_id")
    return await MySQLController.create_like(user_id,song_mongo_id)

@router.put("/likes/{like_id}")
async def update_like(like_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_like(like_id, data)

@router.delete("/likes/delete/{user_id}/{song_id}")
async def delete_like(user_id: int,song_id:str):
    return await MySQLController.delete_like(user_id,song_id)
