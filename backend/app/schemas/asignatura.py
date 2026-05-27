from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from app.models.asignatura import EstadoAsignatura


class AsignaturaBase(BaseModel):
    codigo: str
    nombre: str
    creditos: int = 3
    horas_teoricas: int = 2
    horas_practicas: int = 2
    programa_id: int
    semestre_sugerido: int = 1
    estado: EstadoAsignatura = EstadoAsignatura.ACTIVA

    @field_validator("creditos")
    @classmethod
    def validar_creditos(cls, v):
        if not (1 <= v <= 20):
            raise ValueError("Los créditos deben estar entre 1 y 20")
        return v

    @field_validator("semestre_sugerido")
    @classmethod
    def validar_semestre(cls, v):
        if not (1 <= v <= 12):
            raise ValueError("El semestre sugerido debe estar entre 1 y 12")
        return v


class AsignaturaCreate(AsignaturaBase):
    pass


class AsignaturaUpdate(BaseModel):
    nombre: Optional[str] = None
    creditos: Optional[int] = None
    horas_teoricas: Optional[int] = None
    horas_practicas: Optional[int] = None
    programa_id: Optional[int] = None
    semestre_sugerido: Optional[int] = None
    estado: Optional[EstadoAsignatura] = None


class AsignaturaResponse(AsignaturaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    programa_nombre: Optional[str] = None


class AsignaturaList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    creditos: int
    semestre_sugerido: int
    estado: EstadoAsignatura
    programa_id: int
