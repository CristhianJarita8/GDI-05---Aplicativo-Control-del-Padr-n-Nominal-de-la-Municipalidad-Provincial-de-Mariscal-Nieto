from db.repository import GenericRepository
from typing import Tuple, List, Dict, Optional

class InfanteService:
    def __init__(self):
        self.repo = GenericRepository("Infante")

    def crear(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_insert_Infante", data)

    def modificar(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_update_Infante", data)

    def eliminar(self, dni_ce: str, codigo_padron: str) -> bool:
        return self.repo.call_procedure("sp_delete_Infante", (dni_ce, codigo_padron))

    def listar(self) -> List[Dict]:
        return self.repo.query_procedure("sp_list_Infante")

    def get_by_pk(self, dni_ce: str, codigo_padron: str) -> Optional[Dict]:
        rows = self.repo.query_procedure("sp_get_Infante", (dni_ce, codigo_padron))
        return rows[0] if rows else None
