from db.repository import GenericRepository
from typing import Tuple, Dict, Optional

class ApoderadoService:
    def __init__(self):
        self.repo = GenericRepository("Apoderado")

    def crear(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_insert_Apoderado", data)

    def modificar(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_update_Apoderado", data)

    def eliminar(self, dni: str, dni_ce: str) -> bool:
        return self.repo.call_procedure("sp_delete_Apoderado", (dni, dni_ce))

    def listar(self):
        return self.repo.query_procedure("sp_list_Apoderado")

    def get_by_pk(self, dni: str, dni_ce: str) -> Optional[Dict]:
        rows = self.repo.query_procedure("sp_get_Apoderado", (dni, dni_ce))
        return rows[0] if rows else None
