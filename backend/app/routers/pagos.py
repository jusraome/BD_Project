from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin_or_administrativo
from app.services.pago import PagoService
from app.schemas.pago import PagoCreate, PagoUpdate, PagoResponse, PagoList

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.get("/", response_model=List[PagoList])
def listar_pagos(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return PagoService(db).listar(skip=skip, limit=limit)


@router.get("/pendientes", response_model=List[PagoList])
def pagos_pendientes(
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return PagoService(db).listar_pendientes()


@router.get("/estudiante/{estudiante_id}", response_model=List[PagoList])
def pagos_por_estudiante(
    estudiante_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return PagoService(db).listar_por_estudiante(estudiante_id)


@router.get("/{pago_id}", response_model=PagoResponse)
def obtener_pago(
    pago_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return PagoService(db).obtener(pago_id)


@router.post("/", response_model=PagoResponse, status_code=201)
def crear_pago(
    data: PagoCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_administrativo),
):
    return PagoService(db).crear(data)


@router.put("/{pago_id}", response_model=PagoResponse)
def actualizar_pago(
    pago_id: int,
    data: PagoUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_administrativo),
):
    return PagoService(db).registrar_pago(pago_id, data)


@router.delete("/{pago_id}", status_code=204)
def eliminar_pago(
    pago_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin_or_administrativo),
):
    PagoService(db).eliminar(pago_id)
