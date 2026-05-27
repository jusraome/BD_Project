"""
Modelo: Grupo
=============
Un Grupo es una instancia de una Asignatura dictada por un Docente
en un período académico específico.

DISTRIBUCIÓN FUTURA:
- Los grupos son locales a la facultad donde se dicta la asignatura
- La consulta de carga docente entre facultades requeriría JOIN federado
"""

import enum
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum, CheckConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EstadoGrupo(str, enum.Enum):
    ACTIVO = "activo"
    CERRADO = "cerrado"
    CANCELADO = "cancelado"


class Grupo(Base):
    __tablename__ = "grupos"
    __table_args__ = (
        CheckConstraint("cupo_maximo >= 1 AND cupo_maximo <= 200", name="ck_grupo_cupo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asignatura_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("asignaturas.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    docente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("docentes.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    periodo: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # Ej: "2024-1"
    cupo_maximo: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    horario: Mapped[str | None] = mapped_column(Text)         # JSON o texto libre
    aula: Mapped[str | None] = mapped_column(String(50))
    estado: Mapped[str] = mapped_column(
        SQLEnum(EstadoGrupo), default=EstadoGrupo.ACTIVO, nullable=False
    )

    # ─── Relaciones ────────────────────────────────────────────────────────────
    asignatura: Mapped["Asignatura"] = relationship("Asignatura", back_populates="grupos")
    docente: Mapped["Docente"] = relationship("Docente", back_populates="grupos")
    matriculas: Mapped[list["Matricula"]] = relationship(
        "Matricula", back_populates="grupo", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Grupo id={self.id} periodo={self.periodo!r}>"
