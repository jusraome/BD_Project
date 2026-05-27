from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.docente import Docente
from app.repositories.docente import DocenteRepository
from app.repositories.facultad import FacultadRepository
from app.schemas.docente import DocenteCreate, DocenteUpdate


class DocenteService:
    def __init__(self, db: Session):
        self.repo = DocenteRepository(db)
        self.facultad_repo = FacultadRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[Docente]:
        return self.repo.get_all(skip=skip, limit=limit)

    def buscar(self, query: str) -> List[Docente]:
        return self.repo.buscar(query)

    def obtener(self, docente_id: int) -> Docente:
        docente = self.repo.get_by_id(docente_id)
        if not docente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Docente con ID {docente_id} no encontrado",
            )
        return docente

    def crear(self, data: DocenteCreate) -> Docente:
        if not self.facultad_repo.get_by_id(data.facultad_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Facultad con ID {data.facultad_id} no encontrada",
            )
        if self.repo.get_by_correo(data.correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un docente con el correo '{data.correo}'",
            )
        return self.repo.create(data.model_dump())

    def actualizar(self, docente_id: int, data: DocenteUpdate) -> Docente:
        docente = self.obtener(docente_id)
        update_data = data.model_dump(exclude_none=True)

        if "correo" in update_data:
            existente = self.repo.get_by_correo(update_data["correo"])
            if existente and existente.id != docente_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ya existe un docente con ese correo",
                )

        return self.repo.update(docente, update_data)

    def eliminar(self, docente_id: int) -> bool:
        docente = self.obtener(docente_id)
        return self.repo.delete(docente)
