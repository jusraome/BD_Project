import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { authService } from '../services/auth.service'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)

  // Inicializar desde localStorage al cargar
  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    if (storedToken && storedUser) {
      setToken(storedToken)
      setUser(JSON.parse(storedUser))
    }
    setLoading(false)
  }, [])

  const login = useCallback(async (username, password) => {
    const data = await authService.login(username, password)
    const userData = {
      id: data.usuario_id,
      username: data.username,
      rol: data.rol,
    }
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(userData))
    setToken(data.access_token)
    setUser(userData)
    return userData
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setToken(null)
    setUser(null)
  }, [])

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    isAuthenticated: !!token,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider')
  }
  return context
}
