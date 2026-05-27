from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_or_coordinador
from app.services.facultad import FacultadService
from app.schemas.facultad import FacultadCreate, FacultadUpdate, FacultadResponse, FacultadList

router = APIRouter(prefix="/facultades", tags=["Facultades"])


@router.get("/", response_model=List[FacultadList])
def listar_facultades(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return FacultadService(db).listar(skip=skip, limit=limit)


@router.get("/{facultad_id}", response_model=FacultadResponse)
def obtener_facultad(
    facultad_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return FacultadService(db).obtener(facultad_id)


@router.post("/", response_model=FacultadResponse, status_code=201)
def crear_facultad(
    data: FacultadCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return FacultadService(db).crear(data)


@router.put("/{facultad_id}", response_model=FacultadResponse)
def actualizar_facultad(
    facultad_id: int,
    data: FacultadUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return FacultadService(db).actualizar(facultad_id, data)


@router.delete("/{facultad_id}", status_code=204)
def eliminar_facultad(
    facultad_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    FacultadService(db).eliminar(facultad_id)
