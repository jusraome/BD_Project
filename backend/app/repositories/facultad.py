from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.facultad import Facultad
from app.repositories.base import BaseRepository


class FacultadRepository(BaseRepository[Facultad]):
    def __init__(self, db: Session):
        super().__init__(Facultad, db)

    def get_by_nombre(self, nombre: str) -> Optional[Facultad]:
        return self.db.execute(
            select(Facultad).where(Facultad.nombre == nombre)
        ).scalar_one_or_none()

    def get_by_correo(self, correo: str) -> Optional[Facultad]:
        return self.db.execute(
            select(Facultad).where(Facultad.correo == correo)
        ).scalar_one_or_none()

    def get_activas(self) -> List[Facultad]:
        return list(
            self.db.execute(
                select(Facultad).where(Facultad.estado == "activo")
            ).scalars().all()
        )
