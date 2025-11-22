from db.repository import GenericRepository
from typing import Tuple, List, Dict, Optional

class HomologacionService:
    def __init__(self):
        self.repo = GenericRepository("Homologacion_Nominal")

    def crear(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_insert_Homologacion_Nominal", data)

    def modificar(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_update_Homologacion_Nominal", data)

    def eliminar(self, id_h: str) -> bool:
        return self.repo.call_procedure("sp_delete_Homologacion_Nominal", (id_h,))

    def listar(self):
        return self.repo.query_procedure("sp_list_Homologacion_Nominal")

    def get_by_pk(self, id_h: str) -> Optional[Dict]:
        rows = self.repo.query_procedure("sp_get_Homologacion_Nominal", (id_h,))
        return rows[0] if rows else None
