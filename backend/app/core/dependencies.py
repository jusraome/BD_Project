"""
Dependencias compartidas de FastAPI
=====================================
Contiene los dependencies para autenticación, roles y base de datos.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.usuario import Usuario, RolUsuario

# Esquema de seguridad Bearer token
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Usuario:
    """
    Dependency que extrae y valida el usuario del JWT token.
    Lanza 401 si el token es inválido o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(credentials.credentials)
    if payload is None:
        raise credentials_exception

    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        uid = int(user_id)
    except ValueError:
        raise credentials_exception

    usuario = db.query(Usuario).filter(
        Usuario.id == uid,
    ).first()

    if usuario is None:
        raise credentials_exception

    return usuario


def get_current_active_user(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    """Verifica que el usuario esté activo."""
    if current_user.estado != "activo":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    return current_user


def require_roles(*roles: RolUsuario):
    """
    Factory de dependency para restringir acceso por rol.

    Uso:
        @router.delete("/{id}")
        def delete_item(
            current_user = Depends(require_roles(RolUsuario.ADMIN))
        ):
            ...
    """
    def _check_role(
        current_user: Usuario = Depends(get_current_active_user),
    ) -> Usuario:
        if current_user.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Roles requeridos: {[r.value for r in roles]}",
            )
        return current_user

    return _check_role


# Shortcuts de roles comunes
require_admin = require_roles(RolUsuario.ADMIN)
require_admin_or_coordinador = require_roles(RolUsuario.ADMIN, RolUsuario.COORDINADOR)
require_admin_or_administrativo = require_roles(
    RolUsuario.ADMIN, RolUsuario.COORDINADOR, RolUsuario.ADMINISTRATIVO
)
