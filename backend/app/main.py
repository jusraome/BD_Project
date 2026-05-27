"""
Punto de entrada de la aplicación FastAPI
==========================================
Sistema de Gestión Académica Universitaria
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import check_db_connection

# ─── Importar todos los routers ────────────────────────────────────────────────
from app.routers import (
    auth, facultades, programas, estudiantes, docentes,
    asignaturas, grupos, matriculas, notas, pagos, usuarios, reportes,
)

# ─── Crear la app ──────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## Sistema de Gestión Académica Universitaria

    API REST para la gestión de:
    - 🏛️ Facultades y programas académicos
    - 👩‍🎓 Estudiantes y docentes
    - 📚 Asignaturas y grupos
    - 📝 Matrículas y notas
    - 💰 Pagos de matrícula
    - 📊 Reportes y consultas académicas

    **Arquitectura preparada para futura distribución de datos.**
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Registrar routers ─────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(facultades.router)
app.include_router(programas.router)
app.include_router(estudiantes.router)
app.include_router(docentes.router)
app.include_router(asignaturas.router)
app.include_router(grupos.router)
app.include_router(matriculas.router)
app.include_router(notas.router)
app.include_router(pagos.router)
app.include_router(usuarios.router)
app.include_router(reportes.router)


# ─── Endpoint de salud ─────────────────────────────────────────────────────────
@app.get("/health", tags=["Sistema"])
def health_check():
    """Verifica el estado de la aplicación y la conexión a la BD."""
    db_ok = check_db_connection()
    return {
        "status": "ok" if db_ok else "degraded",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "connected" if db_ok else "error",
    }


@app.get("/", tags=["Sistema"])
def root():
    return {
        "message": f"Bienvenido al {settings.APP_NAME}",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }
