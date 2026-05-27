import { useState, useEffect, useCallback } from 'react'
import Table from '../components/Table'
import Modal from '../components/Modal'
import Alert from '../components/Alert'
import { gruposService } from '../services/grupos.service'
import { asignaturasService } from '../services/asignaturas.service'
import { docentesService } from '../services/docentes.service'

const EMPTY_FORM = { asignatura_id: '', docente_id: '', periodo: '2024-1', cupo_maximo: 30, horario: '', aula: '', estado: 'activo' }

export default function Grupos() {
  const [data, setData] = useState([])
  const [asignaturas, setAsignaturas] = useState([])
  const [docentes, setDocentes] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [alert, setAlert] = useState(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const [grp, asig, doc] = await Promise.all([gruposService.getAll(), asignaturasService.getAll(), docentesService.getAll()])
      setData(grp); setAsignaturas(asig); setDocentes(doc)
    } catch { setAlert({ type: 'error', message: 'Error al cargar' }) }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  const openCreate = () => { setEditing(null); setForm(EMPTY_FORM); setModalOpen(true) }
  const openEdit = (row) => { setEditing(row); setForm({ ...row }); setModalOpen(true) }
  const closeModal = () => { setModalOpen(false); setEditing(null) }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const payload = { ...form, asignatura_id: parseInt(form.asignatura_id), docente_id: parseInt(form.docente_id), cupo_maximo: parseInt(form.cupo_maximo) }
      if (editing) { await gruposService.update(editing.id, payload) } else { await gruposService.create(payload) }
      setAlert({ type: 'success', message: editing ? 'Grupo actualizado' : 'Grupo creado' })
      closeModal(); fetchData()
    } catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error' }) }
  }

  const handleDelete = async (row) => {
    if (!confirm('¿Eliminar este grupo?')) return
    try { await gruposService.delete(row.id); setAlert({ type: 'success', message: 'Eliminado' }); fetchData() }
    catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error' }) }
  }

  const columns = [
    { key: 'asignatura_id', label: 'Asignatura', render: r => asignaturas.find(a => a.id === r.asignatura_id)?.nombre || r.asignatura_id },
    { key: 'docente_id', label: 'Docente', render: r => { const d = docentes.find(d => d.id === r.docente_id); return d ? `${d.nombres} ${d.apellidos}` : r.docente_id } },
    { key: 'periodo', label: 'Período' },
    { key: 'cupo_maximo', label: 'Cupo' },
    { key: 'aula', label: 'Aula' },
    { key: 'estado', label: 'Estado', render: r => <span className={`px-2 py-0.5 rounded-full text-xs ${r.estado === 'activo' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>{r.estado}</span> },
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-800">🗓️ Grupos</h1>
        <button className="btn-primary" onClick={openCreate}>+ Nuevo</button>
      </div>
      {alert && <Alert type={alert.type} message={alert.message} onClose={() => setAlert(null)} />}
      <Table columns={columns} data={data} loading={loading} emptyMessage="No hay grupos"
        actions={row => (
          <div className="flex gap-2 justify-end">
            <button onClick={() => openEdit(row)} className="text-xs text-primary-600 hover:underline">Editar</button>
            <button onClick={() => handleDelete(row)} className="text-xs text-red-500 hover:underline">Eliminar</button>
          </div>
        )}
      />
      <Modal isOpen={modalOpen} onClose={closeModal} title={editing ? 'Editar Grupo' : 'Nuevo Grupo'}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Asignatura *</label>
              <select className="input-field" value={form.asignatura_id} onChange={e => setForm(p => ({ ...p, asignatura_id: e.target.value }))} required>
                <option value="">— Seleccione —</option>
                {asignaturas.map(a => <option key={a.id} value={a.id}>{a.nombre}</option>)}
              </select></div>
            <div className="col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Docente *</label>
              <select className="input-field" value={form.docente_id} onChange={e => setForm(p => ({ ...p, docente_id: e.target.value }))} required>
                <option value="">— Seleccione —</option>
                {docentes.map(d => <option key={d.id} value={d.id}>{d.nombres} {d.apellidos}</option>)}
              </select></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Período *</label>
              <input className="input-field" placeholder="2024-1" value={form.periodo} onChange={e => setForm(p => ({ ...p, periodo: e.target.value }))} required /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Cupo máximo</label>
              <input type="number" min="1" max="200" className="input-field" value={form.cupo_maximo} onChange={e => setForm(p => ({ ...p, cupo_maximo: e.target.value }))} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Horario</label>
              <input className="input-field" placeholder="L-M-V 8:00-10:00" value={form.horario} onChange={e => setForm(p => ({ ...p, horario: e.target.value }))} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Aula</label>
              <input className="input-field" value={form.aula} onChange={e => setForm(p => ({ ...p, aula: e.target.value }))} /></div>
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" className="btn-secondary" onClick={closeModal}>Cancelar</button>
            <button type="submit" className="btn-primary">{editing ? 'Guardar' : 'Crear'}</button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
