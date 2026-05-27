from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.matricula import Matricula, EstadoMatricula
from app.repositories.base import BaseRepository


class MatriculaRepository(BaseRepository[Matricula]):
    def __init__(self, db: Session):
        super().__init__(Matricula, db)

    def get_by_estudiante(self, estudiante_id: int) -> List[Matricula]:
        return list(
            self.db.execute(
                select(Matricula).where(Matricula.estudiante_id == estudiante_id)
            ).scalars().all()
        )

    def get_by_grupo(self, grupo_id: int) -> List[Matricula]:
        return list(
            self.db.execute(
                select(Matricula).where(Matricula.grupo_id == grupo_id)
            ).scalars().all()
        )

    def get_by_estudiante_y_grupo(
        self, estudiante_id: int, grupo_id: int
    ) -> Optional[Matricula]:
        return self.db.execute(
            select(Matricula).where(
                Matricula.estudiante_id == estudiante_id,
                Matricula.grupo_id == grupo_id,
            )
        ).scalar_one_or_none()

    def get_activas_por_estudiante(self, estudiante_id: int) -> List[Matricula]:
        return list(
            self.db.execute(
                select(Matricula).where(
                    Matricula.estudiante_id == estudiante_id,
                    Matricula.estado == EstadoMatricula.ACTIVA,
                )
            ).scalars().all()
        )
