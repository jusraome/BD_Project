from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.matricula import Matricula, EstadoMatricula
from app.repositories.matricula import MatriculaRepository
from app.repositories.estudiante import EstudianteRepository
from app.repositories.grupo import GrupoRepository
from app.schemas.matricula import MatriculaCreate, MatriculaUpdate


class MatriculaService:
    def __init__(self, db: Session):
        self.repo = MatriculaRepository(db)
        self.estudiante_repo = EstudianteRepository(db)
        self.grupo_repo = GrupoRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[Matricula]:
        return self.repo.get_all(skip=skip, limit=limit)

    def listar_por_estudiante(self, estudiante_id: int) -> List[Matricula]:
        return self.repo.get_by_estudiante(estudiante_id)

    def listar_por_grupo(self, grupo_id: int) -> List[Matricula]:
        return self.repo.get_by_grupo(grupo_id)

    def obtener(self, matricula_id: int) -> Matricula:
        matricula = self.repo.get_by_id(matricula_id)
        if not matricula:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Matrícula con ID {matricula_id} no encontrada",
            )
        return matricula

    def crear(self, data: MatriculaCreate) -> Matricula:
        # Validar que el estudiante exista y esté activo
        estudiante = self.estudiante_repo.get_by_id(data.estudiante_id)
        if not estudiante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Estudiante con ID {data.estudiante_id} no encontrado",
            )
        if estudiante.estado != "activo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se pueden matricular estudiantes activos",
            )

        # Validar que el grupo exista y esté activo
        grupo = self.grupo_repo.get_by_id(data.grupo_id)
        if not grupo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Grupo con ID {data.grupo_id} no encontrado",
            )
        if grupo.estado != "activo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Solo se puede matricular en grupos activos",
            )

        # REGLA DE NEGOCIO: Verificar cupo disponible
        if not self.grupo_repo.hay_cupo(data.grupo_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El grupo no tiene cupo disponible "
                       f"(máximo: {grupo.cupo_maximo})",
            )

        # REGLA DE NEGOCIO: Verificar matrícula duplicada
        existente = self.repo.get_by_estudiante_y_grupo(data.estudiante_id, data.grupo_id)
        if existente and existente.estado == EstadoMatricula.ACTIVA:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El estudiante ya está matriculado en este grupo",
            )

        return self.repo.create(data.model_dump())

    def actualizar(self, matricula_id: int, data: MatriculaUpdate) -> Matricula:
        matricula = self.obtener(matricula_id)
        return self.repo.update(matricula, data.model_dump(exclude_none=True))

    def cancelar(self, matricula_id: int) -> Matricula:
        matricula = self.obtener(matricula_id)
        return self.repo.update(matricula, {"estado": EstadoMatricula.CANCELADA})
