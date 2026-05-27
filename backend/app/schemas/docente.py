from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.models.docente import CategoriaDocente, EstadoDocente


class DocenteBase(BaseModel):
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: Optional[str] = None
    categoria: CategoriaDocente = CategoriaDocente.CATEDRATICO
    facultad_id: int
    estado: EstadoDocente = EstadoDocente.ACTIVO


class DocenteCreate(DocenteBase):
    pass


class DocenteUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    categoria: Optional[CategoriaDocente] = None
    facultad_id: Optional[int] = None
    estado: Optional[EstadoDocente] = None


class DocenteResponse(DocenteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    facultad_nombre: Optional[str] = None


class DocenteList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombres: str
    apellidos: str
    correo: str
    categoria: CategoriaDocente
    estado: EstadoDocente
    facultad_id: int
