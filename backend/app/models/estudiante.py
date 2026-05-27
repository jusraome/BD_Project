"""
Modelo: Estudiante
==================
DISTRIBUCIÓN FUTURA:
- Candidato principal para fragmentación horizontal (por programa/facultad)
- El campo programa_id → llave de sharding
- Datos personales: nodo local de facultad
- Historial académico: nodo centralizado de consultas
"""

import enum
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TipoDocumento(str, enum.Enum):
    CC = "CC"        # Cédula de Ciudadanía
    TI = "TI"        # Tarjeta de Identidad
    CE = "CE"        # Cédula de Extranjería
    PP = "PP"        # Pasaporte
    NIT = "NIT"      # NIT


class EstadoEstudiante(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    GRADUADO = "graduado"
    RETIRADO = "retirado"
    SUSPENDIDO = "suspendido"


class Estudiante(Base):
    __tablename__ = "estudiantes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    tipo_documento: Mapped[str] = mapped_column(SQLEnum(TipoDocumento), nullable=False)
    numero_documento: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    telefono: Mapped[str | None] = mapped_column(String(20))
    direccion: Mapped[str | None] = mapped_column(String(300))
    programa_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("programas_academicos.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    estado: Mapped[str] = mapped_column(
        SQLEnum(EstadoEstudiante), default=EstadoEstudiante.ACTIVO, nullable=False
    )

    # ─── Relaciones ────────────────────────────────────────────────────────────
    programa: Mapped["ProgramaAcademico"] = relationship(
        "ProgramaAcademico", back_populates="estudiantes"
    )
    matriculas: Mapped[list["Matricula"]] = relationship(
        "Matricula", back_populates="estudiante"
    )
    pagos: Mapped[list["PagoMatricula"]] = relationship(
        "PagoMatricula", back_populates="estudiante"
    )

    def __repr__(self) -> str:
        return f"<Estudiante codigo={self.codigo!r} nombre={self.nombres!r} {self.apellidos!r}>"
