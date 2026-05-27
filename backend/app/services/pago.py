from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.pago import PagoMatricula, EstadoPago
from app.repositories.pago import PagoRepository
from app.repositories.estudiante import EstudianteRepository
from app.schemas.pago import PagoCreate, PagoUpdate


class PagoService:
    def __init__(self, db: Session):
        self.repo = PagoRepository(db)
        self.estudiante_repo = EstudianteRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[PagoMatricula]:
        return self.repo.get_all(skip=skip, limit=limit)

    def listar_pendientes(self, skip: int = 0, limit: int = 100) -> List[PagoMatricula]:
        return self.repo.get_pendientes(skip=skip, limit=limit)

    def listar_por_estudiante(self, estudiante_id: int) -> List[PagoMatricula]:
        return self.repo.get_by_estudiante(estudiante_id)

    def obtener(self, pago_id: int) -> PagoMatricula:
        pago = self.repo.get_by_id(pago_id)
        if not pago:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pago con ID {pago_id} no encontrado",
            )
        return pago

    def crear(self, data: PagoCreate) -> PagoMatricula:
        # Validar que el estudiante exista
        estudiante = self.estudiante_repo.get_by_id(data.estudiante_id)
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {data.estudiante_id} no encontrado",
            )

        pago_data = data.model_dump()
        # Si el estado es PAGADO, registrar fecha de pago
        if data.estado_pago == EstadoPago.PAGADO and not pago_data.get("fecha_pago"):
            pago_data["fecha_pago"] = datetime.utcnow()

        return self.repo.create(pago_data)

    def registrar_pago(self, pago_id: int, data: PagoUpdate) -> PagoMatricula:
        """Marca un pago como pagado y registra el medio de pago."""
        pago = self.obtener(pago_id)

        if pago.estado_pago == EstadoPago.ANULADO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede actualizar un pago anulado",
            )

        update_data = data.model_dump(exclude_none=True)

        if data.estado_pago == EstadoPago.PAGADO and not pago.fecha_pago:
            update_data["fecha_pago"] = datetime.utcnow()

        return self.repo.update(pago, update_data)

    def eliminar(self, pago_id: int) -> bool:
        pago = self.obtener(pago_id)
        return self.repo.delete(pago)
