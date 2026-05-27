from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.nota import Nota, EstadoAprobacion
from app.repositories.nota import NotaRepository
from app.repositories.matricula import MatriculaRepository
from app.schemas.nota import NotaCreate, NotaUpdate


class NotaService:
    def __init__(self, db: Session):
        self.repo = NotaRepository(db)
        self.matricula_repo = MatriculaRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[Nota]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, nota_id: int) -> Nota:
        nota = self.repo.get_by_id(nota_id)
        if not nota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Nota con ID {nota_id} no encontrada",
            )
        return nota

    def obtener_por_matricula(self, matricula_id: int) -> Nota:
        nota = self.repo.get_by_matricula(matricula_id)
        if not nota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe nota para la matrícula {matricula_id}",
            )
        return nota

    def crear(self, data: NotaCreate) -> Nota:
        # Validar que la matrícula exista
        matricula = self.matricula_repo.get_by_id(data.matricula_id)
        if not matricula:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Matrícula con ID {data.matricula_id} no encontrada",
            )
        if matricula.estado != "activa":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden registrar notas en matrículas activas",
            )
        # Verificar que no exista ya una nota para esta matrícula
        if self.repo.get_by_matricula(data.matricula_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una nota para la matrícula {data.matricula_id}",
            )

        nota_data = data.model_dump()
        nota_data["nota_final"] = None
        nota_data["estado_aprobacion"] = EstadoAprobacion.PENDIENTE

        # Calcular nota final si todos los cortes están presentes
        nota_obj = Nota(**nota_data)
        nota_final = nota_obj.calcular_nota_final()
        if nota_final is not None:
            nota_data["nota_final"] = nota_final
            nota_data["estado_aprobacion"] = (
                EstadoAprobacion.APROBADO if nota_final >= 3.0
                else EstadoAprobacion.REPROBADO
            )

        return self.repo.create(nota_data)

    def actualizar(self, nota_id: int, data: NotaUpdate) -> Nota:
        nota = self.obtener(nota_id)
        update_data = data.model_dump(exclude_none=True)

        # Fusionar cortes actuales con los nuevos
        corte1 = update_data.get("corte1", nota.corte1)
        corte2 = update_data.get("corte2", nota.corte2)
        corte3 = update_data.get("corte3", nota.corte3)

        # Recalcular nota final
        if corte1 is not None and corte2 is not None and corte3 is not None:
            nota_final = round(float(corte1) * 0.30 + float(corte2) * 0.30 + float(corte3) * 0.40, 2)
            update_data["nota_final"] = nota_final
            update_data["estado_aprobacion"] = (
                EstadoAprobacion.APROBADO if nota_final >= 3.0
                else EstadoAprobacion.REPROBADO
            )
        else:
            update_data["estado_aprobacion"] = EstadoAprobacion.PENDIENTE

        return self.repo.update(nota, update_data)
