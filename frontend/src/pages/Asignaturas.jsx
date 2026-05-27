import { useState, useEffect, useCallback } from 'react'
import Table from '../components/Table'
import Modal from '../components/Modal'
import Alert from '../components/Alert'
import { asignaturasService } from '../services/asignaturas.service'
import { programasService } from '../services/programas.service'

const EMPTY_FORM = { codigo: '', nombre: '', creditos: 3, horas_teoricas: 2, horas_practicas: 2, programa_id: '', semestre_sugerido: 1, estado: 'activa' }

export default function Asignaturas() {
  const [data, setData] = useState([])
  const [programas, setProgramas] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [alert, setAlert] = useState(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const [asig, prg] = await Promise.all([asignaturasService.getAll(), programasService.getAll()])
      setData(asig); setProgramas(prg)
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
      const payload = { ...form, programa_id: parseInt(form.programa_id), creditos: parseInt(form.creditos), horas_teoricas: parseInt(form.horas_teoricas), horas_practicas: parseInt(form.horas_practicas), semestre_sugerido: parseInt(form.semestre_sugerido) }
      if (editing) { await asignaturasService.update(editing.id, payload) } else { await asignaturasService.create(payload) }
      setAlert({ type: 'success', message: editing ? 'Actualizada' : 'Creada' })
      closeModal(); fetchData()
    } catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error' }) }
  }

  const handleDelete = async (row) => {
    if (!confirm(`¿Eliminar ${row.nombre}?`)) return
    try { await asignaturasService.delete(row.id); setAlert({ type: 'success', message: 'Eliminada' }); fetchData() }
    catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error' }) }
  }

  const columns = [
    { key: 'codigo', label: 'Código' },
    { key: 'nombre', label: 'Nombre' },
    { key: 'creditos', label: 'Créditos' },
    { key: 'semestre_sugerido', label: 'Semestre' },
    { key: 'programa_id', label: 'Programa', render: r => programas.find(p => p.id === r.programa_id)?.nombre || r.programa_id },
    { key: 'estado', label: 'Estado', render: r => <span className={`px-2 py-0.5 rounded-full text-xs ${r.estado === 'activa' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>{r.estado}</span> },
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-800">📚 Asignaturas</h1>
        <button className="btn-primary" onClick={openCreate}>+ Nueva</button>
      </div>
      {alert && <Alert type={alert.type} message={alert.message} onClose={() => setAlert(null)} />}
      <Table columns={columns} data={data} loading={loading} emptyMessage="No hay asignaturas"
        actions={row => (
          <div className="flex gap-2 justify-end">
            <button onClick={() => openEdit(row)} className="text-xs text-primary-600 hover:underline">Editar</button>
            <button onClick={() => handleDelete(row)} className="text-xs text-red-500 hover:underline">Eliminar</button>
          </div>
        )}
      />
      <Modal isOpen={modalOpen} onClose={closeModal} title={editing ? 'Editar Asignatura' : 'Nueva Asignatura'}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Código *</label>
              <input className="input-field" value={form.codigo} onChange={e => setForm(p => ({ ...p, codigo: e.target.value }))} required disabled={!!editing} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
              <input className="input-field" value={form.nombre} onChange={e => setForm(p => ({ ...p, nombre: e.target.value }))} required /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Créditos</label>
              <input type="number" min="1" max="20" className="input-field" value={form.creditos} onChange={e => setForm(p => ({ ...p, creditos: e.target.value }))} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Horas teóricas</label>
              <input type="number" min="0" className="input-field" value={form.horas_teoricas} onChange={e => setForm(p => ({ ...p, horas_teoricas: e.target.value }))} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Horas prácticas</label>
              <input type="number" min="0" className="input-field" value={form.horas_practicas} onChange={e => setForm(p => ({ ...p, horas_practicas: e.target.value }))} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Semestre sugerido</label>
              <input type="number" min="1" max="12" className="input-field" value={form.semestre_sugerido} onChange={e => setForm(p => ({ ...p, semestre_sugerido: e.target.value }))} /></div>
            <div className="col-span-2"><label className="block text-sm font-medium text-gray-700 mb-1">Programa *</label>
              <select className="input-field" value={form.programa_id} onChange={e => setForm(p => ({ ...p, programa_id: e.target.value }))} required>
                <option value="">— Seleccione —</option>
                {programas.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
              </select></div>
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
