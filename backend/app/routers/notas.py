from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.services.nota import NotaService
from app.schemas.nota import NotaCreate, NotaUpdate, NotaResponse, NotaList

router = APIRouter(prefix="/notas", tags=["Notas"])


@router.get("/", response_model=List[NotaList])
def listar_notas(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return NotaService(db).listar(skip=skip, limit=limit)


@router.get("/matricula/{matricula_id}", response_model=NotaResponse)
def obtener_nota_por_matricula(
    matricula_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return NotaService(db).obtener_por_matricula(matricula_id)


@router.get("/{nota_id}", response_model=NotaResponse)
def obtener_nota(
    nota_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return NotaService(db).obtener(nota_id)


@router.post("/", response_model=NotaResponse, status_code=201)
def crear_nota(
    data: NotaCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return NotaService(db).crear(data)


@router.put("/{nota_id}", response_model=NotaResponse)
def actualizar_nota(
    nota_id: int,
    data: NotaUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return NotaService(db).actualizar(nota_id, data)
