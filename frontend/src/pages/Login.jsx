import { useState } from 'react'
import { useNavigate, Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Alert from '../components/Alert'

export default function Login() {
  const { login, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (isAuthenticated) return <Navigate to="/dashboard" replace />

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(form.username, form.password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Credenciales incorrectas')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-800 to-primary-600 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-8">
        {/* Logo */}
        <div className="text-center mb-8">
          <span className="text-5xl">🎓</span>
          <h1 className="mt-3 text-2xl font-bold text-gray-800">Sistema Académico</h1>
          <p className="text-sm text-gray-500 mt-1">Gestión Universitaria</p>
        </div>

        {error && <Alert type="error" message={error} onClose={() => setError('')} />}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Usuario o correo
            </label>
            <input
              type="text"
              className="input-field"
              placeholder="admin"
              value={form.username}
              onChange={e => setForm(prev => ({ ...prev, username: e.target.value }))}
              required
              autoFocus
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Contraseña
            </label>
            <input
              type="password"
              className="input-field"
              placeholder="••••••••"
              value={form.password}
              onChange={e => setForm(prev => ({ ...prev, password: e.target.value }))}
              required
            />
          </div>

          <button
            type="submit"
            className="btn-primary w-full py-2.5 mt-2"
            disabled={loading}
          >
            {loading ? 'Iniciando sesión...' : 'Iniciar sesión'}
          </button>
        </form>

        <p className="mt-6 text-xs text-center text-gray-400">
          Usuario demo: <strong>admin</strong> / contraseña: <strong>Admin123!</strong>
        </p>
      </div>
    </div>
  )
}
