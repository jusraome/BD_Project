from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.estudiante import Estudiante, EstadoEstudiante
from app.repositories.base import BaseRepository


class EstudianteRepository(BaseRepository[Estudiante]):
    def __init__(self, db: Session):
        super().__init__(Estudiante, db)

    def get_by_codigo(self, codigo: str) -> Optional[Estudiante]:
        return self.db.execute(
            select(Estudiante).where(Estudiante.codigo == codigo)
        ).scalar_one_or_none()

    def get_by_correo(self, correo: str) -> Optional[Estudiante]:
        return self.db.execute(
            select(Estudiante).where(Estudiante.correo == correo)
        ).scalar_one_or_none()

    def get_by_documento(self, numero_documento: str) -> Optional[Estudiante]:
        return self.db.execute(
            select(Estudiante).where(Estudiante.numero_documento == numero_documento)
        ).scalar_one_or_none()

    def get_by_programa(self, programa_id: int, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        return list(
            self.db.execute(
                select(Estudiante)
                .where(Estudiante.programa_id == programa_id)
                .offset(skip).limit(limit)
            ).scalars().all()
        )

    def get_activos(self, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        return list(
            self.db.execute(
                select(Estudiante)
                .where(Estudiante.estado == EstadoEstudiante.ACTIVO)
                .offset(skip).limit(limit)
            ).scalars().all()
        )

    def buscar(self, query: str, skip: int = 0, limit: int = 50) -> List[Estudiante]:
        """Búsqueda por nombre, apellido o código."""
        like_q = f"%{query}%"
        return list(
            self.db.execute(
                select(Estudiante).where(
                    (Estudiante.nombres.ilike(like_q)) |
                    (Estudiante.apellidos.ilike(like_q)) |
                    (Estudiante.codigo.ilike(like_q))
                ).offset(skip).limit(limit)
            ).scalars().all()
        )
