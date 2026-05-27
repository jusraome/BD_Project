"""
Configuración central de la aplicación
=======================================
Centraliza TODA la configuración usando pydantic-settings.

NOTA DISTRIBUCIÓN FUTURA:
Aquí se agregarán URLs de conexión para nodos adicionales:
- DATABASE_URL_FACULTAD_INGENIERIA
- DATABASE_URL_FACULTAD_CIENCIAS
- DATABASE_URL_PAGOS (nodo centralizado)
- DATABASE_URL_HISTORICO (nodo de solo lectura)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ─── Aplicación ────────────────────────────────────────
    APP_NAME: str = "Sistema de Gestión Académica Universitaria"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ─── CORS ──────────────────────────────────────────────
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ─── Base de Datos Principal ───────────────────────────
    # FASE ACTUAL: Instancia única PostgreSQL
    # FUTURO: Agregar URLs por nodo/facultad
    DATABASE_URL: str = "postgresql://postgres:Admin123@localhost:5432/academia_db"

    # ─── Seguridad JWT ─────────────────────────────────────
    SECRET_KEY: str = "test123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ─── Paginación por defecto ────────────────────────────
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 200


# Instancia global — importar desde aquí en toda la app
settings = Settings()
