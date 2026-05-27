"""
Modelo: Matricula
==================
Representa la inscripción de un Estudiante a un Grupo.

DISTRIBUCIÓN FUTURA:
- Las matrículas son el punto de JOIN entre estudiantes y grupos
- En arquitectura distribuida, este será el mayor desafío:
  Estudiante en nodo A, Grupo en nodo B → JOIN distribuido
- Estrategia sugerida: mantener matrículas en nodo de la facultad del grupo
"""

import enum
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EstadoMatricula(str, enum.Enum):
    ACTIVA = "activa"
    CANCELADA = "cancelada"
    RETIRADA = "retirada"


class Matricula(Base):
    __tablename__ = "matriculas"
    __table_args__ = (
        # Un estudiante no puede matricularse dos veces en el mismo grupo
        UniqueConstraint("estudiante_id", "grupo_id", name="uq_matricula_estudiante_grupo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    estudiante_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("estudiantes.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    grupo_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("grupos.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    fecha_matricula: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    estado: Mapped[str] = mapped_column(
        SQLEnum(EstadoMatricula), default=EstadoMatricula.ACTIVA, nullable=False
    )

    # ─── Relaciones ────────────────────────────────────────────────────────────
    estudiante: Mapped["Estudiante"] = relationship("Estudiante", back_populates="matriculas")
    grupo: Mapped["Grupo"] = relationship("Grupo", back_populates="matriculas")
    nota: Mapped["Nota | None"] = relationship(
        "Nota", back_populates="matricula", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Matricula id={self.id} estudiante_id={self.estudiante_id} grupo_id={self.grupo_id}>"
