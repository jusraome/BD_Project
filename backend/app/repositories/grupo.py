from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.grupo import Grupo, EstadoGrupo
from app.models.matricula import Matricula, EstadoMatricula
from app.repositories.base import BaseRepository


class GrupoRepository(BaseRepository[Grupo]):
    def __init__(self, db: Session):
        super().__init__(Grupo, db)

    def get_by_asignatura(self, asignatura_id: int) -> List[Grupo]:
        return list(
            self.db.execute(
                select(Grupo).where(Grupo.asignatura_id == asignatura_id)
            ).scalars().all()
        )

    def get_by_docente(self, docente_id: int) -> List[Grupo]:
        return list(
            self.db.execute(
                select(Grupo).where(Grupo.docente_id == docente_id)
            ).scalars().all()
        )

    def get_by_periodo(self, periodo: str) -> List[Grupo]:
        return list(
            self.db.execute(
                select(Grupo).where(Grupo.periodo == periodo, Grupo.estado == EstadoGrupo.ACTIVO)
            ).scalars().all()
        )

    def contar_matriculados(self, grupo_id: int) -> int:
        """Cuenta las matrículas activas en un grupo."""
        return self.db.execute(
            select(func.count()).select_from(Matricula).where(
                Matricula.grupo_id == grupo_id,
                Matricula.estado == EstadoMatricula.ACTIVA,
            )
        ).scalar_one()

    def hay_cupo(self, grupo_id: int) -> bool:
        """Verifica si hay cupo disponible en el grupo."""
        grupo = self.get_by_id(grupo_id)
        if not grupo:
            return False
        matriculados = self.contar_matriculados(grupo_id)
        return matriculados < grupo.cupo_maximo
