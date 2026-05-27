from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.docente import Docente, EstadoDocente
from app.repositories.base import BaseRepository


class DocenteRepository(BaseRepository[Docente]):
    def __init__(self, db: Session):
        super().__init__(Docente, db)

    def get_by_correo(self, correo: str) -> Optional[Docente]:
        return self.db.execute(
            select(Docente).where(Docente.correo == correo)
        ).scalar_one_or_none()

    def get_by_facultad(self, facultad_id: int) -> List[Docente]:
        return list(
            self.db.execute(
                select(Docente).where(Docente.facultad_id == facultad_id)
            ).scalars().all()
        )

    def get_activos(self) -> List[Docente]:
        return list(
            self.db.execute(
                select(Docente).where(Docente.estado == EstadoDocente.ACTIVO)
            ).scalars().all()
        )

    def buscar(self, query: str, skip: int = 0, limit: int = 50) -> List[Docente]:
        like_q = f"%{query}%"
        return list(
            self.db.execute(
                select(Docente).where(
                    (Docente.nombres.ilike(like_q)) |
                    (Docente.apellidos.ilike(like_q))
                ).offset(skip).limit(limit)
            ).scalars().all()
        )
