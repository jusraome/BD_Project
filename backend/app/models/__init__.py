"""
Paquete de modelos
===================
Importar todos los modelos aquí es ESENCIAL para que:
1. Alembic detecte todos los modelos en Base.metadata
2. SQLAlchemy resuelva todas las relaciones correctamente
3. Las migraciones incluyan todas las tablas

NOTA: El orden de importación no importa gracias a las
referencias por string en las relaciones (lazy evaluation).
"""

from app.models.base import Base
from app.models.facultad import Facultad, EstadoGeneral
from app.models.programa import ProgramaAcademico, NivelFormacion, Modalidad, EstadoPrograma
from app.models.estudiante import Estudiante, TipoDocumento, EstadoEstudiante
from app.models.docente import Docente, CategoriaDocente, EstadoDocente
from app.models.asignatura import Asignatura, EstadoAsignatura
from app.models.grupo import Grupo, EstadoGrupo
from app.models.matricula import Matricula, EstadoMatricula
from app.models.nota import Nota, EstadoAprobacion
from app.models.pago import PagoMatricula, EstadoPago, MedioPago
from app.models.usuario import Usuario, RolUsuario

__all__ = [
    "Base",
    "Facultad", "EstadoGeneral",
    "ProgramaAcademico", "NivelFormacion", "Modalidad", "EstadoPrograma",
    "Estudiante", "TipoDocumento", "EstadoEstudiante",
    "Docente", "CategoriaDocente", "EstadoDocente",
    "Asignatura", "EstadoAsignatura",
    "Grupo", "EstadoGrupo",
    "Matricula", "EstadoMatricula",
    "Nota", "EstadoAprobacion",
    "PagoMatricula", "EstadoPago", "MedioPago",
    "Usuario", "RolUsuario",
]
