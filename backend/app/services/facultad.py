from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.facultad import Facultad
from app.repositories.facultad import FacultadRepository
from app.schemas.facultad import FacultadCreate, FacultadUpdate


class FacultadService:
    def __init__(self, db: Session):
        self.repo = FacultadRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[Facultad]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, facultad_id: int) -> Facultad:
        facultad = self.repo.get_by_id(facultad_id)
        if not facultad:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Facultad con ID {facultad_id} no encontrada",
            )
        return facultad

    def crear(self, data: FacultadCreate) -> Facultad:
        # Validar nombre único
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una facultad con el nombre '{data.nombre}'",
            )
        # Validar correo único
        if data.correo and self.repo.get_by_correo(data.correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una facultad con el correo '{data.correo}'",
            )
        return self.repo.create(data.model_dump())

    def actualizar(self, facultad_id: int, data: FacultadUpdate) -> Facultad:
        facultad = self.obtener(facultad_id)
        update_data = data.model_dump(exclude_none=True)

        if "nombre" in update_data:
            existente = self.repo.get_by_nombre(update_data["nombre"])
            if existente and existente.id != facultad_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una facultad con el nombre '{update_data['nombre']}'",
                )

        return self.repo.update(facultad, update_data)

    def eliminar(self, facultad_id: int) -> bool:
        facultad = self.obtener(facultad_id)
        return self.repo.delete(facultad)
