from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.usuario import Usuario
from app.repositories.base import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, db: Session):
        super().__init__(Usuario, db)

    def get_by_username(self, username: str) -> Optional[Usuario]:
        return self.db.execute(
            select(Usuario).where(Usuario.username == username)
        ).scalar_one_or_none()

    def get_by_correo(self, correo: str) -> Optional[Usuario]:
        return self.db.execute(
            select(Usuario).where(Usuario.correo == correo)
        ).scalar_one_or_none()

    def get_activos(self) -> List[Usuario]:
        return list(
            self.db.execute(
                select(Usuario).where(Usuario.estado == "activo")
            ).scalars().all()
        )
