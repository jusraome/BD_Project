"""
Módulo de seguridad: JWT y hashing de contraseñas
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


# ─── Contraseñas ───────────────────────────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """Genera hash bcrypt de una contraseña en texto plano."""
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con su hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# ─── JWT Tokens ────────────────────────────────────────────────────────────────

def create_access_token(
    subject: Any,
    extra_data: Optional[dict] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Genera un JWT access token.

    Args:
        subject: Identificador principal (normalmente user_id o username)
        extra_data: Datos adicionales a incluir en el payload (rol, etc.)
        expires_delta: Tiempo de expiración personalizado
    """
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
        "type": "access",
    }

    if extra_data:
        payload.update(extra_data)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un JWT token.

    Returns:
        dict con el payload si el token es válido, None si no.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except JWTError:
        return None
