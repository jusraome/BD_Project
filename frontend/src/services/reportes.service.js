import api from './api'

export const reportesService = {
  estudiantesPorPrograma: () => api.get('/reportes/estudiantes-por-programa').then(r => r.data),
  cargaDocente: () => api.get('/reportes/carga-docente').then(r => r.data),
  promedioEstudiantes: (params) => api.get('/reportes/promedio-estudiantes', { params }).then(r => r.data),
  estudiantesRiesgo: () => api.get('/reportes/estudiantes-riesgo').then(r => r.data),
  asignaturasMayorPerdida: () => api.get('/reportes/asignaturas-mayor-perdida').then(r => r.data),
  gruposLimiteCupo: () => api.get('/reportes/grupos-limite-cupo').then(r => r.data),
  pagosPendientes: () => api.get('/reportes/pagos-pendientes').then(r => r.data),
  rankingEstudiantes: (params) => api.get('/reportes/ranking-estudiantes', { params }).then(r => r.data),
  historialAcademico: (id) => api.get(`/reportes/historial-academico/${id}`).then(r => r.data),
  docentesMasReprobados: () => api.get('/reportes/docentes-mas-reprobados').then(r => r.data),
}
