"""
Configuración de Alembic para migraciones.
==========================================
Importa todos los modelos para que Alembic pueda detectar cambios.
"""

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.models.base import Base

# IMPORTANTE: Importar TODOS los modelos para que Alembic los detecte
import app.models  # noqa: F401

# Objeto de configuración de Alembic
config = context.config

# Sobreescribir la URL desde las settings de la app
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configurar logging de Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de todos los modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo 'offline' (sin conexión activa)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta migraciones en modo 'online' (con conexión activa)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
