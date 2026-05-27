from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.pago import EstadoPago, MedioPago


class PagoBase(BaseModel):
    estudiante_id: int
    periodo: str
    valor_pago: float
    estado_pago: EstadoPago = EstadoPago.PENDIENTE
    medio_pago: Optional[MedioPago] = None
    referencia: Optional[str] = None


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    estado_pago: Optional[EstadoPago] = None
    medio_pago: Optional[MedioPago] = None
    fecha_pago: Optional[datetime] = None
    referencia: Optional[str] = None


class PagoResponse(PagoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_pago: Optional[datetime] = None
    created_at: datetime
    estudiante_nombre: Optional[str] = None


class PagoList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    estudiante_id: int
    periodo: str
    valor_pago: float
    estado_pago: EstadoPago
    fecha_pago: Optional[datetime] = None
