import { useState, useEffect, useCallback } from 'react'
import Table from '../components/Table'
import Modal from '../components/Modal'
import Alert from '../components/Alert'
import { docentesService } from '../services/docentes.service'
import { facultadesService } from '../services/facultades.service'

const CATEGORIA_OPTIONS = ['titular', 'asociado', 'auxiliar', 'catedratico', 'visitante']
const EMPTY_FORM = { nombres: '', apellidos: '', correo: '', telefono: '', categoria: 'catedratico', facultad_id: '', estado: 'activo' }

export default function Docentes() {
  const [data, setData] = useState([])
  const [facultades, setFacultades] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [alert, setAlert] = useState(null)

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const [doc, fac] = await Promise.all([docentesService.getAll(), facultadesService.getAll()])
      setData(doc); setFacultades(fac)
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
      const payload = { ...form, facultad_id: parseInt(form.facultad_id) }
      if (editing) { await docentesService.update(editing.id, payload) } else { await docentesService.create(payload) }
      setAlert({ type: 'success', message: editing ? 'Docente actualizado' : 'Docente creado' })
      closeModal(); fetchData()
    } catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error' }) }
  }

  const handleDelete = async (row) => {
    if (!confirm(`¿Eliminar a ${row.nombres} ${row.apellidos}?`)) return
    try { await docentesService.delete(row.id); setAlert({ type: 'success', message: 'Eliminado' }); fetchData() }
    catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error' }) }
  }

  const columns = [
    { key: 'nombres', label: 'Nombre', render: r => `${r.nombres} ${r.apellidos}` },
    { key: 'correo', label: 'Correo' },
    { key: 'categoria', label: 'Categoría' },
    { key: 'facultad_id', label: 'Facultad', render: r => facultades.find(f => f.id === r.facultad_id)?.nombre || r.facultad_id },
    { key: 'estado', label: 'Estado', render: r => <span className={`px-2 py-0.5 rounded-full text-xs ${r.estado === 'activo' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>{r.estado}</span> },
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-800">👨‍🏫 Docentes</h1>
        <button className="btn-primary" onClick={openCreate}>+ Nuevo</button>
      </div>
      {alert && <Alert type={alert.type} message={alert.message} onClose={() => setAlert(null)} />}
      <Table columns={columns} data={data} loading={loading} emptyMessage="No hay docentes"
        actions={row => (
          <div className="flex gap-2 justify-end">
            <button onClick={() => openEdit(row)} className="text-xs text-primary-600 hover:underline">Editar</button>
            <button onClick={() => handleDelete(row)} className="text-xs text-red-500 hover:underline">Eliminar</button>
          </div>
        )}
      />
      <Modal isOpen={modalOpen} onClose={closeModal} title={editing ? 'Editar Docente' : 'Nuevo Docente'}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Nombres *</label>
              <input className="input-field" value={form.nombres} onChange={e => setForm(p => ({ ...p, nombres: e.target.value }))} required /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Apellidos *</label>
              <input className="input-field" value={form.apellidos} onChange={e => setForm(p => ({ ...p, apellidos: e.target.value }))} required /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Correo *</label>
              <input type="email" className="input-field" value={form.correo} onChange={e => setForm(p => ({ ...p, correo: e.target.value }))} required /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
              <input className="input-field" value={form.telefono} onChange={e => setForm(p => ({ ...p, telefono: e.target.value }))} /></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Categoría</label>
              <select className="input-field" value={form.categoria} onChange={e => setForm(p => ({ ...p, categoria: e.target.value }))}>
                {CATEGORIA_OPTIONS.map(o => <option key={o}>{o}</option>)}
              </select></div>
            <div><label className="block text-sm font-medium text-gray-700 mb-1">Facultad *</label>
              <select className="input-field" value={form.facultad_id} onChange={e => setForm(p => ({ ...p, facultad_id: e.target.value }))} required>
                <option value="">— Seleccione —</option>
                {facultades.map(f => <option key={f.id} value={f.id}>{f.nombre}</option>)}
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
