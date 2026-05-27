from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_or_coordinador
from app.services.docente import DocenteService
from app.schemas.docente import DocenteCreate, DocenteUpdate, DocenteResponse, DocenteList

router = APIRouter(prefix="/docentes", tags=["Docentes"])


@router.get("/", response_model=List[DocenteList])
def listar_docentes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: Optional[str] = Query(None, description="Búsqueda por nombre"),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    svc = DocenteService(db)
    if q:
        return svc.buscar(q)
    return svc.listar(skip=skip, limit=limit)


@router.get("/{docente_id}", response_model=DocenteResponse)
def obtener_docente(
    docente_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return DocenteService(db).obtener(docente_id)


@router.post("/", response_model=DocenteResponse, status_code=201)
def crear_docente(
    data: DocenteCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return DocenteService(db).crear(data)


@router.put("/{docente_id}", response_model=DocenteResponse)
def actualizar_docente(
    docente_id: int,
    data: DocenteUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    return DocenteService(db).actualizar(docente_id, data)


@router.delete("/{docente_id}", status_code=204)
def eliminar_docente(
    docente_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_coordinador),
):
    DocenteService(db).eliminar(docente_id)
