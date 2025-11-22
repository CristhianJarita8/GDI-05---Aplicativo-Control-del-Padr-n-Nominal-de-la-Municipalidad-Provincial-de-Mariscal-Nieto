from db.repository import GenericRepository
from typing import Tuple, Dict, Optional

class SeguimientoNominalService:
    def __init__(self):
        self.repo = GenericRepository("Seguimiento_Nominal")

    def crear(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_insert_Seguimiento_Nominal", data)

    def modificar(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_update_Seguimiento_Nominal", data)

    def eliminar(self, id_s: str) -> bool:
        return self.repo.call_procedure("sp_delete_Seguimiento_Nominal", (id_s,))

    def listar(self):
        return self.repo.query_procedure("sp_list_Seguimiento_Nominal")

    def get_by_pk(self, id_s: str) -> Optional[Dict]:
        rows = self.repo.query_procedure("sp_get_Seguimiento_Nominal", (id_s,))
        return rows[0] if rows else None
