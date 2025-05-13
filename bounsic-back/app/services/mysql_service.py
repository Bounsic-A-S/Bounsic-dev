from app.provider import DatabaseFacade
import logging

class MySQLSongService:
    _db = DatabaseFacade()

    # USERS
    @staticmethod
    async def get_all_users():
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Users")
        except Exception as e:
            logging.error(f"get_all_users error: {e}")
            return None
        
    @staticmethod
    async def get_user_by_id( user_id):
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Users WHERE id_user = :user_id",{"user_id":user_id})
        except Exception as e:
            logging.error(f"get_user_by_id error: {e}")
            return None
        
    @staticmethod
    async def get_user_by_email( email):
        try:
            query = "SELECT * FROM Bounsic_Users WHERE email = :email"
            return await MySQLSongService._db.execute_query(query, {"email":email})
        except Exception as e:
            logging.error(f"get_user_by_id error: {e}")
            return None
        
    @staticmethod   
    async def get_user_by_username( username):
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Users WHERE username = %s", (username,))
        except Exception as e:
            logging.error(f"get_user_by_id error: {e}")
            return None

    @staticmethod
    async def insert_user(data):
        try:
            query = """
                INSERT INTO Bounsic_Users (name, username, email, profile_img, rol_user, phone, country )
                VALUES (:name, :username, :email, null, 2, :phone, 'colombia'  )
            """
            return await MySQLSongService._db.execute_query(query, data)
        except Exception as e:
            logging.error(f"insert_user error: {e}")
            return False


    @staticmethod
    async def update_user_by_email(id, data, img):
        try:
            fields = []
            params = {
                "username": data["username"],
                "phone": data["phone"],
                "country": data["country"],
                "id": id
            }
            if img != "same" and img is not None:
                fields.append("profile_img = :profile_img")
                params["profile_img"] = img

            fields.append("username = :username")
            fields.append("phone = :phone")
            fields.append("country = :country")

            query = f"""
                UPDATE Bounsic_Users
                SET {', '.join(fields)}
                WHERE id_user = :id
            """

            return await MySQLSongService._db.execute_query(query, params)

        except Exception as e:
            logging.error(f"update_user_by_id error: {e}")
            return False

    @staticmethod
    async def delete_user( user_id):
        try:
            return await MySQLSongService._db.execute_query("DELETE FROM Bounsic_Users WHERE id_user = %s", (user_id,))
        except Exception as e:
            logging.error(f"delete_user error: {e}")
            return False

    # ROLES
    @staticmethod
    async def get_all_roles():
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Role")
        except Exception as e:
            logging.error(f"get_all_roles error: {e}")
            return None

    @staticmethod
    async def get_role_by_id( role_id):
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Role WHERE id_rol = %s", (role_id,))
        except Exception as e:
            logging.error(f"get_role_by_id error: {e}")
            return None

    @staticmethod
    async def insert_role( data):
        try:
            return await MySQLSongService._db.execute_query(
                "INSERT INTO Bounsic_Role (name_rol) VALUES (%s)",
                (data["name_rol"],)
            )
        except Exception as e:
            logging.error(f"insert_role error: {e}")
            return False

    @staticmethod
    async def update_role( role_id, data):
        try:
            return await MySQLSongService._db.execute_query(
                "UPDATE Bounsic_Role SET name_rol=%s WHERE id_rol=%s",
                (data["name_rol"], role_id)
            )
        except Exception as e:
            logging.error(f"update_role error: {e}")
            return False

    @staticmethod
    async def delete_role( role_id):
        try:
            return await MySQLSongService._db.execute_query("DELETE FROM Bounsic_Role WHERE id_rol = %s", (role_id,))
        except Exception as e:
            logging.error(f"delete_role error: {e}")
            return False

    # PERMISSIONS
    @staticmethod
    async def get_all_permissions():
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Permissions")
        except Exception as e:
            logging.error(f"get_all_permissions error: {e}")
            return None

    @staticmethod
    async def get_permission_by_id( permission_id):
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Permissions WHERE id_permission = %s", (permission_id,))
        except Exception as e:
            logging.error(f"get_permission_by_id error: {e}")
            return None

    @staticmethod
    async def insert_permission( data):
        try:
            return await MySQLSongService._db.execute_query(
                "INSERT INTO Bounsic_Permissions (name_permission, description) VALUES (%s, %s)",
                (data["name_permission"], data.get("description"))
            )
        except Exception as e:
            logging.error(f"insert_permission error: {e}")
            return False

    @staticmethod
    async def update_permission( permission_id, data):
        try:
            return await MySQLSongService._db.execute_query(
                "UPDATE Bounsic_Permissions SET name_permission=%s, description=%s WHERE id_permission=%s",
                (data["name_permission"], data.get("description"), permission_id)
            )
        except Exception as e:
            logging.error(f"update_permission error: {e}")
            return False

    @staticmethod
    async def delete_permission( permission_id):
        try:
            return await MySQLSongService._db.execute_query("DELETE FROM Bounsic_Permissions WHERE id_permission = %s", (permission_id,))
        except Exception as e:
            logging.error(f"delete_permission error: {e}")
            return False

    # ROLES-PERMISSIONS
    @staticmethod
    async def assign_permission_to_role( role_id, permission_id):
        try:
            return await MySQLSongService._db.execute_query(
                "INSERT INTO Bounsic_Role_Permissions (role_id, permission_id) VALUES (%s, %s)",
                (role_id, permission_id)
            )
        except Exception as e:
            logging.error(f"assign_permission_to_role error: {e}")
            return False

    @staticmethod
    async def remove_permission_from_role( role_id, permission_id):
        try:
            return await MySQLSongService._db.execute_query(
                "DELETE FROM Bounsic_Role_Permissions WHERE role_id = %s AND permission_id = %s",
                (role_id, permission_id)
            )
        except Exception as e:
            logging.error(f"remove_permission_from_role error: {e}")
            return False

    @staticmethod
    async def get_permissions_by_role( role_id):
        try:
            query = """
                SELECT p.* FROM Bounsic_Permissions p
                JOIN Bounsic_Role_Permissions rp ON p.id_permission = rp.permission_id
                WHERE rp.role_id = %s
            """
            return await MySQLSongService._db.execute_query(query, (role_id,))
        except Exception as e:
            logging.error(f"get_permissions_by_role error: {e}")
            return None

    # PREFERENCES
    @staticmethod
    async def get_all_preferences():
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Preferences")
        except Exception as e:
            logging.error(f"get_all_preferences error: {e}")
            return None

    @staticmethod
    async def get_preference_by_id( preference_id):
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Preferences WHERE id_preferences = %s", (preference_id,))
        except Exception as e:
            logging.error(f"get_preference_by_id error: {e}")
            return None

    @staticmethod
    async def get_preferences_by_user( user_id):
        try:
            query = "SELECT * FROM Bounsic_Preferences WHERE user_id = :user_id"
            return await MySQLSongService._db.execute_query(query, {"user_id": user_id})
        except Exception as e:
            logging.error(f"get_preferences_by_user error: {e}")
            return None

    @staticmethod
    async def insert_preference( data):
        try:
            query = """
                INSERT INTO Bounsic_Preferences (user_id, background, typography, language)
                VALUES (:user_id, :background, :typography, :language)
            """
            return await MySQLSongService._db.execute_query(query, data)
        except Exception as e:
            logging.error(f"insert_preference error: {e}")
            return False


    @staticmethod
    async def update_background( user_id, background, theme):
        try:
            query = "UPDATE Bounsic_Preferences SET background= :background, theme= :theme WHERE user_id= :user_id"
            values = {
            "user_id": user_id,
            "background": background,
            "theme": theme
        }
            return await MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            logging.error(f"insert_preference error: {e}")
            return False

    @staticmethod
    async def update_preference( preference_id, data):
        try:
            query = "UPDATE Bounsic_Preferences SET typography= :fontSize WHERE user_id= :user_id"
            values = {
                "user_id": user_id,
                "fontSize": fontSize
            }
            return await MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            logging.error(f"update_preference error: {e}")
            return False
    @staticmethod
    async def update_language( user_id, language):
        try:
            query = "UPDATE Bounsic_Preferences SET language= :language WHERE user_id= :user_id"
            values = {
                "user_id": user_id,
                "language": language
            }
            return await MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            logging.error(f"update_preference error: {e}")
            return False

    @staticmethod
    async def delete_preference( preference_id):
        try:
            return await MySQLSongService._db.execute_query("DELETE FROM Bounsic_Preferences WHERE id_preferences = %s", (preference_id,))
        except Exception as e:
            logging.error(f"delete_preference error: {e}")
        return False

    # HISTORY
    @staticmethod
    async def get_all_history():
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_History")
        except Exception as e:
            logging.error(f"get_all_history error: {e}")
            return None

    @staticmethod
    async def get_history_by_id( history_id):
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_History WHERE history_id = %s", (history_id,))
        except Exception as e:
            logging.error(f"get_history_by_id error: {e}")
            return None
    
    @staticmethod
    async def update_cant_history(id_user: int, id_mongo_song: str):
        try:
            # Intentar actualizar
            query_update = """
                UPDATE Bounsic_History
                SET cant_repro = cant_repro + 1
                WHERE user_id = :id_user AND song_mongo_id = :id_mongo_song
            """
            result = await MySQLSongService._db.execute_query(query_update, {
                "id_user": id_user,
                "id_mongo_song": id_mongo_song
            })

            # Verificar si se actualizó alguna fila
            if result.rowcount == 0:
                # Si no, insertar nueva entrada
                query_insert = """
                    INSERT INTO Bounsic_History (user_id, song_mongo_id, cant_repro)
                    VALUES (:id_user, :id_mongo_song, 1)
                """
                await MySQLSongService._db.execute_query(query_insert, {
                    "id_user": id_user,
                    "id_mongo_song": id_mongo_song
                })

            return True
        except Exception as e:
            logging.error(f"update_cant_history error: {e}")
            return False

    @staticmethod
    async def get_history_by_user( user_id):
        try:
            query = """
                SELECT h.*
                FROM Bounsic_History h
                INNER JOIN Bounsic_Users u ON h.user_id = u.id_user
                WHERE u.email = :email
            """
            # Pasamos el email como parámetro
            values = {'email': email}

            # Ejecutamos la consulta
            return await MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            logging.error(f"get_history_by_user error: {e}")
            return None

    @staticmethod
    async def insert_history( data):
        try:
            query = "INSERT INTO Bounsic_History (user_id, history_mongo_id) VALUES (%s, %s)"
            values = (data["user_id"], data["history_mongo_id"])
            return await MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            logging.error(f"insert_history error: {e}")
            return False

    @staticmethod
    async def update_history( history_id, data):
        try:
            query = "UPDATE Bounsic_History SET user_id=%s, history_mongo_id=%s WHERE history_id=%s"
            values = (data["user_id"], data["history_mongo_id"], history_id)
            return await MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            logging.error(f"update_history error: {e}")
            return False

    @staticmethod
    async def delete_history( history_id):
        try:
            return await MySQLSongService._db.execute_query("DELETE FROM Bounsic_History WHERE history_id = %s", (history_id,))
        except Exception as e:
            logging.error(f"delete_history error: {e}")
            return False
        


    # PLAYLIST
    @staticmethod
    async def get_all_playlists():
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Playlist")
        except Exception as e:
            logging.error(f"get_all_playlists error: {e}")
            return None

    @staticmethod
    async def get_playlist_by_id(playlist_id):
        try:
            query = "SELECT * FROM Bounsic_Playlist WHERE playlist_id = :playlist_id"
            params = {"playlist_id": playlist_id}
            return await MySQLSongService._db.execute_query(query, params)
        except Exception as e:
            logging.error(f"get_playlist_by_id error: {e}")
            return None


    @staticmethod
    async def get_playlists_by_user( user_id):
        try:
            query = """
                    SELECT p.*
                    FROM Bounsic_Playlist p
                    JOIN Bounsic_User_Playlists up ON p.playlist_id = up.playlist_id
                    WHERE up.user_id = :user_id;
            """
            return await MySQLSongService._db.execute_query(query, {"user_id":user_id})
        except Exception as e:
            logging.error(f"get_playlists_by_user error: {e}")
            return None

    @staticmethod
    async def insert_playlist(data):
        try:
            query = """
            INSERT INTO Bounsic_Playlist (plist_name, playlist_desc, playlist_mongo_id)
            VALUES (:p1, :p2, :p3)
            """
            values = {
                "p1": data["plist_name"],
                "p2": data.get("playlist_desc"),
                "p3": data["playlist_mongo_id"]
            }

            result = await MySQLSongService._db.execute_query(query, values)

            if "user_id" in data and result:
                last_id_result = await MySQLSongService._db.execute_query("SELECT LAST_INSERT_ID() AS id")
                playlist_id = last_id_result[0]["id"]
                print(playlist_id)

                await MySQLSongService._db.execute_query(
                    """
                    INSERT INTO Bounsic_User_Playlists (user_id, playlist_id)
                    VALUES (:user_id, :playlist_id)
                    """,
                    {"user_id": data["user_id"], "playlist_id": playlist_id}
                )

            return result
        except Exception as e:
            logging.error(f"insert_playlist error: {e}")
            return False

           


    @staticmethod
    async def update_playlist( playlist_id, data):
        try:
            query = "UPDATE Bounsic_Playlist SET plist_name=%s, playlist_desc=%s, playlist_mongo_id=%s WHERE playlist_id=%s"
            values = (data["plist_name"], data.get("playlist_desc"), data["playlist_mongo_id"], playlist_id)
            return await MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            logging.error(f"update_playlist error: {e}")
            return False

    @staticmethod
    async def delete_playlist(playlist_id):
        try:
            query = "DELETE FROM Bounsic_Playlist WHERE playlist_id = :playlist_id"
            params = {"playlist_id": playlist_id}
            return await MySQLSongService._db.execute_query(query, params)
        except Exception as e:
            logging.error(f"delete_playlist error: {e}")
            return False

    # LIKE
    @staticmethod
    async def get_all_likes():
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Like")
        except Exception as e:
            logging.error(f"get_all_likes error: {e}")
            return None

    @staticmethod
    async def get_like_by_id( like_id):
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Like WHERE like_id = %s", (like_id,))
        except Exception as e:
            logging.error(f"get_like_by_id error: {e}")
            return None

    @staticmethod
    async def get_likes_by_user( user_id):
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Like WHERE user_id = :user_id", {"user_id":user_id})
        except Exception as e:
            logging.error(f"get_likes_by_user error: {e}")
            return None
        
    @staticmethod
    async def get_likes_by_user_count(user_id):
        try:
            result = await MySQLSongService._db.execute_query(
                "SELECT COUNT(*) as like_count FROM Bounsic_Like WHERE user_id = :user_id", 
                {"user_id": user_id}
            )
            return result[0]["like_count"] if result else 0
        except Exception as e:
            logging.error(f"get_likes_by_user error: {e}")
            return 0


    @staticmethod
    async def check_like_by_user( user_id , song_id):
        try:
            return await MySQLSongService._db.execute_query("SELECT * FROM Bounsic_Like WHERE user_id = :user_id AND song_mongo_id = :song_mongo_id", {"user_id":user_id ,"song_mongo_id":song_id })
        except Exception as e:
            logging.error(f"get_likes_by_user error: {e}")
            return None

    @staticmethod
    async def insert_like(user_id , song_id):
        try:
            query = """
                INSERT INTO Bounsic_Like (user_id, song_mongo_id)
                VALUES (:user_id, :song_mongo_id)
            """
            return await MySQLSongService._db.execute_query(query, {
                "user_id": user_id,
                "song_mongo_id": song_id
            })
        except Exception as e:
            logging.error(f"insert_like error: {e}")
            return False

    @staticmethod
    async def update_like( like_id, data):
        try:
            query = "UPDATE Bounsic_Like SET user_id=%s, song_mongo_id=%s WHERE like_id=%s"
            values = (data["user_id"], data["song_mongo_id"], like_id)
            return await MySQLSongService._db.execute_query(query, values)
        except Exception as e:
            logging.error(f"update_like error: {e}")
            return False

    @staticmethod
    async def delete_like( user_id,song_id):
        try:
            return await MySQLSongService._db.execute_query("DELETE FROM Bounsic_Like WHERE user_id = :user_id AND song_mongo_id = :song_mongo_id", {"user_id":user_id ,"song_mongo_id":song_id })
        except Exception as e:
            logging.error(f"delete_like error: {e}")
            return False

    # recomendations
    @staticmethod
    async def get_random_likes(user_id: int, number: int):
        # Return (number) random song_id in likes of user (user_id)
        try:
            query = "SELECT song_mongo_id FROM Bounsic_Like WHERE user_id = :user_id ORDER BY RAND() LIMIT :number"
            return await MySQLSongService._db.execute_query(query, ({"user_id": user_id, "number": number}))
        except Exception as e:
            logging.error(f"get_like error: {e}")
            return False
        
    @staticmethod
    async def get_safe_choices(email: str):
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
                    bh.user_id = (SELECT user_id FROM Bounsic_Users WHERE email = :email)
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
                    WHERE bh2.user_id = (SELECT user_id FROM Bounsic_Users WHERE email = :email)
                    ORDER BY bh2.cant_repro DESC
                    LIMIT 6
                ) AS top_songs
                ON bl.song_mongo_id = top_songs.song_mongo_id
                WHERE 
                    bl.user_id = (SELECT user_id FROM Bounsic_Users WHERE email = :email) AND 
                    top_songs.song_mongo_id IS NULL
                ORDER BY RAND()
                LIMIT 6
            )
            """
            return await MySQLSongService._db.execute_query(query, {"email": email})
        except Exception as e:
            logging.error(f"Error in get_safe_choices_by_email: {e}")
            return []
        
    @staticmethod
    async def get_likes_by_user_email( email):
        try:
            query = """
            SELECT Bounsic_Like.*, Bounsic_Users.email, Bounsic_Users.username
            FROM Bounsic_Like
            JOIN Bounsic_Users ON Bounsic_Like.user_id = Bounsic_Users.id_user
            WHERE Bounsic_Users.email = :email
            """
            return await MySQLSongService._db.execute_query(query, {"email": email})
        except Exception as e:
            logging.error(f"get_lsafe_choices error: {e}")
            return None
        
    @staticmethod
    async def get_history_month(email):
        try:
            query = """
                SELECT 
                    song_mongo_id,
                    last_listened,
                    cant_repro
                FROM (
                    SELECT h.song_mongo_id, h.last_listened, h.cant_repro
                    FROM Bounsic_Users u
                    JOIN Bounsic_History h ON u.id_user = h.user_id
                    WHERE u.email = :email
                    ORDER BY h.last_listened DESC
                    LIMIT 12
                ) AS ultimas
                ORDER BY RAND();
            """
            return await MySQLSongService._db.execute_query(query, {"email": email})
        except Exception as e:
            logging.error(f"get_history_month error: {e}")
            return None

    @staticmethod
    async def get_full_user_by_email( email):
        try:
            query = """ 
                    SELECT 
                        u.id_user,
                        u.username,
                        u.name,
                        u.email,
                        u.country,
                        u.phone,
                        r.name_rol AS role,
                        u.profile_img,
                        p.background,
                        p.typography,
                        p.language,
                        p.theme
                    FROM 
                        Bounsic_Users u
                    INNER JOIN 
                        Bounsic_Role r ON u.rol_user = r.id_rol
                    LEFT JOIN 
                        Bounsic_Preferences p ON u.id_user = p.user_id
                    WHERE 
                        u.email = :email;
            """
            return await MySQLSongService._db.execute_query(query, {"email": email})
        except Exception as e:
            print.error(f"get_full_user_by_email error: {e}")
            return None
        
    async def get_most_played_songs(user_id, size):
        try:
            query = """SELECT bh.song_mongo_id, bh.cant_repro AS play_count 
                    FROM Bounsic_History bh 
                    WHERE bh.user_id = :id ORDER BY  bh.cant_repro DESC LIMIT :size"""
            return await MySQLSongService._db.execute_query(query, ({"id": user_id, "size": size}))
        except Exception as e:
            logging.error(f"get_most_played_songs error: {e}")
            return False

