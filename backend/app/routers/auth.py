from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.dependencies import get_current_active_user
from app.repositories.usuario import UsuarioRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Autentica un usuario y devuelve un JWT token."""
    repo = UsuarioRepository(db)

    # Buscar por username o correo
    usuario = repo.get_by_username(data.username)
    if not usuario:
        usuario = repo.get_by_correo(data.username)

    if not usuario or not verify_password(data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    if usuario.estado != "activo":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacte al administrador.",
        )

    # Registrar último acceso
    repo.update(usuario, {"ultimo_acceso": datetime.now(timezone.utc)})

    token = create_access_token(
        subject=usuario.id,
        extra_data={"rol": usuario.rol, "username": usuario.username},
    )

    return TokenResponse(
        access_token=token,
        usuario_id=usuario.id,
        username=usuario.username,
        rol=usuario.rol,
    )


@router.get("/me", response_model=UsuarioResponse)
def get_me(current_user=Depends(get_current_active_user)):
    """Devuelve información del usuario autenticado."""
    return current_user
