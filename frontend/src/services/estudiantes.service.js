import api from './api'

export const estudiantesService = {
  getAll: (params) => api.get('/estudiantes', { params }).then(r => r.data),
  getById: (id) => api.get(`/estudiantes/${id}`).then(r => r.data),
  create: (data) => api.post('/estudiantes', data).then(r => r.data),
  update: (id, data) => api.put(`/estudiantes/${id}`, data).then(r => r.data),
  delete: (id) => api.delete(`/estudiantes/${id}`),
}
