from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.programa import ProgramaAcademico
from app.repositories.programa import ProgramaRepository
from app.repositories.facultad import FacultadRepository
from app.schemas.programa import ProgramaCreate, ProgramaUpdate


class ProgramaService:
    def __init__(self, db: Session):
        self.repo = ProgramaRepository(db)
        self.facultad_repo = FacultadRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[ProgramaAcademico]:
        return self.repo.get_all(skip=skip, limit=limit)

    def listar_por_facultad(self, facultad_id: int) -> List[ProgramaAcademico]:
        return self.repo.get_by_facultad(facultad_id)

    def obtener(self, programa_id: int) -> ProgramaAcademico:
        programa = self.repo.get_by_id(programa_id)
        if not programa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Programa con ID {programa_id} no encontrado",
            )
        return programa

    def crear(self, data: ProgramaCreate) -> ProgramaAcademico:
        # Validar que la facultad exista
        if not self.facultad_repo.get_by_id(data.facultad_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Facultad con ID {data.facultad_id} no encontrada",
            )
        # Validar nombre único en la misma facultad
        if self.repo.get_by_nombre_y_facultad(data.nombre, data.facultad_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un programa con ese nombre en la facultad indicada",
            )
        return self.repo.create(data.model_dump())

    def actualizar(self, programa_id: int, data: ProgramaUpdate) -> ProgramaAcademico:
        programa = self.obtener(programa_id)
        return self.repo.update(programa, data.model_dump(exclude_none=True))

    def eliminar(self, programa_id: int) -> bool:
        programa = self.obtener(programa_id)
        return self.repo.delete(programa)
