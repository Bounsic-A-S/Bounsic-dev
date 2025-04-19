from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging
from app.services import MySQLSongService


class MySQLController:
    # USERS
    @staticmethod
    def get_all_users():
        try:
            users = MySQLSongService.get_all_users()
            if not users:
                raise HTTPException(status_code=404, detail="No users found")
            return JSONResponse(status_code=200, content={"users": users})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_users error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching users")
        
    @staticmethod
    def get_users_by_id( user_id):
        try:
            user = MySQLSongService.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"user": user})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_users_by_id error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching user")
    
    @staticmethod
    def get_users_by_email( email):
        try:
            user = MySQLSongService.get_user_by_email(email)
            print(user)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"user": user})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_users_by_email error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching user")
    
    @staticmethod
    def get_users_by_username( username):
        try:
            user = MySQLSongService.get_user_by_username(username)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"user": user})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_users_by_username error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching user")
    @staticmethod
    def create_user(data):
        try:
            user = MySQLSongService.insert_user(data)
            return JSONResponse(status_code=201, content={"user": user})
        except Exception as e:
            logging.error(f"create_user error: {e}")
            raise HTTPException(status_code=500, detail="Error creating user")
        
    @staticmethod
    def update_user(user_id, data):
        try:
            user = MySQLSongService.update_user(user_id, data)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return JSONResponse(status_code=200, content={"user": user})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_user error: {e}")
            raise HTTPException(status_code=500, detail="Error updating user")
    @staticmethod
    def delete_user( user_id):
        try:
            result = MySQLSongService.delete_user(user_id)
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
    def get_all_roles():
        try:
            roles = MySQLSongService.get_all_roles()
            if not roles:
                raise HTTPException(status_code=404, detail="No roles found")
            return JSONResponse(status_code=200, content={"roles": roles})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_roles error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching roles")

    @staticmethod
    def create_role( data):
        try:
            role = MySQLSongService.insert_role(data)
            return JSONResponse(status_code=201, content={"role": role})
        except Exception as e:
            logging.error(f"create_role error: {e}")
            raise HTTPException(status_code=500, detail="Error creating role")

    # PERMISSIONS
    @staticmethod
    def get_all_permissions():
        try:
            permissions = MySQLSongService.get_all_permissions()
            if not permissions:
                raise HTTPException(status_code=404, detail="No permissions found")
            return JSONResponse(status_code=200, content={"permissions": permissions})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_permissions error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching permissions")

    @staticmethod
    def create_permission( data):
        try:
            permission = MySQLSongService.create_permission(data)
            return JSONResponse(status_code=201, content={"permission": permission})
        except Exception as e:
            logging.error(f"create_permission error: {e}")
            raise HTTPException(status_code=500, detail="Error creating permission")

    # PREFERENCES
    @staticmethod
    def get_all_preferences():
        try:
            preferences = MySQLSongService.get_all_preferences()
            if not preferences:
                raise HTTPException(status_code=404, detail="No preferences found")
            return JSONResponse(status_code=200, content={"preferences": preferences})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_preferences error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching preferences")
        
    @staticmethod
    def get_preference( preference_id):
        try:
            preference = MySQLSongService.get_preference_by_id(preference_id)
            if not preference:
                raise HTTPException(status_code=404, detail="Preference not found")
            return JSONResponse(status_code=200, content={"preference": preference})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_preference error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching preference")

    @staticmethod
    def get_preferences_by_user( user_id):
        try:
            preferences = MySQLSongService.get_preferences_by_user(user_id)
            if not preferences:
                raise HTTPException(status_code=404, detail="No preferences found for this user")
            return JSONResponse(status_code=200, content={"preferences": preferences})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_preferences_by_user error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching preferences by user")

    @staticmethod
    def create_preference( data):
        try:
            preference = MySQLSongService.insert_preference(data)
            return JSONResponse(status_code=201, content={"preference": preference})
        except Exception as e:
            logging.error(f"create_preference error: {e}")
            raise HTTPException(status_code=500, detail="Error creating preference")

    @staticmethod
    def update_preference( preference_id, data):
        try:
            preference = MySQLSongService.update_preference(preference_id, data)
            if not preference:
                raise HTTPException(status_code=404, detail="Preference not found")
            return JSONResponse(status_code=200, content={"preference": preference})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_preference error: {e}")
            raise HTTPException(status_code=500, detail="Error updating preference")

    @staticmethod
    def delete_preference( preference_id):
        try:
            result = MySQLSongService.delete_preference(preference_id)
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
    def get_all_history():
        try:
            history = MySQLSongService.get_all_history()
            if not history:
                raise HTTPException(status_code=404, detail="No history found")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_history error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching history")

    @staticmethod
    def get_history( history_id):
        try:
            history = MySQLSongService.get_history_by_id(history_id)
            if not history:
                raise HTTPException(status_code=404, detail="History not found")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_history error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching history")
        
    @staticmethod
    def sum_count_history_song( email:str, id_mongo_song:str):
        try:
            # get user by email
            user = MySQLSongService.get_user_by_email(email)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_json = user[0] 
            user_id = user_json["id_user"]

            #update cant history
            history = MySQLSongService.update_cant_history(user_id, id_mongo_song)
            if not history:
                raise HTTPException(status_code=404, detail="Could not update history")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_history error: {e}")
            raise HTTPException(status_code=500, detail="Error with  history")

    @staticmethod
    def get_history_by_user( user_id):
        try:
            history = MySQLSongService.get_history_by_user(user_id)
            if not history:
                raise HTTPException(status_code=404, detail="No history found for this user")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_history_by_user error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching history by user")

    @staticmethod
    def create_history( data):
        try:
            history = MySQLSongService.insert_history(data)
            return JSONResponse(status_code=201, content={"history": history})
        except Exception as e:
            logging.error(f"create_history error: {e}")
            raise HTTPException(status_code=500, detail="Error creating history")
        
    @staticmethod
    def update_history( history_id, data):
        try:
            history = MySQLSongService.update_history(history_id, data)
            if not history:
                raise HTTPException(status_code=404, detail="History not found")
            return JSONResponse(status_code=200, content={"history": history})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_history error: {e}")
            raise HTTPException(status_code=500, detail="Error updating history")

    @staticmethod
    def delete_history( history_id):
        try:
            result = MySQLSongService.delete_history(history_id)
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
    def get_all_playlists():
        try:
            playlists = MySQLSongService.get_all_playlists()
            if not playlists:
                raise HTTPException(status_code=404, detail="No playlists found")
            return JSONResponse(status_code=200, content={"playlists": playlists})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_playlists error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching playlists")

    @staticmethod
    def get_playlist( playlist_id):
        try:
            playlist = MySQLSongService.get_playlist_by_id(playlist_id)
            if not playlist:
                raise HTTPException(status_code=404, detail="Playlist not found")
            return JSONResponse(status_code=200, content={"playlist": playlist})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_playlist error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching playlist")

    @staticmethod
    def get_playlists_by_user( user_id):
        try:
            playlists = MySQLSongService.get_playlists_by_user(user_id)
            if not playlists:
                raise HTTPException(status_code=404, detail="No playlists found for this user")
            return JSONResponse(status_code=200, content={"playlists": playlists})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_playlists_by_user error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching playlists by user")

    @staticmethod
    def create_playlist( data):
        try:
            playlist = MySQLSongService.insert_playlist(data)
            return JSONResponse(status_code=201, content={"playlist": playlist})
        except Exception as e:
            logging.error(f"create_playlist error: {e}")
            raise HTTPException(status_code=500, detail="Error creating playlist")

    @staticmethod
    def update_playlist( playlist_id, data):
        try:
            playlist = MySQLSongService.update_playlist(playlist_id, data)
            if not playlist:
                raise HTTPException(status_code=404, detail="Playlist not found")
            return JSONResponse(status_code=200, content={"playlist": playlist})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_playlist error: {e}")
            raise HTTPException(status_code=500, detail="Error updating playlist")

    @staticmethod
    def delete_playlist( playlist_id):
        try:
            result = MySQLSongService.delete_playlist(playlist_id)
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
    def get_all_likes():
        try:
            likes = MySQLSongService.get_all_likes()
            if not likes:
                raise HTTPException(status_code=404, detail="No likes found")
            return JSONResponse(status_code=200, content={"likes": likes})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_all_likes error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching likes")

    @staticmethod
    def get_like( like_id):
        try:
            like = MySQLSongService.get_like_by_id(like_id)
            if not like:
                raise HTTPException(status_code=404, detail="Like not found")
            return JSONResponse(status_code=200, content={"like": like})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_like error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching like")
        
    @staticmethod
    def get_likes_by_user( user_id):
        try:
            likes = MySQLSongService.get_likes_by_user(user_id)
            if not likes:
                raise HTTPException(status_code=404, detail="No likes found for this user")
            return JSONResponse(status_code=200, content={"likes": likes})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"get_likes_by_user error: {e}")
            raise HTTPException(status_code=500, detail="Error fetching likes by user")

    @staticmethod
    def create_like( data):
        try:
            like = MySQLSongService.create_like(data)
            return JSONResponse(status_code=201, content={"like": like})
        except Exception as e:
            logging.error(f"create_like error: {e}")
            raise HTTPException(status_code=500, detail="Error creating like")
        
    @staticmethod
    def update_like( like_id, data):
        try:
            like = MySQLSongService.update_like(like_id, data)
            if not like:
                raise HTTPException(status_code=404, detail="Like not found")
            return JSONResponse(status_code=200, content={"like": like})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"update_like error: {e}")
            raise HTTPException(status_code=500, detail="Error updating like")

    @staticmethod
    def delete_like( like_id):
        try:
            result = MySQLSongService.delete_like(like_id)
            if not result:
                raise HTTPException(status_code=404, detail="Like not found")
            return JSONResponse(status_code=200, content={"message": "Like deleted successfully"})
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"delete_like error: {e}")
            raise HTTPException(status_code=500, detail="Error deleting like")