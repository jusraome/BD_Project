"""
Modelo: Nota
============
Notas académicas de una matrícula. Una matrícula tiene exactamente una Nota.

Fórmula por defecto: nota_final = corte1*0.3 + corte2*0.3 + corte3*0.4

DISTRIBUCIÓN FUTURA:
- El historial de notas es candidato a nodo centralizado de solo lectura
- Las notas activas van al nodo local; notas históricas al nodo de historial
"""

import enum
from sqlalchemy import Integer, ForeignKey, Enum as SQLEnum, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EstadoAprobacion(str, enum.Enum):
    APROBADO = "aprobado"
    REPROBADO = "reprobado"
    PENDIENTE = "pendiente"   # Notas aún no registradas completamente


class Nota(Base):
    __tablename__ = "notas"
    __table_args__ = (
        CheckConstraint("corte1 >= 0 AND corte1 <= 5", name="ck_nota_corte1"),
        CheckConstraint("corte2 >= 0 AND corte2 <= 5", name="ck_nota_corte2"),
        CheckConstraint("corte3 >= 0 AND corte3 <= 5", name="ck_nota_corte3"),
        CheckConstraint(
            "(nota_final IS NULL) OR (nota_final >= 0 AND nota_final <= 5)",
            name="ck_nota_final",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    matricula_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("matriculas.id", ondelete="CASCADE"),
        unique=True,    # Una matrícula → una sola nota
        nullable=False,
        index=True,
    )
    corte1: Mapped[float | None] = mapped_column(Numeric(4, 2), default=None)
    corte2: Mapped[float | None] = mapped_column(Numeric(4, 2), default=None)
    corte3: Mapped[float | None] = mapped_column(Numeric(4, 2), default=None)
    nota_final: Mapped[float | None] = mapped_column(Numeric(4, 2), default=None)
    estado_aprobacion: Mapped[str] = mapped_column(
        SQLEnum(EstadoAprobacion),
        default=EstadoAprobacion.PENDIENTE,
        nullable=False,
    )

    # ─── Relaciones ────────────────────────────────────────────────────────────
    matricula: Mapped["Matricula"] = relationship("Matricula", back_populates="nota")

    def calcular_nota_final(self) -> float | None:
        """
        Calcula la nota final según los cortes registrados.
        Fórmula: corte1*30% + corte2*30% + corte3*40%
        Retorna None si no todos los cortes están registrados.
        """
        if self.corte1 is None or self.corte2 is None or self.corte3 is None:
            return None
        return round(float(self.corte1) * 0.30 + float(self.corte2) * 0.30 + float(self.corte3) * 0.40, 2)

    def __repr__(self) -> str:
        return f"<Nota id={self.id} matricula_id={self.matricula_id} final={self.nota_final}>"
