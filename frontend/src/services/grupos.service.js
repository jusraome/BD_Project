import api from './api'

export const gruposService = {
  getAll: (params) => api.get('/grupos', { params }).then(r => r.data),
  getById: (id) => api.get(`/grupos/${id}`).then(r => r.data),
  create: (data) => api.post('/grupos', data).then(r => r.data),
  update: (id, data) => api.put(`/grupos/${id}`, data).then(r => r.data),
  delete: (id) => api.delete(`/grupos/${id}`),
}
