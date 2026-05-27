from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from app.models.grupo import EstadoGrupo


class GrupoBase(BaseModel):
    asignatura_id: int
    docente_id: int
    periodo: str
    cupo_maximo: int = 30
    horario: Optional[str] = None
    aula: Optional[str] = None
    estado: EstadoGrupo = EstadoGrupo.ACTIVO

    @field_validator("cupo_maximo")
    @classmethod
    def validar_cupo(cls, v):
        if not (1 <= v <= 200):
            raise ValueError("El cupo máximo debe estar entre 1 y 200")
        return v


class GrupoCreate(GrupoBase):
    pass


class GrupoUpdate(BaseModel):
    docente_id: Optional[int] = None
    cupo_maximo: Optional[int] = None
    horario: Optional[str] = None
    aula: Optional[str] = None
    estado: Optional[EstadoGrupo] = None


class GrupoResponse(GrupoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asignatura_nombre: Optional[str] = None
    docente_nombre: Optional[str] = None
    matriculados: Optional[int] = None


class GrupoList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    periodo: str
    cupo_maximo: int
    estado: EstadoGrupo
    asignatura_id: int
    docente_id: int
