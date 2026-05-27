from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.models.estudiante import TipoDocumento, EstadoEstudiante


class EstudianteBase(BaseModel):
    codigo: str
    tipo_documento: TipoDocumento
    numero_documento: str
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_id: int
    estado: EstadoEstudiante = EstadoEstudiante.ACTIVO


class EstudianteCreate(EstudianteBase):
    pass


class EstudianteUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_id: Optional[int] = None
    estado: Optional[EstadoEstudiante] = None


class EstudianteResponse(EstudianteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    programa_nombre: Optional[str] = None


class EstudianteList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombres: str
    apellidos: str
    correo: str
    estado: EstadoEstudiante
    programa_id: int
