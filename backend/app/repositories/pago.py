from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.pago import PagoMatricula, EstadoPago
from app.repositories.base import BaseRepository


class PagoRepository(BaseRepository[PagoMatricula]):
    def __init__(self, db: Session):
        super().__init__(PagoMatricula, db)

    def get_by_estudiante(self, estudiante_id: int) -> List[PagoMatricula]:
        return list(
            self.db.execute(
                select(PagoMatricula).where(PagoMatricula.estudiante_id == estudiante_id)
            ).scalars().all()
        )

    def get_by_periodo(self, periodo: str) -> List[PagoMatricula]:
        return list(
            self.db.execute(
                select(PagoMatricula).where(PagoMatricula.periodo == periodo)
            ).scalars().all()
        )

    def get_pendientes(self, skip: int = 0, limit: int = 100) -> List[PagoMatricula]:
        return list(
            self.db.execute(
                select(PagoMatricula)
                .where(PagoMatricula.estado_pago.in_([EstadoPago.PENDIENTE, EstadoPago.EN_MORA]))
                .offset(skip).limit(limit)
            ).scalars().all()
        )

    def get_by_estudiante_y_periodo(
        self, estudiante_id: int, periodo: str
    ) -> Optional[PagoMatricula]:
        return self.db.execute(
            select(PagoMatricula).where(
                PagoMatricula.estudiante_id == estudiante_id,
                PagoMatricula.periodo == periodo,
            )
        ).scalar_one_or_none()
