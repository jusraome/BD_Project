"""
Modelo: Facultad
================
DISTRIBUCIÓN FUTURA:
- Cada facultad podría tener su propio nodo PostgreSQL
- La tabla facultades podría ser replicada en todos los nodos
  como tabla de referencia/lookup
"""

import enum
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EstadoGeneral(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"


class Facultad(Base):
    __tablename__ = "facultades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    ubicacion: Mapped[str | None] = mapped_column(String(300))
    telefono: Mapped[str | None] = mapped_column(String(20))
    correo: Mapped[str | None] = mapped_column(String(100), unique=True)
    estado: Mapped[str] = mapped_column(
        SQLEnum(EstadoGeneral), default=EstadoGeneral.ACTIVO, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # ─── Relaciones ────────────────────────────────────────────────────────────
    programas: Mapped[list["ProgramaAcademico"]] = relationship(
        "ProgramaAcademico",
        back_populates="facultad",
        cascade="all, delete-orphan",
    )
    docentes: Mapped[list["Docente"]] = relationship(
        "Docente",
        back_populates="facultad",
    )

    def __repr__(self) -> str:
        return f"<Facultad id={self.id} nombre={self.nombre!r}>"
