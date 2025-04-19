from app.provider import DatabaseFacade

class MySQLSongService:
    _db = DatabaseFacade()

    # USERS
    @staticmethod
    def get_all_users():
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Users")
        except Exception as e:
            print.error(f"get_all_users error: {e}")
            return None

    def get_user_by_id( user_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Users WHERE id_user = %s", (user_id,))
        except Exception as e:
            print.error(f"get_user_by_id error: {e}")
            return None
        
    def get_user_by_email( email):
        try:
            query = """
                SELECT * FROM Bounsic_Users WHERE email = %s
                """
            return MySQLSongService._db.execute_query(query, (email,))
        except Exception as e:
            print.error(f"get_user_by_id error: {e}")
            return None
        
    def get_user_by_username( username):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Users WHERE username = %s", (username,))
        except Exception as e:
            print.error(f"get_user_by_id error: {e}")
            return None

    def insert_user(data):
        try:
            query = """
                INSERT INTO Bounsic_Users (name, last_name, email, pwd, profile_img, rol_user, username)
                VALUES (%s, %s, %s, %s, %s, %s,%s)
            """
            values = (
                data["name"], data["last_name"], data["email"],
                data["pwd"], data.get("profile_img"), data["rol_user"], data["username"]
            )
            return MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            print.error(f"insert_user error: {e}")
            return False

    def update_user(user_id, data):
        try:
            query = """
                UPDATE Bounsic_Users
                SET name=%s, last_name=%s, email=%s, pwd=%s, profile_img=%s, rol_user=%s, username=%s
                WHERE id_user=%s
            """
            values = (
                data["name"], data["last_name"], data["email"],
                data["pwd"], data.get("profile_img"), data["rol_user"],data["username"],
                user_id
            )
            return MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            print.error(f"update_user error: {e}")
            return False

    def delete_user( user_id):
        try:
            return MySQLSongService._db.execute_query("DELETE FROM Bounsic_Users WHERE id_user = %s", (user_id,))
        except Exception as e:
            print.error(f"delete_user error: {e}")
            return False

    # ROLES
    def get_all_roles():
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Role")
        except Exception as e:
            print.error(f"get_all_roles error: {e}")
            return None

    def get_role_by_id( role_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Role WHERE id_rol = %s", (role_id,))
        except Exception as e:
            print.error(f"get_role_by_id error: {e}")
            return None

    def insert_role( data):
        try:
            return MySQLSongService._db.execute_query(
                "INSERT INTO Bounsic_Role (name_rol) VALUES (%s)",
                (data["name_rol"],)
            )
        except Exception as e:
            print.error(f"insert_role error: {e}")
            return False

    def update_role( role_id, data):
        try:
            return MySQLSongService._db.execute_query(
                "UPDATE Bounsic_Role SET name_rol=%s WHERE id_rol=%s",
                (data["name_rol"], role_id)
            )
        except Exception as e:
            print.error(f"update_role error: {e}")
            return False

    def delete_role( role_id):
        try:
            return MySQLSongService._db.execute_query("DELETE FROM Bounsic_Role WHERE id_rol = %s", (role_id,))
        except Exception as e:
            print.error(f"delete_role error: {e}")
            return False

    # PERMISSIONS
    def get_all_permissions():
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Permissions")
        except Exception as e:
            print.error(f"get_all_permissions error: {e}")
            return None

    def get_permission_by_id( permission_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Permissions WHERE id_permission = %s", (permission_id,))
        except Exception as e:
            print.error(f"get_permission_by_id error: {e}")
            return None

    def insert_permission( data):
        try:
            return MySQLSongService._db.execute_query(
                "INSERT INTO Bounsic_Permissions (name_permission, description) VALUES (%s, %s)",
                (data["name_permission"], data.get("description"))
            )
        except Exception as e:
            print.error(f"insert_permission error: {e}")
            return False

    def update_permission( permission_id, data):
        try:
            return MySQLSongService._db.execute_query(
                "UPDATE Bounsic_Permissions SET name_permission=%s, description=%s WHERE id_permission=%s",
                (data["name_permission"], data.get("description"), permission_id)
            )
        except Exception as e:
            print.error(f"update_permission error: {e}")
            return False

    def delete_permission( permission_id):
        try:
            return MySQLSongService._db.execute_query("DELETE FROM Bounsic_Permissions WHERE id_permission = %s", (permission_id,))
        except Exception as e:
            print.error(f"delete_permission error: {e}")
            return False

    # ROLES-PERMISSIONS
    def assign_permission_to_role( role_id, permission_id):
        try:
            return MySQLSongService._db.execute_query(
                "INSERT INTO Bounsic_Role_Permissions (role_id, permission_id) VALUES (%s, %s)",
                (role_id, permission_id)
            )
        except Exception as e:
            print.error(f"assign_permission_to_role error: {e}")
            return False

    def remove_permission_from_role( role_id, permission_id):
        try:
            return MySQLSongService._db.execute_query(
                "DELETE FROM Bounsic_Role_Permissions WHERE role_id = %s AND permission_id = %s",
                (role_id, permission_id)
            )
        except Exception as e:
            print.error(f"remove_permission_from_role error: {e}")
            return False

    def get_permissions_by_role( role_id):
        try:
            query = """
                SELECT p.* FROM Bounsic_Permissions p
                JOIN Bounsic_Role_Permissions rp ON p.id_permission = rp.permission_id
                WHERE rp.role_id = %s
            """
            return MySQLSongService._db.execute_query(query, (role_id,))
        except Exception as e:
            print.error(f"get_permissions_by_role error: {e}")
            return None

    # PREFERENCES
    def get_all_preferences():
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Preferences")
        except Exception as e:
            print.error(f"get_all_preferences error: {e}")
            return None

    def get_preference_by_id( preference_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Preferences WHERE id_preferences = %s", (preference_id,))
        except Exception as e:
            print.error(f"get_preference_by_id error: {e}")
            return None

    def get_preferences_by_user( user_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Preferences WHERE user_id = %s", (user_id,))
        except Exception as e:
            print.error(f"get_preferences_by_user error: {e}")
            return None

    def insert_preference( data):
        try:
            query = "INSERT INTO Bounsic_Preferences (user_id, background, typography, language) VALUES (%s, %s, %s, %s)"
            values = (data["user_id"], data.get("background"), data.get("typography"), data.get("language"))
            return MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            print.error(f"insert_preference error: {e}")
            return False

    def update_preference( preference_id, data):
        try:
            query = "UPDATE Bounsic_Preferences SET background=%s, typography=%s, language=%s WHERE id_preferences=%s"
            values = (data.get("background"), data.get("typography"), data.get("language"), preference_id)
            return MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            print.error(f"update_preference error: {e}")
            return False

    def delete_preference( preference_id):
        try:
            return MySQLSongService._db.execute_query("DELETE FROM Bounsic_Preferences WHERE id_preferences = %s", (preference_id,))
        except Exception as e:
            print.error(f"delete_preference error: {e}")
            return False

    # HISTORY
    def get_all_history():
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_History")
        except Exception as e:
            print.error(f"get_all_history error: {e}")
            return None

    def get_history_by_id( history_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_History WHERE history_id = %s", (history_id,))
        except Exception as e:
            print.error(f"get_history_by_id error: {e}")
            return None

    def get_history_by_user( user_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_History WHERE user_id = %s", (user_id,))
        except Exception as e:
            print.error(f"get_history_by_user error: {e}")
            return None

    def insert_history( data):
        try:
            query = "INSERT INTO Bounsic_History (user_id, history_mongo_id) VALUES (%s, %s)"
            values = (data["user_id"], data["history_mongo_id"])
            return MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            print.error(f"insert_history error: {e}")
            return False

    def update_history( history_id, data):
        try:
            query = "UPDATE Bounsic_History SET user_id=%s, history_mongo_id=%s WHERE history_id=%s"
            values = (data["user_id"], data["history_mongo_id"], history_id)
            return MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            print.error(f"update_history error: {e}")
            return False

    def delete_history( history_id):
        try:
            return MySQLSongService._db.execute_query("DELETE FROM Bounsic_History WHERE history_id = %s", (history_id,))
        except Exception as e:
            print.error(f"delete_history error: {e}")
            return False
        


    # PLAYLIST
    def get_all_playlists():
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Playlist")
        except Exception as e:
            print.error(f"get_all_playlists error: {e}")
            return None

    def get_playlist_by_id( playlist_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Playlist WHERE playlist_id = %s", (playlist_id,))
        except Exception as e:
            print.error(f"get_playlist_by_id error: {e}")
            return None

    def get_playlists_by_user( user_id):
        try:
            query = """
                SELECT p.* FROM Bounsic_Playlist p
                JOIN Bounsic_User_Playlists up ON p.playlist_id = up.playlist_id
                WHERE up.user_id = %s
            """
            return MySQLSongService._db.execute_query(query, (user_id,))
        except Exception as e:
            print.error(f"get_playlists_by_user error: {e}")
            return None

    def insert_playlist(data):
        try:
            query = "INSERT INTO Bounsic_Playlist (plist_name, playlist_desc, playlist_mongo_id) VALUES (%s, %s, %s)"
            values = (data["plist_name"], data.get("playlist_desc"), data["playlist_mongo_id"])
            result = MySQLSongService._db.execute_query(query, values)

            if "user_id" in data and result:
                # Obtener el ID directamente del resultado
                playlist_id = result["lastrowid"]
                
                MySQLSongService._db.execute_query(
                    "INSERT INTO Bounsic_User_Playlists (user_id, playlist_id) VALUES (%s, %s)", 
                    (data["user_id"], playlist_id)
                )

            return result
        except Exception as e:
            print(f"insert_playlist error: {e}")
            return False

    def update_playlist( playlist_id, data):
        try:
            query = "UPDATE Bounsic_Playlist SET plist_name=%s, playlist_desc=%s, playlist_mongo_id=%s WHERE playlist_id=%s"
            values = (data["plist_name"], data.get("playlist_desc"), data["playlist_mongo_id"], playlist_id)
            return MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            print.error(f"update_playlist error: {e}")
            return False

    def delete_playlist( playlist_id):
        try:
            return MySQLSongService._db.execute_query("DELETE FROM Bounsic_Playlist WHERE playlist_id = %s", (playlist_id,))
        except Exception as e:
            print.error(f"delete_playlist error: {e}")
            return False

    # LIKE
    def get_all_likes():
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Like")
        except Exception as e:
            print.error(f"get_all_likes error: {e}")
            return None

    def get_like_by_id( like_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Like WHERE like_id = %s", (like_id,))
        except Exception as e:
            print.error(f"get_like_by_id error: {e}")
            return None

    def get_likes_by_user( user_id):
        try:
            return MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Like WHERE user_id = %s", (user_id,))
        except Exception as e:
            print.error(f"get_likes_by_user error: {e}")
            return None

    def insert_like(data):
        try:
            query = "INSERT INTO Bounsic_Like (user_id, song_mongo_id) VALUES (%s, %s)"
            values = (data["user_id"], data["song_mongo_id"])
            return MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            print.error(f"insert_like error: {e}")
            return False

    def update_like( like_id, data):
        try:
            query = "UPDATE Bounsic_Like SET user_id=%s, song_mongo_id=%s WHERE like_id=%s"
            values = (data["user_id"], data["song_mongo_id"], like_id)
            return MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            print.error(f"update_like error: {e}")
            return False

    def delete_like( like_id):
        try:
            return MySQLSongService._db.execute_query("DELETE FROM Bounsic_Like WHERE like_id = %s", (like_id,))
        except Exception as e:
            print.error(f"delete_like error: {e}")
            return False

    def get_random_likes(user_id: int, number: int):
        # Return (number) random song_id in likes of user (user_id)
        try:
            return MySQLSongService._db.execute_query("SELECT song_mongo_id FROM Bounsic_Like WHERE user_id = %s ORDER BY RAND() LIMIT %s", (user_id, number))
        except Exception as e:
            print.error(f"get_like error: {e}")
            return False

    # recomendations 
    def get_safe_choices(user_id: int) -> list[dict] | None:
        try:
            query = """
        (
            SELECT 
                'most_played' AS source,
                bh.song_mongo_id,
                bh.cant_repro AS play_count
            FROM 
                Bounsic_History bh
            WHERE 
                bh.user_id = %s
            ORDER BY 
                bh.cant_repro DESC
            LIMIT 6
        )
        UNION ALL
        (
            SELECT 
                'liked_songs' AS source,
                bl.song_mongo_id,
                0 AS play_count
            FROM 
                Bounsic_Like bl
            LEFT JOIN (
                SELECT bh2.song_mongo_id
                FROM Bounsic_History bh2
                WHERE bh2.user_id = %s
                ORDER BY bh2.cant_repro DESC
                LIMIT 6
            ) AS top_songs
            ON bl.song_mongo_id = top_songs.song_mongo_id
            WHERE 
                bl.user_id = %s AND 
                top_songs.song_mongo_id IS NULL
            ORDER BY RAND()
            LIMIT 6
            )
            """


            return MySQLSongService._db.execute_query(query, (user_id, user_id, user_id))
        except Exception as e:
            print(f"Error in get_safe_choices: {e}")
            return []
