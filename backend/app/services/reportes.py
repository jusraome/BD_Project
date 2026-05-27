"""
Servicio de Reportes Académicos
=================================
Implementa las 10 consultas de negocio requeridas.

NOTA DISTRIBUCIÓN FUTURA:
En una arquitectura distribuida, estas consultas serían las más complejas:
- Requerirán consultas federadas entre nodos
- Podrían implementarse con FDW (Foreign Data Wrappers)
- O con un sistema de ETL hacia un data warehouse central
- Las consultas de ranking serían candidatas para MapReduce
"""

from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, asc

from app.models.estudiante import Estudiante, EstadoEstudiante
from app.models.programa import ProgramaAcademico
from app.models.docente import Docente
from app.models.asignatura import Asignatura
from app.models.grupo import Grupo, EstadoGrupo
from app.models.matricula import Matricula, EstadoMatricula
from app.models.nota import Nota, EstadoAprobacion
from app.models.pago import PagoMatricula, EstadoPago
from app.schemas.reportes import (
    EstudiantePorPrograma, CargaDocenteItem, PromedioEstudiante,
    EstudianteRiesgo, AsignaturasPerdida, GrupoCupo,
    PagoPendienteItem, RankingEstudiante, HistorialAcademico,
    DocenteReprobados,
)


class ReportesService:
    def __init__(self, db: Session):
        self.db = db

    # ─── 1. Estudiantes por programa ──────────────────────────────────────────
    def estudiantes_por_programa(self) -> List[EstudiantePorPrograma]:
        rows = self.db.execute(
            select(
                ProgramaAcademico.id,
                ProgramaAcademico.nombre,
                func.count(Estudiante.id).label("total"),
                func.count(Estudiante.id).filter(Estudiante.estado == EstadoEstudiante.ACTIVO).label("activos"),
            )
            .outerjoin(Estudiante, Estudiante.programa_id == ProgramaAcademico.id)
            .group_by(ProgramaAcademico.id, ProgramaAcademico.nombre)
            .order_by(ProgramaAcademico.nombre)
        ).all()

        return [
            EstudiantePorPrograma(
                programa_id=r.id,
                programa_nombre=r.nombre,
                total_estudiantes=r.total,
                estudiantes_activos=r.activos,
            )
            for r in rows
        ]

    # ─── 2. Carga académica docente ────────────────────────────────────────────
    def carga_docente(self) -> List[CargaDocenteItem]:
        rows = self.db.execute(
            select(
                Docente.id,
                Docente.nombres,
                Docente.apellidos,
                func.count(Grupo.id.distinct()).label("total_grupos"),
                func.count(Matricula.id).filter(Matricula.estado == EstadoMatricula.ACTIVA).label("total_estudiantes"),
                func.string_agg(Grupo.periodo.distinct(), ", ").label("periodos"),
            )
            .outerjoin(Grupo, Grupo.docente_id == Docente.id)
            .outerjoin(Matricula, Matricula.grupo_id == Grupo.id)
            .group_by(Docente.id, Docente.nombres, Docente.apellidos)
            .order_by(desc("total_grupos"))
        ).all()

        return [
            CargaDocenteItem(
                docente_id=r.id,
                nombres=r.nombres,
                apellidos=r.apellidos,
                total_grupos=r.total_grupos,
                total_estudiantes=r.total_estudiantes,
                periodos=r.periodos or "",
            )
            for r in rows
        ]

    # ─── 3. Promedio académico por estudiante ──────────────────────────────────
    def promedio_por_estudiante(self, programa_id: int = None) -> List[PromedioEstudiante]:
        query = (
            select(
                Estudiante.id,
                Estudiante.codigo,
                Estudiante.nombres,
                Estudiante.apellidos,
                func.round(func.avg(Nota.nota_final), 2).label("promedio"),
                func.count(Nota.id).label("total_materias"),
                func.count(Nota.id).filter(Nota.estado_aprobacion == EstadoAprobacion.APROBADO).label("aprobadas"),
            )
            .outerjoin(Matricula, Matricula.estudiante_id == Estudiante.id)
            .outerjoin(Nota, Nota.matricula_id == Matricula.id)
            .where(Nota.nota_final.isnot(None))
            .group_by(Estudiante.id, Estudiante.codigo, Estudiante.nombres, Estudiante.apellidos)
            .order_by(desc("promedio"))
        )
        if programa_id:
            query = query.where(Estudiante.programa_id == programa_id)

        rows = self.db.execute(query).all()
        return [
            PromedioEstudiante(
                estudiante_id=r.id,
                codigo=r.codigo,
                nombres=r.nombres,
                apellidos=r.apellidos,
                promedio=float(r.promedio) if r.promedio else None,
                total_materias=r.total_materias,
                materias_aprobadas=r.aprobadas,
            )
            for r in rows
        ]

    # ─── 4. Estudiantes en riesgo académico (promedio < 3.5 o materias reprobadas) ──
    def estudiantes_en_riesgo(self) -> List[EstudianteRiesgo]:
        rows = self.db.execute(
            select(
                Estudiante.id,
                Estudiante.codigo,
                Estudiante.nombres,
                Estudiante.apellidos,
                func.round(func.avg(Nota.nota_final), 2).label("promedio"),
                func.count(Nota.id).filter(Nota.estado_aprobacion == EstadoAprobacion.REPROBADO).label("reprobadas"),
            )
            .join(Matricula, Matricula.estudiante_id == Estudiante.id)
            .join(Nota, Nota.matricula_id == Matricula.id)
            .where(
                Estudiante.estado == EstadoEstudiante.ACTIVO,
                Nota.nota_final.isnot(None),
            )
            .group_by(Estudiante.id, Estudiante.codigo, Estudiante.nombres, Estudiante.apellidos)
            .having(
                (func.avg(Nota.nota_final) < 3.5) |
                (func.count(Nota.id).filter(Nota.estado_aprobacion == EstadoAprobacion.REPROBADO) > 0)
            )
            .order_by(asc("promedio"))
        ).all()

        return [
            EstudianteRiesgo(
                estudiante_id=r.id,
                codigo=r.codigo,
                nombres=r.nombres,
                apellidos=r.apellidos,
                promedio=float(r.promedio) if r.promedio else 0.0,
                materias_reprobadas=r.reprobadas,
            )
            for r in rows
        ]

    # ─── 5. Asignaturas con mayor pérdida ──────────────────────────────────────
    def asignaturas_mayor_perdida(self) -> List[AsignaturasPerdida]:
        rows = self.db.execute(
            select(
                Asignatura.id,
                Asignatura.codigo,
                Asignatura.nombre,
                func.count(Nota.id).label("total_matriculados"),
                func.count(Nota.id).filter(Nota.estado_aprobacion == EstadoAprobacion.REPROBADO).label("reprobados"),
            )
            .join(Grupo, Grupo.asignatura_id == Asignatura.id)
            .join(Matricula, Matricula.grupo_id == Grupo.id)
            .join(Nota, Nota.matricula_id == Matricula.id)
            .where(Nota.nota_final.isnot(None))
            .group_by(Asignatura.id, Asignatura.codigo, Asignatura.nombre)
            .having(func.count(Nota.id) > 0)
            .order_by(desc("reprobados"))
        ).all()

        return [
            AsignaturasPerdida(
                asignatura_id=r.id,
                codigo=r.codigo,
                nombre=r.nombre,
                total_matriculados=r.total_matriculados,
                total_reprobados=r.reprobados,
                porcentaje_perdida=round(r.reprobados / r.total_matriculados * 100, 1)
                if r.total_matriculados > 0 else 0.0,
            )
            for r in rows
        ]

    # ─── 6. Grupos cerca al límite de cupo ────────────────────────────────────
    def grupos_cerca_limite_cupo(self, umbral_pct: float = 80.0) -> List[GrupoCupo]:
        rows = self.db.execute(
            select(
                Grupo.id,
                Asignatura.nombre.label("asignatura_nombre"),
                Grupo.periodo,
                Grupo.cupo_maximo,
                func.count(Matricula.id).filter(Matricula.estado == EstadoMatricula.ACTIVA).label("matriculados"),
            )
            .join(Asignatura, Asignatura.id == Grupo.asignatura_id)
            .outerjoin(Matricula, Matricula.grupo_id == Grupo.id)
            .where(Grupo.estado == EstadoGrupo.ACTIVO)
            .group_by(Grupo.id, Asignatura.nombre, Grupo.periodo, Grupo.cupo_maximo)
            .order_by(desc("matriculados"))
        ).all()

        resultado = []
        for r in rows:
            pct = (r.matriculados / r.cupo_maximo * 100) if r.cupo_maximo > 0 else 0
            if pct >= umbral_pct:
                resultado.append(GrupoCupo(
                    grupo_id=r.id,
                    asignatura_nombre=r.asignatura_nombre,
                    periodo=r.periodo,
                    cupo_maximo=r.cupo_maximo,
                    matriculados=r.matriculados,
                    disponibles=r.cupo_maximo - r.matriculados,
                    porcentaje_ocupacion=round(pct, 1),
                ))
        return resultado

    # ─── 7. Pagos pendientes ───────────────────────────────────────────────────
    def pagos_pendientes(self) -> List[PagoPendienteItem]:
        rows = self.db.execute(
            select(
                PagoMatricula.id,
                PagoMatricula.estudiante_id,
                Estudiante.codigo.label("codigo_estudiante"),
                Estudiante.nombres,
                Estudiante.apellidos,
                PagoMatricula.periodo,
                PagoMatricula.valor_pago,
                PagoMatricula.estado_pago,
            )
            .join(Estudiante, Estudiante.id == PagoMatricula.estudiante_id)
            .where(PagoMatricula.estado_pago.in_([EstadoPago.PENDIENTE, EstadoPago.EN_MORA]))
            .order_by(PagoMatricula.estado_pago, Estudiante.apellidos)
        ).all()

        return [
            PagoPendienteItem(
                pago_id=r.id,
                estudiante_id=r.estudiante_id,
                codigo_estudiante=r.codigo_estudiante,
                nombres=r.nombres,
                apellidos=r.apellidos,
                periodo=r.periodo,
                valor_pago=float(r.valor_pago),
                estado_pago=r.estado_pago,
            )
            for r in rows
        ]

    # ─── 8. Ranking de estudiantes ─────────────────────────────────────────────
    def ranking_estudiantes(self, programa_id: int = None, top_n: int = 20) -> List[RankingEstudiante]:
        query = (
            select(
                Estudiante.id,
                Estudiante.codigo,
                Estudiante.nombres,
                Estudiante.apellidos,
                ProgramaAcademico.nombre.label("programa_nombre"),
                func.round(func.avg(Nota.nota_final), 2).label("promedio"),
            )
            .join(ProgramaAcademico, ProgramaAcademico.id == Estudiante.programa_id)
            .join(Matricula, Matricula.estudiante_id == Estudiante.id)
            .join(Nota, Nota.matricula_id == Matricula.id)
            .where(Nota.nota_final.isnot(None))
            .group_by(
                Estudiante.id, Estudiante.codigo, Estudiante.nombres,
                Estudiante.apellidos, ProgramaAcademico.nombre,
            )
            .order_by(desc("promedio"))
            .limit(top_n)
        )
        if programa_id:
            query = query.where(Estudiante.programa_id == programa_id)

        rows = self.db.execute(query).all()
        return [
            RankingEstudiante(
                posicion=idx + 1,
                estudiante_id=r.id,
                codigo=r.codigo,
                nombres=r.nombres,
                apellidos=r.apellidos,
                promedio=float(r.promedio) if r.promedio else 0.0,
                programa_nombre=r.programa_nombre,
            )
            for idx, r in enumerate(rows)
        ]

    # ─── 9. Historial académico de un estudiante ──────────────────────────────
    def historial_academico(self, estudiante_id: int) -> List[HistorialAcademico]:
        rows = self.db.execute(
            select(
                Grupo.periodo,
                Asignatura.codigo.label("asignatura_codigo"),
                Asignatura.nombre.label("asignatura_nombre"),
                Asignatura.creditos,
                Nota.nota_final,
                Nota.estado_aprobacion,
            )
            .join(Matricula, Matricula.estudiante_id == estudiante_id)
            .join(Grupo, Grupo.id == Matricula.grupo_id)
            .join(Asignatura, Asignatura.id == Grupo.asignatura_id)
            .outerjoin(Nota, Nota.matricula_id == Matricula.id)
            .where(Matricula.estudiante_id == estudiante_id)
            .order_by(Grupo.periodo, Asignatura.nombre)
        ).all()

        return [
            HistorialAcademico(
                periodo=r.periodo,
                asignatura_codigo=r.asignatura_codigo,
                asignatura_nombre=r.asignatura_nombre,
                creditos=r.creditos,
                nota_final=float(r.nota_final) if r.nota_final else None,
                estado_aprobacion=r.estado_aprobacion or "pendiente",
            )
            for r in rows
        ]

    # ─── 10. Docentes con más estudiantes reprobados ──────────────────────────
    def docentes_mas_reprobados(self) -> List[DocenteReprobados]:
        rows = self.db.execute(
            select(
                Docente.id,
                Docente.nombres,
                Docente.apellidos,
                func.count(Nota.id).filter(Nota.nota_final.isnot(None)).label("total_estudiantes"),
                func.count(Nota.id).filter(Nota.estado_aprobacion == EstadoAprobacion.REPROBADO).label("reprobados"),
            )
            .join(Grupo, Grupo.docente_id == Docente.id)
            .join(Matricula, Matricula.grupo_id == Grupo.id)
            .join(Nota, Nota.matricula_id == Matricula.id)
            .group_by(Docente.id, Docente.nombres, Docente.apellidos)
            .having(func.count(Nota.id).filter(Nota.nota_final.isnot(None)) > 0)
            .order_by(desc("reprobados"))
        ).all()

        return [
            DocenteReprobados(
                docente_id=r.id,
                nombres=r.nombres,
                apellidos=r.apellidos,
                total_estudiantes=r.total_estudiantes,
                total_reprobados=r.reprobados,
                porcentaje_reprobados=round(r.reprobados / r.total_estudiantes * 100, 1)
                if r.total_estudiantes > 0 else 0.0,
            )
            for r in rows
        ]
