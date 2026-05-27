from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_or_coordinador
from app.services.programa import ProgramaService
from app.schemas.programa import ProgramaCreate, ProgramaUpdate, ProgramaResponse, ProgramaList

router = APIRouter(prefix="/programas", tags=["Programas Académicos"])


@router.get("/", response_model=List[ProgramaList])
def listar_programas(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return ProgramaService(db).listar(skip=skip, limit=limit)


@router.get("/{programa_id}", response_model=ProgramaResponse)
def obtener_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return ProgramaService(db).obtener(programa_id)


@router.post("/", response_model=ProgramaResponse, status_code=201)
def crear_programa(
    data: ProgramaCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return ProgramaService(db).crear(data)


@router.put("/{programa_id}", response_model=ProgramaResponse)
def actualizar_programa(
    programa_id: int,
    data: ProgramaUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return ProgramaService(db).actualizar(programa_id, data)


@router.delete("/{programa_id}", status_code=204)
def eliminar_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    ProgramaService(db).eliminar(programa_id)
