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
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, params)
                
                # Determinar el tipo de consulta
                query_type = query.strip().upper().split()[0]
                
                if query_type == "SELECT":
                    # Para consultas SELECT, devolver los resultados
                    result = cursor.fetchall()
                    return result
                elif query_type == "INSERT":
                    # Para INSERT, hacer commit y devolver información incluyendo el último ID
                    connection.commit()
                    return {
                        "rowcount": cursor.rowcount,
                        "lastrowid": cursor.lastrowid
                    }
                else:
                    # Para UPDATE, DELETE, hacer commit y devolver filas afectadas
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

