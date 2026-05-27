from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, require_admin
from app.services.usuario import UsuarioService
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioList, UsuarioCambiarPassword

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioList])
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return UsuarioService(db).listar(skip=skip, limit=limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return UsuarioService(db).obtener(usuario_id)


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return UsuarioService(db).crear(data)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    return UsuarioService(db).actualizar(usuario_id, data)


@router.post("/{usuario_id}/cambiar-password")
def cambiar_password(
    usuario_id: int,
    data: UsuarioCambiarPassword,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return UsuarioService(db).cambiar_password(usuario_id, data)


@router.delete("/{usuario_id}", status_code=204)
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    UsuarioService(db).eliminar(usuario_id)
