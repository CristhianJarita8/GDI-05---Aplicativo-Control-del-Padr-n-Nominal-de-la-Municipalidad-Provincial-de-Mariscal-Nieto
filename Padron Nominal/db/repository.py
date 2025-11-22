# db/repository.py
from db.connection import DatabaseConnection
from mysql.connector import Error

class GenericRepository:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.db = DatabaseConnection()

    def call_procedure(self, procedure_name: str, params: tuple = ()):
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            cur.callproc(procedure_name, params)
            conn.commit()
            return True
        except Error as e:
            # Propagar la excepción para que la UI la maneje (mostrar mensaje amigable)
            raise
        finally:
            try:
                cur.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass

    def query_procedure(self, procedure_name: str, params: tuple = ()):
        """
        Ejecuta un procedure que retorna un result set. Devuelve una lista de dicts.
        """
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            cur.callproc(procedure_name, params)
            # cursor.stored_results() contiene los resultsets del procedure
            rows = []
            for result in cur.stored_results():
                cols = result.column_names
                for r in result.fetchall():
                    rows.append(dict(zip(cols, r)))
            return rows
        except Error as e:
            raise
        finally:
            try:
                cur.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass
