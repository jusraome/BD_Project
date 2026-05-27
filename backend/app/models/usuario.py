"""
Modelo: Usuario
===============
Usuarios del sistema con autenticación por roles.

DISTRIBUCIÓN FUTURA:
- La tabla de usuarios podría ser replicada en todos los nodos
- O centralizada en un nodo de autenticación (SSO)
"""

import enum
from datetime import datetime
from sqlalchemy import String, Integer, Enum as SQLEnum, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class RolUsuario(str, enum.Enum):
    ADMIN = "admin"
    COORDINADOR = "coordinador"
    DOCENTE = "docente"
    ESTUDIANTE = "estudiante"
    ADMINISTRATIVO = "administrativo"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(
        SQLEnum(RolUsuario), default=RolUsuario.ESTUDIANTE, nullable=False
    )
    estado: Mapped[str] = mapped_column(String(20), default="activo", nullable=False)
    ultimo_acceso: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Usuario id={self.id} username={self.username!r} rol={self.rol!r}>"
