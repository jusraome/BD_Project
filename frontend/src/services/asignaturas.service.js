import api from './api'

export const asignaturasService = {
  getAll: (params) => api.get('/asignaturas', { params }).then(r => r.data),
  getById: (id) => api.get(`/asignaturas/${id}`).then(r => r.data),
  create: (data) => api.post('/asignaturas', data).then(r => r.data),
  update: (id, data) => api.put(`/asignaturas/${id}`, data).then(r => r.data),
  delete: (id) => api.delete(`/asignaturas/${id}`),
}
