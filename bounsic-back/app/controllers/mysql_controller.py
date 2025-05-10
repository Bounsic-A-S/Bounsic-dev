from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging
from app.services import MySQLSongService , insert_usr_image


class MySQLController:

    dataPreference = {
        "background":"bg-bounsic-gradient",
        "typography":"",
        "language":"es",
        "theme": "dark"
    }
    # USERS
    @staticmethod
    async def get_all_users():
        try:
            users = await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Users")
            if not users:
                raise HTTPException(status_code=404, detail="No users found")
            return JSONResponse(status_code=200, content={"users": users})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_users error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching users")
        
    @staticmethod
    async def get_users_by_id( user_id):
        try:
            user = await MySQLSongService.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"user": user})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_users_by_id error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching user")
    
    @staticmethod
    async def get_users_by_email( email):
        try:
            user = await MySQLSongService.get_user_by_email(email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"user": user})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_users_by_email error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching user")
    
    @staticmethod
    async def get_users_by_username( username):
        try:
            user = await MySQLSongService.get_user_by_username(username)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"user": user})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_users_by_username error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching user")
        
    @staticmethod
    async def register_user(data):
        try:
            user = await MySQLSongService.insert_user(data)
            if not user:
                return JSONResponse(status_code=400, content={"message": "Err creating the user"})
            
            new_user = await MySQLSongService.get_user_by_email(data["email"])
            MySQLController.dataPreference["user_id"] = new_user[0]["id_user"]
            preferences = await MySQLSongService.insert_preference(MySQLController.dataPreference)
            if not preferences:
                return JSONResponse(status_code=400, content={"message": "Err creating the preferences"})
            full_user = await MySQLSongService.get_full_user_by_email(data["email"])
            full_user = full_user[0]
            transformated_user = {
                "id_user": full_user["id_user"],
                "username": full_user["username"],
                "name": full_user["name"],
                "email": full_user["email"],
                "role": full_user["role"],
                "phone":full_user["phone"],
                "country":full_user["country"],
                "profile_img": full_user["profile_img"],
                "preferences": {
                    "background": full_user["background"],
                    "typography": full_user["typography"],
                    "language": full_user["language"],
                    "theme": full_user["theme"]

                }
            }
            return JSONResponse(status_code=201, content=transformated_user)
        except Exception as e:
            logging.error(f"create_user error: {e}")
            raise HTTPException(status_code=500, detail="Error creating user")
        
    @staticmethod
    async def update_user(id, data):
        try:
            img = "same"
            if data["profile_img"] != None:
                img = await insert_usr_image(data["profile_img"])
            
            user = await MySQLSongService.update_user_by_email(id, data,img)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"user": user})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_user error: {e}")
            raise HTTPException(status_code=500, detail="Error updating user")
        
    @staticmethod
    async def delete_user( user_id):
        try:
            result = await MySQLSongService.delete_user(user_id)
            if not result:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"message": "User deleted successfully"})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"delete_user error: {e}")
            raise HTTPException(status_code=500, detail="Error deleting user")

    # ROLES
    @staticmethod
    async def get_rol_by_email(email):
        try:
            roles = await MySQLSongService.get_role_by_email(email)
            if not roles:
                raise HTTPException(status_code=404, detail="No roles found")
            return JSONResponse(status_code=200, content={"roles": roles})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_roles error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching roles")

    @staticmethod
    async def create_role( data):
        try:
            role = await MySQLSongService.insert_role(data)
            return JSONResponse(status_code=201, content={"role": role})
        except Exception as e:
            logging.error(f"create_role error: {e}")
            raise HTTPException(status_code=500, detail="Error creating role")

    # PERMISSIONS
    @staticmethod
    async def get_permissions_by_email(email):
        try:
            permissions = await MySQLSongService.get_all_permissions()
            if not permissions:
                raise HTTPException(status_code=404, detail="No permissions found")
            return JSONResponse(status_code=200, content={"permissions": permissions})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_permissions error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching permissions")

    @staticmethod
    async def create_permission( data):
        try:
            permission = await MySQLSongService.create_permission(data)
            return JSONResponse(status_code=201, content={"permission": permission})
        except Exception as e:
            logging.error(f"create_permission error: {e}")
            raise HTTPException(status_code=500, detail="Error creating permission")

    # PREFERENCES
    @staticmethod
    async def get_all_preferences():
        try:
            preferences = await MySQLSongService.get_all_preferences()
            if not preferences:
                raise HTTPException(status_code=404, detail="No preferences found")
            return JSONResponse(status_code=200, content={"preferences": preferences})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_preferences error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching preferences")
        
    @staticmethod
    async def get_preference( preference_id):
        try:
            preference = await MySQLSongService.get_preference_by_id(preference_id)
            if not preference:
                raise HTTPException(status_code=404, detail="Preference not found")
            return JSONResponse(status_code=200, content={"preference": preference})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_preference error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching preference")

    @staticmethod
    async def get_preferences_by_user( user_id):
        try:
            preferences = await MySQLSongService.get_preferences_by_user(user_id)
            if not preferences:
                raise HTTPException(status_code=404, detail="No preferences found for this user")
            return JSONResponse(status_code=200, content={"preferences": preferences})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_preferences_by_user error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching preferences by user")

    @staticmethod
    async def create_preference( data):
        try:
            preference = await MySQLSongService.insert_preference(data)
            return JSONResponse(status_code=201, content={"preference": preference})
        except Exception as e:
            logging.error(f"create_preference error: {e}")
            raise HTTPException(status_code=500, detail="Error creating preference")

    @staticmethod
    async def update_preference( email, data):
        try:
            preference = await MySQLSongService.update_preference(email, data)
            if not preference:
                raise HTTPException(status_code=404, detail="Preference not found")
            return JSONResponse(status_code=200, content={"preference": preference})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_preference error: {e}")
            raise HTTPException(status_code=500, detail="Error updating preference")

    @staticmethod
    async def delete_preference( preference_id):
        try:
            result = await MySQLSongService.delete_preference(preference_id)
            if not result:
                raise HTTPException(status_code=404, detail="Preference not found")
            return JSONResponse(status_code=200, content={"message": "Preference deleted successfully"})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"delete_preference error: {e}")
            raise HTTPException(status_code=500, detail="Error deleting preference")

    # HISTORY
    @staticmethod
    async def get_all_history():
        try:
            history = await MySQLSongService.get_all_history()
            if not history:
                raise HTTPException(status_code=404, detail="No history found")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_history error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching history")

    @staticmethod
    async def get_history( history_id):
        try:
            history = await MySQLSongService.get_history_by_id(history_id)
            if not history:
                raise HTTPException(status_code=404, detail="History not found")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_history error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching history")
        
              
    @staticmethod
    async def sum_count_history_song( email:str, id_mongo_song:str):
        try:
            # get user by email
            user = await MySQLSongService.get_user_by_email(email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_json = user[0] 
            user_id = user_json["id_user"]

            #update cant history
            history = await MySQLSongService.update_cant_history(user_id, id_mongo_song)
            print("history", history)
            if not history:
                raise HTTPException(status_code=404, detail="Could not update history")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_history error: {e}")
            raise HTTPException(status_code=500, detail="Error with  history")

    @staticmethod
    async def get_history_by_email( email):
        try:
            history = await MySQLSongService.get_history_by_user(email)
            if not history:
                raise HTTPException(status_code=404, detail="No history found for this user")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_history_by_user error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching history by user")

    @staticmethod
    async def create_history( data):
        try:
            history = await MySQLSongService.insert_history(data)
            return JSONResponse(status_code=201, content={"history": history})
        except Exception as e:
            logging.error(f"create_history error: {e}")
            raise HTTPException(status_code=500, detail="Error creating history")
        
    @staticmethod
    async def update_history( history_id, data):
        try:
            history = await MySQLSongService.update_history(history_id, data)
            if not history:
                raise HTTPException(status_code=404, detail="History not found")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_history error: {e}")
            raise HTTPException(status_code=500, detail="Error updating history")

    @staticmethod
    async def delete_history( history_id):
        try:
            result = await MySQLSongService.delete_history(history_id)
            if not result:
                raise HTTPException(status_code=404, detail="History not found")
            return JSONResponse(status_code=200, content={"message": "History deleted successfully"})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"delete_history error: {e}")
            raise HTTPException(status_code=500, detail="Error deleting history")

    # PLAYLISTS
    @staticmethod
    async def get_all_playlists():
        try:
            playlists = await MySQLSongService.get_all_playlists()
            if not playlists:
                raise HTTPException(status_code=404, detail="No playlists found")
            return JSONResponse(status_code=200, content={"playlists": playlists})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_playlists error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching playlists")

    @staticmethod
    async def get_playlist( playlist_id):
        try:
            playlist = await MySQLSongService.get_playlist_by_id(playlist_id)
            if not playlist:
                raise HTTPException(status_code=404, detail="Playlist not found")
            return JSONResponse(status_code=200, content={"playlist": playlist})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_playlist error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching playlist")

    @staticmethod
    async def get_playlists_by_user( user_id):
        try:
            playlists = await MySQLSongService.get_playlists_by_user(user_id)
            if not playlists:
                raise HTTPException(status_code=404, detail="No playlists found for this user")
            return JSONResponse(status_code=200, content={"playlists": playlists})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_playlists_by_user error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching playlists by user")
        
    @staticmethod
    async def create_playlist( data):
        try:
            playlist = await MySQLSongService.insert_playlist(data)
            return JSONResponse(status_code=201, content={"playlist": playlist})
        except Exception as e:
            logging.error(f"create_playlist error: {e}")
            raise HTTPException(status_code=500, detail="Error creating playlist")

    @staticmethod
    async def update_playlist( playlist_id, data):
        try:
            playlist = await MySQLSongService.update_playlist(playlist_id, data)
            if not playlist:
                raise HTTPException(status_code=404, detail="Playlist not found")
            return JSONResponse(status_code=200, content={"playlist": playlist})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_playlist error: {e}")
            raise HTTPException(status_code=500, detail="Error updating playlist")

    @staticmethod
    async def delete_playlist( playlist_id):
        try:
            result = await MySQLSongService.delete_playlist(playlist_id)
            if not result:
                raise HTTPException(status_code=404, detail="Playlist not found")
            return JSONResponse(status_code=200, content={"message": "Playlist deleted successfully"})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"delete_playlist error: {e}")
            raise HTTPException(status_code=500, detail="Error deleting playlist")

    # LIKES
    @staticmethod
    async def get_all_likes():
        try:
            likes = await MySQLSongService.get_all_likes()
            if not likes:
                raise HTTPException(status_code=404, detail="No likes found")
            return JSONResponse(status_code=200, content={"likes": likes})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_likes error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching likes")

    @staticmethod
    async def get_like( like_id):
        try:
            like = await MySQLSongService.get_like_by_id(like_id)
            if not like:
                raise HTTPException(status_code=404, detail="Like not found")
            return JSONResponse(status_code=200, content={"like": like})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_like error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching like")
        
    @staticmethod
    async def get_likes_by_user( user_id):
        try:
            likes = await MySQLSongService.get_likes_by_user(user_id)
            if not likes:
                raise HTTPException(status_code=404, detail="No likes found for this user")
            return JSONResponse(status_code=200, content={"likes": likes})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_likes_by_user error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching likes by user")
    @staticmethod
    async def check_like_by_user( user_id , song_id):
        try:
            likes = await MySQLSongService.check_like_by_user(user_id,song_id)
            if not likes:
                return JSONResponse(status_code=200, content=False)
            return JSONResponse(status_code=200, content=True)
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_likes_by_user error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching likes by user")

    @staticmethod
    async def create_like( user_id,song_id):
        try:
            like = await MySQLSongService.insert_like(user_id,song_id)
            return JSONResponse(status_code=201, content={"like": like})
        except Exception as e:
            logging.error(f"create_like error: {e}")
            raise HTTPException(status_code=500, detail="Error creating like")
        
    @staticmethod
    async def update_like( like_id, data):
        try:
            like = await MySQLSongService.update_like(like_id, data)
            if not like:
                raise HTTPException(status_code=404, detail="Like not found")
            return JSONResponse(status_code=200, content={"like": like})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_like error: {e}")
            raise HTTPException(status_code=500, detail="Error updating like")

    @staticmethod
    async def delete_like( user_id,song_id):
        try:
            result = await MySQLSongService.delete_like(user_id,song_id)
            if not result:
                raise HTTPException(status_code=404, detail="Like not found")
            return JSONResponse(status_code=200, content={"message": "Like deleted successfully"})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"delete_like error: {e}")
            raise HTTPException(status_code=500, detail="Error deleting like")