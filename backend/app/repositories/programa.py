from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.programa import ProgramaAcademico
from app.repositories.base import BaseRepository


class ProgramaRepository(BaseRepository[ProgramaAcademico]):
    def __init__(self, db: Session):
        super().__init__(ProgramaAcademico, db)

    def get_by_facultad(self, facultad_id: int) -> List[ProgramaAcademico]:
        return list(
            self.db.execute(
                select(ProgramaAcademico).where(ProgramaAcademico.facultad_id == facultad_id)
            ).scalars().all()
        )

    def get_activos(self) -> List[ProgramaAcademico]:
        return list(
            self.db.execute(
                select(ProgramaAcademico).where(ProgramaAcademico.estado == "activo")
            ).scalars().all()
        )

    def get_by_nombre_y_facultad(self, nombre: str, facultad_id: int) -> Optional[ProgramaAcademico]:
        return self.db.execute(
            select(ProgramaAcademico).where(
                ProgramaAcademico.nombre == nombre,
                ProgramaAcademico.facultad_id == facultad_id,
            )
        ).scalar_one_or_none()
