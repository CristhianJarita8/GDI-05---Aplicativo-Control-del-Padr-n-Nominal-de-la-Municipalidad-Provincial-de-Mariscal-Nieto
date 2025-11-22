from db.repository import GenericRepository
from typing import Tuple, List, Dict, Optional

class PadronNominalService:
    def __init__(self):
        self.repo = GenericRepository("Padron_Nominal")

    def crear(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_insert_Padron_Nominal", data)

    def modificar(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_update_Padron_Nominal", data)

    def eliminar(self, codigo: str) -> bool:
        return self.repo.call_procedure("sp_delete_Padron_Nominal", (codigo,))

    def listar(self):
        return self.repo.query_procedure("sp_list_Padron_Nominal")

    def get_by_pk(self, codigo: str) -> Optional[Dict]:
        rows = self.repo.query_procedure("sp_get_Padron_Nominal", (codigo,))
        return rows[0] if rows else None
