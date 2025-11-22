import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "CrisDemon"
        self.database = "nominal_db"

    def get_connection(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except Error as e:
            print(f"Error al conectar: {e}")
            return None
