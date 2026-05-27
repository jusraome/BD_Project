import { useState, useEffect, useCallback } from 'react'
import Table from '../components/Table'
import Modal from '../components/Modal'
import Alert from '../components/Alert'
import { matriculasService } from '../services/matriculas.service'
import { estudiantesService } from '../services/estudiantes.service'
import { gruposService } from '../services/grupos.service'
import { asignaturasService } from '../services/asignaturas.service'

const EMPTY_FORM = { estudiante_id: '', grupo_id: '', estado: 'activa' }

export default function Matriculas() {
  const [data, setData] = useState([])
  const [estudiantes, setEstudiantes] = useState([])
  const [grupos, setGrupos] = useState([])
  const [asignaturas, setAsignaturas] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [form, setForm] = useState(EMPTY_FORM)
  const [alert, setAlert] = useState(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const [mat, est, grp, asig] = await Promise.all([
        matriculasService.getAll(),
        estudiantesService.getAll(),
        gruposService.getAll(),
        asignaturasService.getAll(),
      ])
      setData(mat); setEstudiantes(est); setGrupos(grp); setAsignaturas(asig)
    } catch { setAlert({ type: 'error', message: 'Error al cargar' }) }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  const openCreate = () => { setForm(EMPTY_FORM); setModalOpen(true) }
  const closeModal = () => { setModalOpen(false) }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await matriculasService.create({ ...form, estudiante_id: parseInt(form.estudiante_id), grupo_id: parseInt(form.grupo_id) })
      setAlert({ type: 'success', message: 'Matrícula registrada exitosamente' })
      closeModal(); fetchData()
    } catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error al matricular' }) }
  }

  const handleCancelar = async (row) => {
    if (!confirm('¿Cancelar esta matrícula?')) return
    try { await matriculasService.cancelar(row.id); setAlert({ type: 'success', message: 'Matrícula cancelada' }); fetchData() }
    catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error' }) }
  }

  const getEstudiante = (id) => { const e = estudiantes.find(e => e.id === id); return e ? `${e.nombres} ${e.apellidos}` : id }
  const getGrupo = (id) => {
    const g = grupos.find(g => g.id === id)
    if (!g) return id
    const a = asignaturas.find(a => a.id === g.asignatura_id)
    return `${a?.nombre || 'N/A'} (${g.periodo})`
  }

  const columns = [
    { key: 'estudiante_id', label: 'Estudiante', render: r => getEstudiante(r.estudiante_id) },
    { key: 'grupo_id', label: 'Grupo / Asignatura', render: r => getGrupo(r.grupo_id) },
    { key: 'fecha_matricula', label: 'Fecha', render: r => new Date(r.fecha_matricula).toLocaleDateString('es-CO') },
    { key: 'estado', label: 'Estado', render: r => <span className={`px-2 py-0.5 rounded-full text-xs ${r.estado === 'activa' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-500'}`}>{r.estado}</span> },
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-800">📝 Matrículas</h1>
        <button className="btn-primary" onClick={openCreate}>+ Nueva</button>
      </div>
      {alert && <Alert type={alert.type} message={alert.message} onClose={() => setAlert(null)} />}
      <Table columns={columns} data={data} loading={loading} emptyMessage="No hay matrículas"
        actions={row => row.estado === 'activa' ? (
          <button onClick={() => handleCancelar(row)} className="text-xs text-red-500 hover:underline">Cancelar</button>
        ) : <span className="text-xs text-gray-400">{row.estado}</span>}
      />
      <Modal isOpen={modalOpen} onClose={closeModal} title="Nueva Matrícula">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Estudiante *</label>
            <select className="input-field" value={form.estudiante_id} onChange={e => setForm(p => ({ ...p, estudiante_id: e.target.value }))} required>
              <option value="">— Seleccione un estudiante —</option>
              {estudiantes.filter(e => e.estado === 'activo').map(e => (
                <option key={e.id} value={e.id}>{e.nombres} {e.apellidos} ({e.codigo})</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Grupo *</label>
            <select className="input-field" value={form.grupo_id} onChange={e => setForm(p => ({ ...p, grupo_id: e.target.value }))} required>
              <option value="">— Seleccione un grupo —</option>
              {grupos.filter(g => g.estado === 'activo').map(g => {
                const a = asignaturas.find(a => a.id === g.asignatura_id)
                return <option key={g.id} value={g.id}>{a?.nombre || 'N/A'} — {g.periodo} (Cupo: {g.cupo_maximo})</option>
              })}
            </select>
          </div>
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-xs text-yellow-800">
            ⚠️ El sistema verificará automáticamente el cupo disponible y no permitirá matrículas duplicadas.
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" className="btn-secondary" onClick={closeModal}>Cancelar</button>
            <button type="submit" className="btn-primary">Matricular</button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
