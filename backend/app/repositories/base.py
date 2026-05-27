"""
Repository Base Genérico
=========================
Provee operaciones CRUD estándar para todos los modelos.

NOTA DISTRIBUCIÓN FUTURA:
En una arquitectura distribuida, este BaseRepository podría
recibir múltiples sesiones o un router de sesiones:

class BaseRepository(Generic[ModelType]):
    def __init__(self, model, db: Session, db_replica: Session = None):
        self.db = db                    # escrituras → nodo primario
        self.db_read = db_replica or db # lecturas   → réplica

Luego cada operación de lectura usaría self.db_read
y cada escritura usaría self.db.
"""

from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Repository base con operaciones CRUD estándar."""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Obtiene un registro por ID."""
        return self.db.execute(
            select(self.model).where(self.model.id == id)
        ).scalar_one_or_none()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtiene todos los registros con paginación."""
        return list(
            self.db.execute(
                select(self.model).offset(skip).limit(limit)
            ).scalars().all()
        )

    def count(self) -> int:
        """Cuenta el total de registros."""
        return self.db.execute(
            select(func.count()).select_from(self.model)
        ).scalar_one()

    def create(self, data: dict) -> ModelType:
        """Crea un nuevo registro."""
        db_obj = self.model(**data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, data: dict) -> ModelType:
        """Actualiza un registro existente."""
        for field, value in data.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, db_obj: ModelType) -> bool:
        """Elimina un registro."""
        self.db.delete(db_obj)
        self.db.commit()
        return True

    def exists(self, id: int) -> bool:
        """Verifica si existe un registro con el ID dado."""
        return self.db.execute(
            select(func.count()).select_from(self.model).where(self.model.id == id)
        ).scalar_one() > 0
