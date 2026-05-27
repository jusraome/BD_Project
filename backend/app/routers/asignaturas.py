from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_or_coordinador
from app.services.asignatura import AsignaturaService
from app.schemas.asignatura import AsignaturaCreate, AsignaturaUpdate, AsignaturaResponse, AsignaturaList

router = APIRouter(prefix="/asignaturas", tags=["Asignaturas"])


@router.get("/", response_model=List[AsignaturaList])
def listar_asignaturas(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return AsignaturaService(db).listar(skip=skip, limit=limit)


@router.get("/{asignatura_id}", response_model=AsignaturaResponse)
def obtener_asignatura(
    asignatura_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return AsignaturaService(db).obtener(asignatura_id)


@router.post("/", response_model=AsignaturaResponse, status_code=201)
def crear_asignatura(
    data: AsignaturaCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return AsignaturaService(db).crear(data)


@router.put("/{asignatura_id}", response_model=AsignaturaResponse)
def actualizar_asignatura(
    asignatura_id: int,
    data: AsignaturaUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return AsignaturaService(db).actualizar(asignatura_id, data)


@router.delete("/{asignatura_id}", status_code=204)
def eliminar_asignatura(
    asignatura_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    AsignaturaService(db).eliminar(asignatura_id)
