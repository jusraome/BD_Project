import { useState, useEffect } from 'react'
import api from '../services/api'
import Loader from '../components/Loader'
import { reportesService } from '../services/reportes.service'

function StatCard({ icon, label, value, color }) {
  return (
    <div className={`bg-white rounded-xl border border-gray-200 p-5 flex items-center gap-4`}>
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-2xl ${color}`}>
        {icon}
      </div>
      <div>
        <p className="text-2xl font-bold text-gray-800">{value ?? '—'}</p>
        <p className="text-sm text-gray-500">{label}</p>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [riesgo, setRiesgo] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [estRes, docRes, grpRes, matRes, riesgoData] = await Promise.all([
          api.get('/estudiantes?limit=1'),
          api.get('/docentes?limit=1'),
          api.get('/grupos?limit=1'),
          api.get('/matriculas?limit=1'),
          reportesService.estudiantesRiesgo(),
        ])
        // Contar registros usando los encabezados de paginación no disponibles,
        // en su lugar usar los arrays (con limit=200)
        const [estAll, docAll, grpAll, matAll] = await Promise.all([
          api.get('/estudiantes?limit=200').then(r => r.data),
          api.get('/docentes?limit=200').then(r => r.data),
          api.get('/grupos?limit=200').then(r => r.data),
          api.get('/matriculas?limit=200').then(r => r.data),
        ])
        setStats({
          estudiantes: estAll.length,
          docentes: docAll.length,
          grupos: grpAll.length,
          matriculas: matAll.length,
        })
        setRiesgo(riesgoData.slice(0, 5))
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <Loader />

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p className="text-gray-500 text-sm mt-1">Resumen general del sistema académico</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon="👩‍🎓" label="Estudiantes" value={stats?.estudiantes} color="bg-blue-50" />
        <StatCard icon="👨‍🏫" label="Docentes" value={stats?.docentes} color="bg-green-50" />
        <StatCard icon="🗓️" label="Grupos activos" value={stats?.grupos} color="bg-purple-50" />
        <StatCard icon="📝" label="Matrículas" value={stats?.matriculas} color="bg-orange-50" />
      </div>

      {/* Estudiantes en riesgo */}
      {riesgo.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <h2 className="text-base font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <span>⚠️</span> Estudiantes en riesgo académico
            <span className="ml-auto text-xs text-gray-400 font-normal">Top 5</span>
          </h2>
          <div className="space-y-2">
            {riesgo.map((est) => (
              <div key={est.estudiante_id} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div>
                  <p className="text-sm font-medium text-gray-800">{est.nombres} {est.apellidos}</p>
                  <p className="text-xs text-gray-400">{est.codigo} · {est.materias_reprobadas} reprobada(s)</p>
                </div>
                <span className={`text-sm font-bold px-2 py-1 rounded ${est.promedio < 3.0 ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>
                  {est.promedio?.toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Accesos rápidos */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">
        <h2 className="text-base font-semibold text-gray-800 mb-4">Accesos rápidos</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { label: 'Nuevo estudiante', icon: '➕', href: '/estudiantes' },
            { label: 'Registrar matrícula', icon: '📝', href: '/matriculas' },
            { label: 'Registrar pago', icon: '💰', href: '/pagos' },
            { label: 'Ver grupos', icon: '🗓️', href: '/grupos' },
          ].map((item) => (
            <a
              key={item.label}
              href={item.href}
              className="flex flex-col items-center gap-2 p-4 rounded-lg border border-gray-100 hover:border-primary-300 hover:bg-primary-50 transition-colors text-center"
            >
              <span className="text-2xl">{item.icon}</span>
              <span className="text-xs font-medium text-gray-600">{item.label}</span>
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}
