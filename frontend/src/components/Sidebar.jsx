import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/estudiantes', label: 'Estudiantes', icon: '👩‍🎓' },
  { path: '/docentes', label: 'Docentes', icon: '👨‍🏫' },
  { path: '/asignaturas', label: 'Asignaturas', icon: '📚' },
  { path: '/grupos', label: 'Grupos', icon: '🗓️' },
  { path: '/matriculas', label: 'Matrículas', icon: '📝' },
  { path: '/pagos', label: 'Pagos', icon: '💰' },
]

export default function Sidebar({ isOpen, onClose }) {
  return (
    <>
      {/* Overlay móvil */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/30 z-20 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 h-full w-60 bg-gray-900 text-white z-30 flex flex-col
          transform transition-transform duration-200 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 lg:static lg:flex
        `}
      >
        {/* Header */}
        <div className="px-5 py-5 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🎓</span>
            <div>
              <p className="font-bold text-sm leading-tight">Sistema Académico</p>
              <p className="text-xs text-gray-400">Universitario</p>
            </div>
          </div>
        </div>

        {/* Navegación */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors
                ${isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`
              }
            >
              <span className="text-base">{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="px-4 py-3 border-t border-gray-700">
          <p className="text-xs text-gray-500 text-center">v1.0.0 — 2024</p>
        </div>
      </aside>
    </>
  )
}
