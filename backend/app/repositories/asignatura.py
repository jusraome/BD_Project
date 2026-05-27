from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.asignatura import Asignatura, EstadoAsignatura
from app.repositories.base import BaseRepository


class AsignaturaRepository(BaseRepository[Asignatura]):
    def __init__(self, db: Session):
        super().__init__(Asignatura, db)

    def get_by_codigo(self, codigo: str) -> Optional[Asignatura]:
        return self.db.execute(
            select(Asignatura).where(Asignatura.codigo == codigo)
        ).scalar_one_or_none()

    def get_by_programa(self, programa_id: int) -> List[Asignatura]:
        return list(
            self.db.execute(
                select(Asignatura).where(Asignatura.programa_id == programa_id)
            ).scalars().all()
        )

    def get_activas(self) -> List[Asignatura]:
        return list(
            self.db.execute(
                select(Asignatura).where(Asignatura.estado == EstadoAsignatura.ACTIVA)
            ).scalars().all()
        )
