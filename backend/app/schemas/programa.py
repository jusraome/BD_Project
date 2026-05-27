from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.programa import NivelFormacion, Modalidad, EstadoPrograma


class ProgramaBase(BaseModel):
    nombre: str
    nivel_formacion: NivelFormacion
    modalidad: Modalidad = Modalidad.PRESENCIAL
    facultad_id: int
    estado: EstadoPrograma = EstadoPrograma.ACTIVO


class ProgramaCreate(ProgramaBase):
    pass


class ProgramaUpdate(BaseModel):
    nombre: Optional[str] = None
    nivel_formacion: Optional[NivelFormacion] = None
    modalidad: Optional[Modalidad] = None
    facultad_id: Optional[int] = None
    estado: Optional[EstadoPrograma] = None


class ProgramaResponse(ProgramaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    facultad_nombre: Optional[str] = None

    @classmethod
    def from_orm_with_facultad(cls, programa):
        data = cls.model_validate(programa)
        if programa.facultad:
            data.facultad_nombre = programa.facultad.nombre
        return data


class ProgramaList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    nivel_formacion: NivelFormacion
    modalidad: Modalidad
    estado: EstadoPrograma
    facultad_id: int
