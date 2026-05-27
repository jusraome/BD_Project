import { useState, useEffect, useCallback } from 'react'
import Table from '../components/Table'
import Modal from '../components/Modal'
import Alert from '../components/Alert'
import { estudiantesService } from '../services/estudiantes.service'
import { programasService } from '../services/programas.service'

const ESTADO_OPTIONS = ['activo', 'inactivo', 'graduado', 'retirado']
const TIPO_DOC_OPTIONS = ['CC', 'TI', 'CE', 'PP']
const EMPTY_FORM = {
  codigo: '', tipo_documento: 'CC', numero_documento: '',
  nombres: '', apellidos: '', correo: '', telefono: '',
  direccion: '', programa_id: '', estado: 'activo',
}

export default function Estudiantes() {
  const [data, setData] = useState([])
  const [programas, setProgramas] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [alert, setAlert] = useState(null)
  const [search, setSearch] = useState('')

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const params = search ? { q: search } : {}
      const [est, prg] = await Promise.all([
        estudiantesService.getAll(params),
        programasService.getAll(),
      ])
      setData(est)
      setProgramas(prg)
    } catch {
      setAlert({ type: 'error', message: 'Error al cargar datos' })
    } finally {
      setLoading(false)
    }
  }, [search])

  useEffect(() => { fetchData() }, [fetchData])

  const openCreate = () => { setEditing(null); setForm(EMPTY_FORM); setModalOpen(true) }
  const openEdit = (row) => { setEditing(row); setForm({ ...row, programa_id: row.programa_id }); setModalOpen(true) }
  const closeModal = () => { setModalOpen(false); setEditing(null); setForm(EMPTY_FORM) }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const payload = { ...form, programa_id: parseInt(form.programa_id) }
      if (editing) {
        await estudiantesService.update(editing.id, payload)
        setAlert({ type: 'success', message: 'Estudiante actualizado' })
      } else {
        await estudiantesService.create(payload)
        setAlert({ type: 'success', message: 'Estudiante creado' })
      }
      closeModal()
      fetchData()
    } catch (err) {
      setAlert({ type: 'error', message: err.response?.data?.detail || 'Error al guardar' })
    }
  }

  const handleDelete = async (row) => {
    if (!confirm(`¿Eliminar al estudiante ${row.nombres} ${row.apellidos}?`)) return
    try {
      await estudiantesService.delete(row.id)
      setAlert({ type: 'success', message: 'Estudiante eliminado' })
      fetchData()
    } catch (err) {
      setAlert({ type: 'error', message: err.response?.data?.detail || 'Error al eliminar' })
    }
  }

  const columns = [
    { key: 'codigo', label: 'Código' },
    { key: 'nombres', label: 'Nombres', render: r => `${r.nombres} ${r.apellidos}` },
    { key: 'correo', label: 'Correo' },
    { key: 'programa_id', label: 'Programa', render: r => programas.find(p => p.id === r.programa_id)?.nombre || r.programa_id },
    {
      key: 'estado', label: 'Estado',
      render: r => (
        <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${r.estado === 'activo' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
          {r.estado}
        </span>
      )
    },
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-800">👩‍🎓 Estudiantes</h1>
        <button className="btn-primary" onClick={openCreate}>+ Nuevo</button>
      </div>

      {alert && <Alert type={alert.type} message={alert.message} onClose={() => setAlert(null)} />}

      {/* Búsqueda */}
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Buscar por nombre, apellido o código..."
          className="input-field max-w-xs"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </div>

      <Table
        columns={columns}
        data={data}
        loading={loading}
        emptyMessage="No hay estudiantes registrados"
        actions={(row) => (
          <div className="flex gap-2 justify-end">
            <button onClick={() => openEdit(row)} className="text-xs text-primary-600 hover:underline">Editar</button>
            <button onClick={() => handleDelete(row)} className="text-xs text-red-500 hover:underline">Eliminar</button>
          </div>
        )}
      />

      {/* Modal */}
      <Modal isOpen={modalOpen} onClose={closeModal} title={editing ? 'Editar Estudiante' : 'Nuevo Estudiante'} size="lg">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Código *</label>
              <input className="input-field" value={form.codigo} onChange={e => setForm(p => ({ ...p, codigo: e.target.value }))} required disabled={!!editing} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tipo documento *</label>
              <select className="input-field" value={form.tipo_documento} onChange={e => setForm(p => ({ ...p, tipo_documento: e.target.value }))}>
                {TIPO_DOC_OPTIONS.map(o => <option key={o}>{o}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nº documento *</label>
              <input className="input-field" value={form.numero_documento} onChange={e => setForm(p => ({ ...p, numero_documento: e.target.value }))} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nombres *</label>
              <input className="input-field" value={form.nombres} onChange={e => setForm(p => ({ ...p, nombres: e.target.value }))} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Apellidos *</label>
              <input className="input-field" value={form.apellidos} onChange={e => setForm(p => ({ ...p, apellidos: e.target.value }))} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Correo *</label>
              <input type="email" className="input-field" value={form.correo} onChange={e => setForm(p => ({ ...p, correo: e.target.value }))} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
              <input className="input-field" value={form.telefono} onChange={e => setForm(p => ({ ...p, telefono: e.target.value }))} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Programa *</label>
              <select className="input-field" value={form.programa_id} onChange={e => setForm(p => ({ ...p, programa_id: e.target.value }))} required>
                <option value="">— Seleccione —</option>
                {programas.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
              </select>
            </div>
            <div className="col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Dirección</label>
              <input className="input-field" value={form.direccion} onChange={e => setForm(p => ({ ...p, direccion: e.target.value }))} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select className="input-field" value={form.estado} onChange={e => setForm(p => ({ ...p, estado: e.target.value }))}>
                {ESTADO_OPTIONS.map(o => <option key={o}>{o}</option>)}
              </select>
            </div>
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" className="btn-secondary" onClick={closeModal}>Cancelar</button>
            <button type="submit" className="btn-primary">{editing ? 'Guardar cambios' : 'Crear estudiante'}</button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
