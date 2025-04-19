from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.controllers import MySQLController

router = APIRouter()# Create an instance of the controller

# USERS
@router.get("/users")
async def get_all_users():
    return await MySQLController.get_all_users()

@router.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    return await MySQLController.get_users_by_id(user_id)

@router.get("/users/email/{user_email}")
async def get_user_by_email(user_email: str):
    return await MySQLController.get_users_by_email(user_email)

@router.get("/users/username/{username}")
async def get_user_by_username(username: str):
    return await MySQLController.get_users_by_username(username)

@router.post("/users")
async def create_user(request: Request):
    data = await request.json()
    return MySQLController.create_user(data)

@router.put("/users/{user_id}")
async def update_user(user_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_user(user_id, data)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return await MySQLController.delete_user(user_id)

# ROLES
@router.get("/roles")
async def get_all_roles():
    return await MySQLController.get_all_roles()

@router.post("/roles")
async def create_role(request: Request):
    data = await request.json()
    return MySQLController.create_role(data)

# PERMISSIONS
@router.get("/permissions")
def get_all_permissions():
    return MySQLController.get_all_permissions()

@router.post("/permissions")
async def create_permission(request: Request):
    data = await request.json()
    return MySQLController.create_permission(data)

# PREFERENCES
@router.get("/preferences")
def get_all_preferences():
    return MySQLController.get_all_preferences()

@router.get("/preferences/{preference_id}")
def get_preference_by_id(preference_id: int):
    return MySQLController.get_preference(preference_id)

@router.get("/preferences/user/{user_id}")
def get_preferences_by_user(user_id: int):
    return MySQLController.get_preferences_by_user(user_id)

@router.post("/preferences")
async def create_preference(request: Request):
    data = await request.json()
    return MySQLController.create_preference(data)

@router.put("/preferences/{preference_id}")
async def update_preference(preference_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_preference(preference_id, data)

@router.delete("/preferences/{preference_id}")
def delete_preference(preference_id: int):
    return MySQLController.delete_preference(preference_id)

# HISTORY
@router.get("/history")
def get_all_history():
    return MySQLController.get_all_history()

@router.get("/history/{history_id}")
def get_history_by_id(history_id: int):
    return MySQLController.get_history(history_id)

@router.patch("/sumCount")
async def sum_count_history(request: Request):
    data = await request.json()
    email = data.get("email")
    id_mongo_song = data.get("song_mongo_id")
    return MySQLController.sum_count_history_song(email, id_mongo_song)

@router.get("/history/user/{user_id}")
def get_history_by_user(user_id: int):
    return MySQLController.get_history_by_user(user_id)

@router.post("/history")
async def create_history(request: Request):
    data = await request.json()
    return MySQLController.create_history(data)

@router.put("/history/{history_id}")
async def update_history(history_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_history(history_id, data)

@router.delete("/history/{history_id}")
def delete_history(history_id: int):
    return MySQLController.delete_history(history_id)

# PLAYLIST
@router.get("/playlists")
def get_all_playlists():
    return MySQLController.get_all_playlists()

@router.get("/playlists/{playlist_id}")
def get_playlist_by_id(playlist_id: int):
    return MySQLController.get_playlist(playlist_id)

@router.get("/playlists/user/{user_id}")
def get_playlists_by_user(user_id: int):
    return MySQLController.get_playlists_by_user(user_id)

@router.post("/playlists")
async def create_playlist(request: Request):
    data = await request.json()
    return MySQLController.create_playlist(data)

@router.put("/playlists/{playlist_id}")
async def update_playlist(playlist_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_playlist(playlist_id, data)

@router.delete("/playlists/{playlist_id}")
def delete_playlist(playlist_id: int):
    return MySQLController.delete_playlist(playlist_id)

# LIKE
@router.get("/likes")
def get_all_likes():
    return MySQLController.get_all_likes()

@router.get("/likes/{like_id}")
def get_like_by_id(like_id: int):
    return MySQLController.get_like(like_id)

@router.get("/likes/user/{user_id}")
def get_likes_by_user(user_id: int):
    return MySQLController.get_likes_by_user(user_id)

@router.post("/likes")
async def create_like(request: Request):
    data = await request.json()
    return MySQLController.create_like(data)

@router.put("/likes/{like_id}")
async def update_like(like_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_like(like_id, data)

@router.delete("/likes/{like_id}")
def delete_like(like_id: int):
    return MySQLController.delete_like(like_id)