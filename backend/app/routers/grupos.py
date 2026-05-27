from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_or_coordinador
from app.services.grupo import GrupoService
from app.schemas.grupo import GrupoCreate, GrupoUpdate, GrupoResponse, GrupoList

router = APIRouter(prefix="/grupos", tags=["Grupos"])


@router.get("/", response_model=List[GrupoList])
def listar_grupos(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    periodo: str = Query(None, description="Filtrar por período ej: 2024-1"),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    svc = GrupoService(db)
    if periodo:
        return svc.repo.get_by_periodo(periodo)
    return svc.listar(skip=skip, limit=limit)


@router.get("/{grupo_id}", response_model=GrupoResponse)
def obtener_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    svc = GrupoService(db)
    grupo = svc.obtener(grupo_id)
    # Enriquecer con nombres y count
    response = GrupoResponse.model_validate(grupo)
    response.asignatura_nombre = grupo.asignatura.nombre if grupo.asignatura else None
    response.docente_nombre = f"{grupo.docente.nombres} {grupo.docente.apellidos}" if grupo.docente else None
    response.matriculados = svc.obtener_matriculados(grupo_id)
    return response


@router.post("/", response_model=GrupoResponse, status_code=201)
def crear_grupo(
    data: GrupoCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return GrupoService(db).crear(data)


@router.put("/{grupo_id}", response_model=GrupoResponse)
def actualizar_grupo(
    grupo_id: int,
    data: GrupoUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return GrupoService(db).actualizar(grupo_id, data)


@router.delete("/{grupo_id}", status_code=204)
def eliminar_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    GrupoService(db).eliminar(grupo_id)
