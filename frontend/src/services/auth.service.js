import api from './api'

export const authService = {
  login: async (username, password) => {
    const { data } = await api.post('/auth/login', { username, password })
    return data
  },
  me: async () => {
    const { data } = await api.get('/auth/me')
    return data
  },
}
