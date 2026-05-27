from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.matricula import EstadoMatricula


class MatriculaBase(BaseModel):
    estudiante_id: int
    grupo_id: int
    estado: EstadoMatricula = EstadoMatricula.ACTIVA


class MatriculaCreate(MatriculaBase):
    pass


class MatriculaUpdate(BaseModel):
    estado: Optional[EstadoMatricula] = None


class MatriculaResponse(MatriculaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_matricula: datetime
    estudiante_nombre: Optional[str] = None
    grupo_info: Optional[str] = None


class MatriculaList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    estudiante_id: int
    grupo_id: int
    fecha_matricula: datetime
    estado: EstadoMatricula
