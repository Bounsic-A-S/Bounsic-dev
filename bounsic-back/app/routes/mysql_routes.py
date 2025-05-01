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


@router.put("/users/{user_id}")
async def update_user(user_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_user(user_id, data)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return await MySQLController.delete_user(user_id)

# ROLES


@router.post("/roles")
async def create_role(request: Request):
    data = await request.json()
    return MySQLController.create_role(data)



@router.post("/permissions")
async def create_permission(request: Request):
    data = await request.json()
    return MySQLController.create_permission(data)

# PREFERENCES
@router.get("/preferences")
async def get_all_preferences():
    return await MySQLController.get_all_preferences()

@router.get("/preferences/{preference_id}")
async def get_preference_by_id(preference_id: int):
    return await MySQLController.get_preference(preference_id)

@router.get("/preferences/user/{user_id}")
async def get_preferences_by_user(user_id: int):
    return await MySQLController.get_preferences_by_user(user_id)

@router.post("/preferences")
async def create_preference(request: Request):
    data = await request.json()
    return MySQLController.create_preference(data)

@router.put("/preferences/{preference_id}")
async def update_preference(preference_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_preference(preference_id, data)

@router.delete("/preferences/{preference_id}")
async def delete_preference(preference_id: int):
    return await MySQLController.delete_preference(preference_id)

# HISTORY
@router.get("/history")
async def get_all_history():
    return await MySQLController.get_all_history()

@router.get("/history/{history_id}")
async def get_history_by_id(history_id: int):
    return await MySQLController.get_history(history_id)

@router.patch("/sumCount")
async def sum_count_history(request: Request):
    data = await request.json()
    email = data.get("email")
    id_mongo_song = data.get("song_mongo_id")
    return  await MySQLController.sum_count_history_song(email, id_mongo_song)


@router.post("/history")
async def create_history(request: Request):
    data = await request.json()
    return MySQLController.create_history(data)

@router.put("/history/{history_id}")
async def update_history(history_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_history(history_id, data)

@router.delete("/history/{history_id}")
async def delete_history(history_id: int):
    return await MySQLController.delete_history(history_id)

# PLAYLIST
@router.get("/playlists")
async def get_all_playlists():
    return await MySQLController.get_all_playlists()

@router.get("/playlists/{playlist_id}")
async def get_playlist_by_id(playlist_id: int):
    return await MySQLController.get_playlist(playlist_id)

@router.get("/playlists/user/{user_id}")
async def get_playlists_by_user(user_id: int):
    return await MySQLController.get_playlists_by_user(user_id)

@router.post("/playlists")
async def create_playlist(request: Request):
    data = await request.json()
    return MySQLController.create_playlist(data)

@router.put("/playlists/{playlist_id}")
async def update_playlist(playlist_id: int, request: Request):
    data = await request.json()
    return MySQLController.update_playlist(playlist_id, data)

@router.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: int):
    return await MySQLController.delete_playlist(playlist_id)

# LIKE
@router.get("/likes")
async def get_all_likes():
    return await MySQLController.get_all_likes()

@router.get("/likes/{like_id}")
async def get_like_by_id(like_id: int):
    return await MySQLController.get_like(like_id)

@router.get("/likes/user/{user_id}")
async def get_likes_by_user(user_id: int):
    return await MySQLController.get_likes_by_user(user_id)

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