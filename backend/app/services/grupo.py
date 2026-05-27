from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.grupo import Grupo
from app.repositories.grupo import GrupoRepository
from app.repositories.asignatura import AsignaturaRepository
from app.repositories.docente import DocenteRepository
from app.schemas.grupo import GrupoCreate, GrupoUpdate


class GrupoService:
    def __init__(self, db: Session):
        self.repo = GrupoRepository(db)
        self.asignatura_repo = AsignaturaRepository(db)
        self.docente_repo = DocenteRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[Grupo]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, grupo_id: int) -> Grupo:
        grupo = self.repo.get_by_id(grupo_id)
        if not grupo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupo con ID {grupo_id} no encontrado",
            )
        return grupo

    def crear(self, data: GrupoCreate) -> Grupo:
        # Validar asignatura existe y está activa
        asignatura = self.asignatura_repo.get_by_id(data.asignatura_id)
        if not asignatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Asignatura con ID {data.asignatura_id} no encontrada",
            )
        if asignatura.estado != "activa":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede crear un grupo para una asignatura inactiva",
            )
        # Validar docente existe y está activo
        docente = self.docente_repo.get_by_id(data.docente_id)
        if not docente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Docente con ID {data.docente_id} no encontrado",
            )
        if docente.estado != "activo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede asignar un docente inactivo",
            )
        return self.repo.create(data.model_dump())

    def actualizar(self, grupo_id: int, data: GrupoUpdate) -> Grupo:
        grupo = self.obtener(grupo_id)
        update_data = data.model_dump(exclude_none=True)

        # Si se reduce el cupo, verificar que no quede por debajo de matriculados
        if "cupo_maximo" in update_data:
            matriculados = self.repo.contar_matriculados(grupo_id)
            if update_data["cupo_maximo"] < matriculados:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No se puede reducir el cupo a {update_data['cupo_maximo']}: "
                           f"hay {matriculados} estudiantes matriculados",
                )

        return self.repo.update(grupo, update_data)

    def eliminar(self, grupo_id: int) -> bool:
        grupo = self.obtener(grupo_id)
        return self.repo.delete(grupo)

    def obtener_matriculados(self, grupo_id: int) -> int:
        self.obtener(grupo_id)  # Valida que exista
        return self.repo.contar_matriculados(grupo_id)
