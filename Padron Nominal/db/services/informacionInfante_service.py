from db.repository import GenericRepository
from typing import Tuple, Dict, Optional

class InformacionInfanteService:
    def __init__(self):
        self.repo = GenericRepository("Informacion_Infante")

    def crear(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_insert_Informacion_Infante", data)

    def modificar(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_update_Informacion_Infante", data)

    def eliminar(self, dni: str, id_s: str) -> bool:
        return self.repo.call_procedure("sp_delete_Informacion_Infante", (dni, id_s))

    def listar(self):
        return self.repo.query_procedure("sp_list_Informacion_Infante")

    def get_by_pk(self, dni: str, id_s: str) -> Optional[Dict]:
        rows = self.repo.query_procedure("sp_get_Informacion_Infante", (dni, id_s))
        return rows[0] if rows else None
