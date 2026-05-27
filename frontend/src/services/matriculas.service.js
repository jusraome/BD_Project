import api from './api'

export const matriculasService = {
  getAll: (params) => api.get('/matriculas', { params }).then(r => r.data),
  getById: (id) => api.get(`/matriculas/${id}`).then(r => r.data),
  getByEstudiante: (id) => api.get(`/matriculas/estudiante/${id}`).then(r => r.data),
  create: (data) => api.post('/matriculas', data).then(r => r.data),
  update: (id, data) => api.put(`/matriculas/${id}`, data).then(r => r.data),
  cancelar: (id) => api.post(`/matriculas/${id}/cancelar`).then(r => r.data),
}
