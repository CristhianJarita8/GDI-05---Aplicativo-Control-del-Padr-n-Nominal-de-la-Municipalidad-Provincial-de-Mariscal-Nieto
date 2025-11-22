from db.repository import GenericRepository
from typing import Tuple, Dict, Optional

class RepresentanteMunicipalService:
    def __init__(self):
        self.repo = GenericRepository("Representante_Municipal")

    def crear(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_insert_Representante_Municipal", data)

    def modificar(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_update_Representante_Municipal", data)

    def eliminar(self, dni: str, id_h: str) -> bool:
        return self.repo.call_procedure("sp_delete_Representante_Municipal", (dni, id_h))

    def listar(self):
        return self.repo.query_procedure("sp_list_Representante_Municipal")

    def get_by_pk(self, dni: str, id_h: str) -> Optional[Dict]:
        rows = self.repo.query_procedure("sp_get_Representante_Municipal", (dni, id_h))
        return rows[0] if rows else None
