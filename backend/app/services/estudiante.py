from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.estudiante import Estudiante
from app.repositories.estudiante import EstudianteRepository
from app.repositories.programa import ProgramaRepository
from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate


class EstudianteService:
    def __init__(self, db: Session):
        self.repo = EstudianteRepository(db)
        self.programa_repo = ProgramaRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[Estudiante]:
        return self.repo.get_all(skip=skip, limit=limit)

    def buscar(self, query: str) -> List[Estudiante]:
        return self.repo.buscar(query)

    def obtener(self, estudiante_id: int) -> Estudiante:
        estudiante = self.repo.get_by_id(estudiante_id)
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {estudiante_id} no encontrado",
            )
        return estudiante

    def crear(self, data: EstudianteCreate) -> Estudiante:
        # Validar que el programa exista y esté activo
        programa = self.programa_repo.get_by_id(data.programa_id)
        if not programa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Programa con ID {data.programa_id} no encontrado",
            )
        if programa.estado != "activo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede matricular en un programa inactivo",
            )
        # Validar código único
        if self.repo.get_by_codigo(data.codigo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un estudiante con el código '{data.codigo}'",
            )
        # Validar correo único
        if self.repo.get_by_correo(data.correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un estudiante con el correo '{data.correo}'",
            )
        # Validar documento único
        if self.repo.get_by_documento(data.numero_documento):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un estudiante con ese número de documento",
            )
        return self.repo.create(data.model_dump())

    def actualizar(self, estudiante_id: int, data: EstudianteUpdate) -> Estudiante:
        estudiante = self.obtener(estudiante_id)
        update_data = data.model_dump(exclude_none=True)

        if "correo" in update_data:
            existente = self.repo.get_by_correo(update_data["correo"])
            if existente and existente.id != estudiante_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ya existe un estudiante con ese correo",
                )

        return self.repo.update(estudiante, update_data)

    def eliminar(self, estudiante_id: int) -> bool:
        estudiante = self.obtener(estudiante_id)
        return self.repo.delete(estudiante)
