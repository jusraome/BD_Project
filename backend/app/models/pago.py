"""
Modelo: PagoMatricula
======================
Registro de pagos de matrícula por período académico.

DISTRIBUCIÓN FUTURA:
- Los pagos son candidato principal para nodo centralizado independiente
- Alta prioridad de integridad y auditoría
- Posible integración con sistemas bancarios externos
"""

import enum
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum, DateTime, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class EstadoPago(str, enum.Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    EN_MORA = "en_mora"
    ANULADO = "anulado"
    PARCIAL = "parcial"


class MedioPago(str, enum.Enum):
    TRANSFERENCIA = "transferencia"
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    PSE = "pse"
    CONVENIO = "convenio"


class PagoMatricula(Base):
    __tablename__ = "pagos_matricula"
    __table_args__ = (
        CheckConstraint("valor_pago >= 0", name="ck_pago_valor"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    estudiante_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("estudiantes.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    periodo: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # Ej: "2024-1"
    valor_pago: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    fecha_pago: Mapped[datetime | None] = mapped_column(DateTime, default=None)
    estado_pago: Mapped[str] = mapped_column(
        SQLEnum(EstadoPago), default=EstadoPago.PENDIENTE, nullable=False
    )
    medio_pago: Mapped[str | None] = mapped_column(SQLEnum(MedioPago))
    referencia: Mapped[str | None] = mapped_column(String(100))   # Número de referencia bancaria
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # ─── Relaciones ────────────────────────────────────────────────────────────
    estudiante: Mapped["Estudiante"] = relationship("Estudiante", back_populates="pagos")

    def __repr__(self) -> str:
        return f"<PagoMatricula id={self.id} estudiante_id={self.estudiante_id} periodo={self.periodo!r}>"
