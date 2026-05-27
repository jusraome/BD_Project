"""Schemas para los reportes académicos."""

from pydantic import BaseModel
from typing import Optional


class EstudiantePorPrograma(BaseModel):
    programa_id: int
    programa_nombre: str
    total_estudiantes: int
    estudiantes_activos: int


class CargaDocenteItem(BaseModel):
    docente_id: int
    nombres: str
    apellidos: str
    total_grupos: int
    total_estudiantes: int
    periodos: str


class PromedioEstudiante(BaseModel):
    estudiante_id: int
    codigo: str
    nombres: str
    apellidos: str
    promedio: Optional[float]
    total_materias: int
    materias_aprobadas: int


class EstudianteRiesgo(BaseModel):
    estudiante_id: int
    codigo: str
    nombres: str
    apellidos: str
    promedio: float
    materias_reprobadas: int


class AsignaturasPerdida(BaseModel):
    asignatura_id: int
    codigo: str
    nombre: str
    total_matriculados: int
    total_reprobados: int
    porcentaje_perdida: float


class GrupoCupo(BaseModel):
    grupo_id: int
    asignatura_nombre: str
    periodo: str
    cupo_maximo: int
    matriculados: int
    disponibles: int
    porcentaje_ocupacion: float


class PagoPendienteItem(BaseModel):
    pago_id: int
    estudiante_id: int
    codigo_estudiante: str
    nombres: str
    apellidos: str
    periodo: str
    valor_pago: float
    estado_pago: str


class RankingEstudiante(BaseModel):
    posicion: int
    estudiante_id: int
    codigo: str
    nombres: str
    apellidos: str
    promedio: float
    programa_nombre: str


class HistorialAcademico(BaseModel):
    periodo: str
    asignatura_codigo: str
    asignatura_nombre: str
    creditos: int
    nota_final: Optional[float]
    estado_aprobacion: str


class DocenteReprobados(BaseModel):
    docente_id: int
    nombres: str
    apellidos: str
    total_estudiantes: int
    total_reprobados: int
    porcentaje_reprobados: float
