from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from app.models.nota import EstadoAprobacion


def _validar_nota(v, field_name: str):
    if v is not None and not (0.0 <= float(v) <= 5.0):
        raise ValueError(f"{field_name} debe estar entre 0.0 y 5.0")
    return v


class NotaBase(BaseModel):
    matricula_id: int
    corte1: Optional[float] = None
    corte2: Optional[float] = None
    corte3: Optional[float] = None

    @field_validator("corte1", "corte2", "corte3", mode="before")
    @classmethod
    def validar_cortes(cls, v):
        if v is not None and not (0.0 <= float(v) <= 5.0):
            raise ValueError("La nota debe estar entre 0.0 y 5.0")
        return v


class NotaCreate(NotaBase):
    pass


class NotaUpdate(BaseModel):
    corte1: Optional[float] = None
    corte2: Optional[float] = None
    corte3: Optional[float] = None

    @field_validator("corte1", "corte2", "corte3", mode="before")
    @classmethod
    def validar_cortes(cls, v):
        if v is not None and not (0.0 <= float(v) <= 5.0):
            raise ValueError("La nota debe estar entre 0.0 y 5.0")
        return v


class NotaResponse(NotaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nota_final: Optional[float] = None
    estado_aprobacion: EstadoAprobacion


class NotaList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    matricula_id: int
    corte1: Optional[float] = None
    corte2: Optional[float] = None
    corte3: Optional[float] = None
    nota_final: Optional[float] = None
    estado_aprobacion: EstadoAprobacion
