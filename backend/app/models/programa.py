"""
Modelo: ProgramaAcademico
==========================
DISTRIBUCIÓN FUTURA:
- La asignación de programas a nodos será clave para el sharding
- Un programa pertenece a una facultad → mismo nodo que su facultad
"""

import enum
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class NivelFormacion(str, enum.Enum):
    PREGRADO = "pregrado"
    POSGRADO = "posgrado"
    TECNICO = "tecnico"
    TECNOLOGICO = "tecnologico"
    ESPECIALIZACION = "especializacion"
    MAESTRIA = "maestria"
    DOCTORADO = "doctorado"


class Modalidad(str, enum.Enum):
    PRESENCIAL = "presencial"
    VIRTUAL = "virtual"
    DISTANCIA = "distancia"
    SEMIPRESENCIAL = "semipresencial"


class EstadoPrograma(str, enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"


class ProgramaAcademico(Base):
    __tablename__ = "programas_academicos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    nivel_formacion: Mapped[str] = mapped_column(
        SQLEnum(NivelFormacion), nullable=False
    )
    modalidad: Mapped[str] = mapped_column(
        SQLEnum(Modalidad), default=Modalidad.PRESENCIAL, nullable=False
    )
    facultad_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("facultades.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    estado: Mapped[str] = mapped_column(
        SQLEnum(EstadoPrograma), default=EstadoPrograma.ACTIVO, nullable=False
    )

    # ─── Relaciones ────────────────────────────────────────────────────────────
    facultad: Mapped["Facultad"] = relationship("Facultad", back_populates="programas")
    estudiantes: Mapped[list["Estudiante"]] = relationship(
        "Estudiante", back_populates="programa"
    )
    asignaturas: Mapped[list["Asignatura"]] = relationship(
        "Asignatura", back_populates="programa", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ProgramaAcademico id={self.id} nombre={self.nombre!r}>"
