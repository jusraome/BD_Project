import api from './api'

export const pagosService = {
  getAll: (params) => api.get('/pagos', { params }).then(r => r.data),
  getById: (id) => api.get(`/pagos/${id}`).then(r => r.data),
  getPendientes: () => api.get('/pagos/pendientes').then(r => r.data),
  getByEstudiante: (id) => api.get(`/pagos/estudiante/${id}`).then(r => r.data),
  create: (data) => api.post('/pagos', data).then(r => r.data),
  update: (id, data) => api.put(`/pagos/${id}`, data).then(r => r.data),
  delete: (id) => api.delete(`/pagos/${id}`),
}
