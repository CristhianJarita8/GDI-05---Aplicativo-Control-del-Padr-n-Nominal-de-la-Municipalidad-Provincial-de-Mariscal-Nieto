from db.repository import GenericRepository
from typing import Tuple, List, Dict, Optional

class FichaVisitaService:
    def __init__(self):
        self.repo = GenericRepository("Ficha_Visita")

    def crear(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_insert_Ficha_Visita", data)

    def modificar(self, data: Tuple) -> bool:
        return self.repo.call_procedure("sp_update_Ficha_Visita", data)

    def eliminar(self, id_visita: int) -> bool:
        return self.repo.call_procedure("sp_delete_Ficha_Visita", (id_visita,))

    def listar(self):
        return self.repo.query_procedure("sp_list_Ficha_Visita")

    def get_by_pk(self, id_visita: int) -> Optional[Dict]:
        rows = self.repo.query_procedure("sp_get_Ficha_Visita", (id_visita,))
        return rows[0] if rows else None
