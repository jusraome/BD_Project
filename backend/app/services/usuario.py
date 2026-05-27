from typing import List
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.repositories.usuario import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioCambiarPassword
from app.core.security import hash_password, verify_password


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener(self, usuario_id: int) -> Usuario:
        usuario = self.repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado",
            )
        return usuario

    def crear(self, data: UsuarioCreate) -> Usuario:
        if self.repo.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario con el username '{data.username}'",
            )
        if self.repo.get_by_correo(data.correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario con el correo '{data.correo}'",
            )

        user_data = data.model_dump(exclude={"password"})
        user_data["password_hash"] = hash_password(data.password)
        return self.repo.create(user_data)

    def actualizar(self, usuario_id: int, data: UsuarioUpdate) -> Usuario:
        usuario = self.obtener(usuario_id)
        return self.repo.update(usuario, data.model_dump(exclude_none=True))

    def cambiar_password(self, usuario_id: int, data: UsuarioCambiarPassword) -> bool:
        usuario = self.obtener(usuario_id)
        if not verify_password(data.password_actual, usuario.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña actual no es correcta",
            )
        self.repo.update(usuario, {"password_hash": hash_password(data.password_nueva)})
        return True

    def eliminar(self, usuario_id: int) -> bool:
        usuario = self.obtener(usuario_id)
        return self.repo.delete(usuario)

    def registrar_acceso(self, usuario_id: int) -> None:
        """Actualiza el campo ultimo_acceso del usuario."""
        usuario = self.repo.get_by_id(usuario_id)
        if usuario:
            self.repo.update(usuario, {"ultimo_acceso": datetime.now(timezone.utc)})
