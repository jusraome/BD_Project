import api from './api'

export const facultadesService = {
  getAll: () => api.get('/facultades').then(r => r.data),
  getById: (id) => api.get(`/facultades/${id}`).then(r => r.data),
  create: (data) => api.post('/facultades', data).then(r => r.data),
  update: (id, data) => api.put(`/facultades/${id}`, data).then(r => r.data),
  delete: (id) => api.delete(`/facultades/${id}`),
}
