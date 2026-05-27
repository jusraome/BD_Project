from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_or_administrativo
from app.services.estudiante import EstudianteService
from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate, EstudianteResponse, EstudianteList

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/", response_model=List[EstudianteList])
def listar_estudiantes(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: Optional[str] = Query(None, description="Búsqueda por nombre, apellido o código"),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    svc = EstudianteService(db)
    if q:
        return svc.buscar(q)
    return svc.listar(skip=skip, limit=limit)


@router.get("/{estudiante_id}", response_model=EstudianteResponse)
def obtener_estudiante(
    estudiante_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return EstudianteService(db).obtener(estudiante_id)


@router.post("/", response_model=EstudianteResponse, status_code=201)
def crear_estudiante(
    data: EstudianteCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_administrativo),
):
    return EstudianteService(db).crear(data)


@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def actualizar_estudiante(
    estudiante_id: int,
    data: EstudianteUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_administrativo),
):
    return EstudianteService(db).actualizar(estudiante_id, data)


@router.delete("/{estudiante_id}", status_code=204)
def eliminar_estudiante(
    estudiante_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_administrativo),
):
    EstudianteService(db).eliminar(estudiante_id)
