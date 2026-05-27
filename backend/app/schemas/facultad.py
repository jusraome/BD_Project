from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.facultad import EstadoGeneral


class FacultadBase(BaseModel):
    nombre: str
    ubicacion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado: EstadoGeneral = EstadoGeneral.ACTIVO


class FacultadCreate(FacultadBase):
    pass


class FacultadUpdate(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado: Optional[EstadoGeneral] = None


class FacultadResponse(FacultadBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class FacultadList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    estado: EstadoGeneral
