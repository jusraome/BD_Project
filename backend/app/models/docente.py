"""
Modelo: Docente
===============
DISTRIBUCIÓN FUTURA:
- Docentes pertenecen a una facultad → mismo nodo
- Un docente puede dictar grupos en diferentes facultades → consulta federada
"""

import enum
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class CategoriaDocente(str, enum.Enum):
    TITULAR = "titular"
    ASOCIADO = "asociado"
    AUXILIAR = "auxiliar"
    CATEDRATICO = "catedratico"
    VISITANTE = "visitante"


class EstadoDocente(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    LICENCIA = "licencia"


class Docente(Base):
    __tablename__ = "docentes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    telefono: Mapped[str | None] = mapped_column(String(20))
    categoria: Mapped[str] = mapped_column(
        SQLEnum(CategoriaDocente), default=CategoriaDocente.CATEDRATICO, nullable=False
    )
    facultad_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("facultades.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    estado: Mapped[str] = mapped_column(
        SQLEnum(EstadoDocente), default=EstadoDocente.ACTIVO, nullable=False
    )

    # ─── Relaciones ────────────────────────────────────────────────────────────
    facultad: Mapped["Facultad"] = relationship("Facultad", back_populates="docentes")
    grupos: Mapped[list["Grupo"]] = relationship("Grupo", back_populates="docente")

    def __repr__(self) -> str:
        return f"<Docente id={self.id} nombre={self.nombres!r} {self.apellidos!r}>"
