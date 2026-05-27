import { useAuth } from '../context/AuthContext'

const rolLabels = {
  admin: 'Administrador',
  coordinador: 'Coordinador',
  docente: 'Docente',
  estudiante: 'Estudiante',
  administrativo: 'Administrativo',
}

export default function Navbar({ onMenuToggle }) {
  const { user, logout } = useAuth()

  return (
    <nav className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between sticky top-0 z-30">
      {/* Botón menú móvil */}
      <button
        onClick={onMenuToggle}
        className="lg:hidden text-gray-500 hover:text-gray-700 text-xl"
      >
        ☰
      </button>

      {/* Logo */}
      <div className="hidden lg:flex items-center gap-2">
        <span className="text-2xl">🎓</span>
        <span className="font-semibold text-gray-800 text-sm">Sistema Académico</span>
      </div>

      {/* Usuario */}
      <div className="flex items-center gap-3 ml-auto">
        <div className="text-right hidden sm:block">
          <p className="text-sm font-medium text-gray-800">{user?.username}</p>
          <p className="text-xs text-gray-500">{rolLabels[user?.rol] || user?.rol}</p>
        </div>
        <div className="w-9 h-9 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm font-semibold">
          {user?.username?.[0]?.toUpperCase()}
        </div>
        <button
          onClick={logout}
          className="text-sm text-gray-500 hover:text-red-600 transition-colors px-2 py-1 rounded"
          title="Cerrar sesión"
        >
          Salir
        </button>
      </div>
    </nav>
  )
}
