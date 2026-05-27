from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.services.reportes import ReportesService
from app.schemas.reportes import (
    EstudiantePorPrograma, CargaDocenteItem, PromedioEstudiante,
    EstudianteRiesgo, AsignaturasPerdida, GrupoCupo,
    PagoPendienteItem, RankingEstudiante, HistorialAcademico,
    DocenteReprobados,
)

router = APIRouter(prefix="/reportes", tags=["Reportes Académicos"])


@router.get("/estudiantes-por-programa", response_model=List[EstudiantePorPrograma])
def estudiantes_por_programa(
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Cantidad de estudiantes matriculados por programa."""
    return ReportesService(db).estudiantes_por_programa()


@router.get("/carga-docente", response_model=List[CargaDocenteItem])
def carga_docente(
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Carga académica por docente: grupos y estudiantes activos."""
    return ReportesService(db).carga_docente()


@router.get("/promedio-estudiantes", response_model=List[PromedioEstudiante])
def promedio_estudiantes(
    programa_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Promedio académico de todos los estudiantes."""
    return ReportesService(db).promedio_por_estudiante(programa_id=programa_id)


@router.get("/estudiantes-riesgo", response_model=List[EstudianteRiesgo])
def estudiantes_riesgo(
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Estudiantes en riesgo académico (promedio < 3.5 o con reprobadas)."""
    return ReportesService(db).estudiantes_en_riesgo()


@router.get("/asignaturas-mayor-perdida", response_model=List[AsignaturasPerdida])
def asignaturas_mayor_perdida(
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Asignaturas con mayor porcentaje de pérdida."""
    return ReportesService(db).asignaturas_mayor_perdida()


@router.get("/grupos-limite-cupo", response_model=List[GrupoCupo])
def grupos_limite_cupo(
    umbral: float = Query(80.0, description="Porcentaje mínimo de ocupación (ej: 80)"),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Grupos que han alcanzado o superado el umbral de ocupación."""
    return ReportesService(db).grupos_cerca_limite_cupo(umbral_pct=umbral)


@router.get("/pagos-pendientes", response_model=List[PagoPendienteItem])
def pagos_pendientes(
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Listado de todos los pagos pendientes o en mora."""
    return ReportesService(db).pagos_pendientes()


@router.get("/ranking-estudiantes", response_model=List[RankingEstudiante])
def ranking_estudiantes(
    programa_id: Optional[int] = Query(None),
    top: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Ranking de mejores estudiantes por promedio."""
    return ReportesService(db).ranking_estudiantes(programa_id=programa_id, top_n=top)


@router.get("/historial-academico/{estudiante_id}", response_model=List[HistorialAcademico])
def historial_academico(
    estudiante_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Historial académico completo de un estudiante."""
    return ReportesService(db).historial_academico(estudiante_id)


@router.get("/docentes-mas-reprobados", response_model=List[DocenteReprobados])
def docentes_mas_reprobados(
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    """Docentes con mayor número de estudiantes reprobados."""
    return ReportesService(db).docentes_mas_reprobados()
