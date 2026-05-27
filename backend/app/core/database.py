"""
Módulo de configuración de base de datos
=========================================
Punto central para TODAS las conexiones de base de datos.

ARQUITECTURA ACTUAL: Instancia única PostgreSQL.

ROADMAP DE DISTRIBUCIÓN FUTURA:
─────────────────────────────────────────────────────────────
Fase 1 (Actual):
    - Un solo motor PostgreSQL
    - SessionLocal único

Fase 2 - Réplicas de lectura:
    - engine_write → escrituras
    - engine_read  → lecturas/reportes
    - Función get_read_db() para consultas pesadas

Fase 3 - Sharding por facultad:
    - engines: Dict[int, Engine]  # {facultad_id: engine}
    - Función get_db_for_faculty(faculty_id) -> Session
    - Los repositories reciben el session correcto

Fase 4 - Nodos especializados:
    - engine_pagos   → nodo centralizado de pagos
    - engine_notas   → nodo de historial académico
    - engine_<fac>   → nodo por facultad

Para agregar un nodo nuevo en el futuro:
    1. Añadir DATABASE_URL_NUEVO en config.py
    2. Crear engine con create_engine(settings.DATABASE_URL_NUEVO)
    3. Crear SessionLocal específico
    4. Crear función get_db_nuevo() como FastAPI dependency
    5. Inyectar el nuevo dependency en los repositories correspondientes
─────────────────────────────────────────────────────────────
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings


# ─── Motor principal ───────────────────────────────────────────────────────────
# FUTURO: Este será uno de varios motores. Se enrutará por contexto/facultad.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # Verifica conexión antes de usarla
    pool_recycle=300,         # Recicla conexiones cada 5 minutos
    pool_size=10,             # Conexiones base en el pool
    max_overflow=20,          # Conexiones adicionales bajo carga
    echo=settings.DEBUG,      # Log SQL en modo debug
)

# ─── Fábrica de sesiones ───────────────────────────────────────────────────────
# FUTURO: Habrá múltiples SessionLocal, uno por nodo.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency que provee una sesión de base de datos.

    FUTURO - Enrutamiento por contexto:
    def get_db(
        request: Request,
        faculty_id: Optional[int] = None
    ) -> Generator[Session, None, None]:
        engine = DatabaseRouter.get_engine(faculty_id or request.state.faculty_id)
        db = sessionmaker(bind=engine)()
        ...

    USO:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """Verifica que la conexión a la base de datos funcione."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
