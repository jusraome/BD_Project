from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.asignatura import Asignatura
from app.repositories.asignatura import AsignaturaRepository
from app.repositories.programa import ProgramaRepository
from app.schemas.asignatura import AsignaturaCreate, AsignaturaUpdate


class AsignaturaService:
    def __init__(self, db: Session):
        self.repo = AsignaturaRepository(db)
        self.programa_repo = ProgramaRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[Asignatura]:
        return self.repo.get_all(skip=skip, limit=limit)

    def listar_por_programa(self, programa_id: int) -> List[Asignatura]:
        return self.repo.get_by_programa(programa_id)

    def obtener(self, asignatura_id: int) -> Asignatura:
        asignatura = self.repo.get_by_id(asignatura_id)
        if not asignatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignatura con ID {asignatura_id} no encontrada",
            )
        return asignatura

    def crear(self, data: AsignaturaCreate) -> Asignatura:
        if not self.programa_repo.get_by_id(data.programa_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Programa con ID {data.programa_id} no encontrado",
            )
        if self.repo.get_by_codigo(data.codigo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una asignatura con el código '{data.codigo}'",
            )
        return self.repo.create(data.model_dump())

    def actualizar(self, asignatura_id: int, data: AsignaturaUpdate) -> Asignatura:
        asignatura = self.obtener(asignatura_id)
        return self.repo.update(asignatura, data.model_dump(exclude_none=True))

    def eliminar(self, asignatura_id: int) -> bool:
        asignatura = self.obtener(asignatura_id)
        return self.repo.delete(asignatura)
