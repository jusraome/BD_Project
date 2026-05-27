from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_or_administrativo
from app.services.matricula import MatriculaService
from app.schemas.matricula import MatriculaCreate, MatriculaUpdate, MatriculaResponse, MatriculaList

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])


@router.get("/", response_model=List[MatriculaList])
def listar_matriculas(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return MatriculaService(db).listar(skip=skip, limit=limit)


@router.get("/estudiante/{estudiante_id}", response_model=List[MatriculaList])
def listar_por_estudiante(
    estudiante_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return MatriculaService(db).listar_por_estudiante(estudiante_id)


@router.get("/grupo/{grupo_id}", response_model=List[MatriculaList])
def listar_por_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return MatriculaService(db).listar_por_grupo(grupo_id)


@router.get("/{matricula_id}", response_model=MatriculaResponse)
def obtener_matricula(
    matricula_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return MatriculaService(db).obtener(matricula_id)


@router.post("/", response_model=MatriculaResponse, status_code=201)
def crear_matricula(
    data: MatriculaCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_administrativo),
):
    return MatriculaService(db).crear(data)


@router.put("/{matricula_id}", response_model=MatriculaResponse)
def actualizar_matricula(
    matricula_id: int,
    data: MatriculaUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_administrativo),
):
    return MatriculaService(db).actualizar(matricula_id, data)


@router.post("/{matricula_id}/cancelar", response_model=MatriculaResponse)
def cancelar_matricula(
    matricula_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_administrativo),
):
    return MatriculaService(db).cancelar(matricula_id)
