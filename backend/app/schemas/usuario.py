from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.usuario import RolUsuario


class UsuarioBase(BaseModel):
    username: str
    correo: EmailStr
    rol: RolUsuario = RolUsuario.ESTUDIANTE
    estado: str = "activo"


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(BaseModel):
    correo: Optional[EmailStr] = None
    rol: Optional[RolUsuario] = None
    estado: Optional[str] = None


class UsuarioCambiarPassword(BaseModel):
    password_actual: str
    password_nueva: str


class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ultimo_acceso: Optional[datetime] = None
    created_at: datetime


class UsuarioList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    correo: str
    rol: RolUsuario
    estado: str
