from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.nota import Nota, EstadoAprobacion
from app.repositories.base import BaseRepository


class NotaRepository(BaseRepository[Nota]):
    def __init__(self, db: Session):
        super().__init__(Nota, db)

    def get_by_matricula(self, matricula_id: int) -> Optional[Nota]:
        return self.db.execute(
            select(Nota).where(Nota.matricula_id == matricula_id)
        ).scalar_one_or_none()

    def get_reprobados_por_grupo(self, grupo_id: int) -> List[Nota]:
        """Notas reprobadas en un grupo específico."""
        from app.models.matricula import Matricula
        return list(
            self.db.execute(
                select(Nota)
                .join(Matricula, Nota.matricula_id == Matricula.id)
                .where(
                    Matricula.grupo_id == grupo_id,
                    Nota.estado_aprobacion == EstadoAprobacion.REPROBADO,
                )
            ).scalars().all()
        )
