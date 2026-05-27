import api from './api'

export const programasService = {
  getAll: () => api.get('/programas').then(r => r.data),
  getById: (id) => api.get(`/programas/${id}`).then(r => r.data),
  create: (data) => api.post('/programas', data).then(r => r.data),
  update: (id, data) => api.put(`/programas/${id}`, data).then(r => r.data),
  delete: (id) => api.delete(`/programas/${id}`),
}
