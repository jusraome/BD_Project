import api from './api'

export const docentesService = {
  getAll: (params) => api.get('/docentes', { params }).then(r => r.data),
  getById: (id) => api.get(`/docentes/${id}`).then(r => r.data),
  create: (data) => api.post('/docentes', data).then(r => r.data),
  update: (id, data) => api.put(`/docentes/${id}`, data).then(r => r.data),
  delete: (id) => api.delete(`/docentes/${id}`),
}
