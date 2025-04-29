from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.controllers import MySQLController

router = APIRouter()# Create an instance of the controller


@router.get("/email/{user_email}")
async def get_user_by_email(user_email: str):
    return await MySQLController.get_users_by_email(user_email)

@router.post("/register")
async def register(request: Request):
    data = await request.json()
    return MySQLController.register_user(data)

@router.put("/update/{user_email}")
async def update_user(user_email: str, request: Request):
    data = await request.json()
    return MySQLController.update_user(user_email, data)


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

@router.post("/likes")
async def create_like(request: Request):
    data = await request.json()
    return MySQLController.create_like(data)

@router.put("/likes/{like_id}")
async def update_like(like_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_like(like_id, data)

@router.delete("/likes/{like_id}")
async def delete_like(like_id: int):
    return await MySQLController.delete_like(like_id)