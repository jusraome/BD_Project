"""
Modelo: Asignatura
==================
DISTRIBUCIÓN FUTURA:
- Las asignaturas son parte del plan de estudios de un programa
- Pueden replicarse en nodo central para consultas de plan de estudios
"""

import enum
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EstadoAsignatura(str, enum.Enum):
    ACTIVA = "activa"
    INACTIVA = "inactiva"


class Asignatura(Base):
    __tablename__ = "asignaturas"
    __table_args__ = (
        CheckConstraint("creditos >= 1 AND creditos <= 20", name="ck_asignatura_creditos"),
        CheckConstraint("semestre_sugerido >= 1 AND semestre_sugerido <= 12", name="ck_asignatura_semestre"),
        CheckConstraint("horas_teoricas >= 0", name="ck_horas_teoricas"),
        CheckConstraint("horas_practicas >= 0", name="ck_horas_practicas"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    creditos: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    horas_teoricas: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    horas_practicas: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    programa_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("programas_academicos.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    semestre_sugerido: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estado: Mapped[str] = mapped_column(
        SQLEnum(EstadoAsignatura), default=EstadoAsignatura.ACTIVA, nullable=False
    )

    # ─── Relaciones ────────────────────────────────────────────────────────────
    programa: Mapped["ProgramaAcademico"] = relationship(
        "ProgramaAcademico", back_populates="asignaturas"
    )
    grupos: Mapped[list["Grupo"]] = relationship(
        "Grupo", back_populates="asignatura", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Asignatura codigo={self.codigo!r} nombre={self.nombre!r}>"
