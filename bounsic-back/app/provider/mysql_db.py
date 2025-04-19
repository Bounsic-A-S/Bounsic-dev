import os
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector.pooling

class DatabaseFacade:
    _pool = None

    def __init__(self, config_path="env/.env.dev"):
        self._load_config(config_path)
        self.conection()

    def _load_config(self, config_path):
        dotenv_path = Path(__file__).resolve().parent.parent.parent / config_path
        load_dotenv(dotenv_path=dotenv_path)
        self.db_config = {
            'host': os.environ.get('DB_HOST'),
            'user': os.environ.get('DB_USER'),
            'password': os.environ.get('DB_PASSWORD'),
            'database': os.environ.get('DB_NAME'),
            'port': int(os.environ.get('PORT_DB', 3306)), 
        }

        print({
            'host': self.db_config.get('host'),
            'user': self.db_config.get('user'),
            'password': self.db_config.get('password'),
            'database': self.db_config.get('database'),
            'port': self.db_config.get('port')
        })

    def conection(self):
        try:
            self._pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=10,
                **self.db_config
            )
            print("Database connection pool created.")
        except mysql.connector.Error as err:
            print(f"Error creating connection pool: {err}")
            self._pool = None

    def get_connection(self):
        if self._pool:
            try:
                return self._pool.get_connection()
            except mysql.connector.Error as err:
                print(f"Error getting connection from pool: {err}")
                return None
        else:
            print("Connection pool not initialized.")
            return None
    def release_connection(self, connection):
        if connection:
            connection.close()  # Para mysql.connector, close() devuelve la conexión al pool

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True, buffered=True)
            try:
                cursor.execute(query, params)

                # Detectar el tipo de consulta (mÃ¡s robusto)
                import re
                query_type_match = re.search(r'\b(SELECT|INSERT|UPDATE|DELETE)\b', query.strip(), re.IGNORECASE)
                query_type = query_type_match.group(1).upper() if query_type_match else ""

                if query_type == "SELECT":
                    result = cursor.fetchall()
                    return result
                elif query_type == "INSERT":
                    connection.commit()
                    return {
                        "rowcount": cursor.rowcount,
                        "lastrowid": cursor.lastrowid
                    }
                else:
                    connection.commit()
                    return {
                        "rowcount": cursor.rowcount
                    }

            except mysql.connector.Error as err:
                print(f"Error executing query: {err}")
                if connection.is_connected():
                    connection.rollback()
                return None
            finally:
                cursor.close()
                if connection.is_connected():
                    connection.close()
        return None

