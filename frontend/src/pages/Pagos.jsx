import { useState, useEffect, useCallback } from 'react'
import Table from '../components/Table'
import Modal from '../components/Modal'
import Alert from '../components/Alert'
import { pagosService } from '../services/pagos.service'
import { estudiantesService } from '../services/estudiantes.service'

const ESTADO_PAGO = ['pendiente', 'pagado', 'en_mora', 'parcial', 'anulado']
const MEDIO_PAGO = ['transferencia', 'efectivo', 'tarjeta', 'pse', 'convenio']
const EMPTY_FORM = { estudiante_id: '', periodo: '2024-1', valor_pago: '', estado_pago: 'pendiente', medio_pago: '', referencia: '' }

const estadoBadge = {
  pagado: 'bg-green-100 text-green-700',
  pendiente: 'bg-yellow-100 text-yellow-700',
  en_mora: 'bg-red-100 text-red-700',
  parcial: 'bg-blue-100 text-blue-700',
  anulado: 'bg-gray-100 text-gray-500',
}

export default function Pagos() {
  const [data, setData] = useState([])
  const [estudiantes, setEstudiantes] = useState([])
  const [loading, setLoading] = useState(true)
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [alert, setAlert] = useState(null)
  const [filtro, setFiltro] = useState('todos')

  const fetchData = useCallback(async () => {
    setLoading(true)
    try {
      const [pag, est] = await Promise.all([pagosService.getAll(), estudiantesService.getAll()])
      setData(pag); setEstudiantes(est)
    } catch { setAlert({ type: 'error', message: 'Error al cargar' }) }
    finally { setLoading(false) }
  }, [])

  useEffect(() => { fetchData() }, [fetchData])

  const openCreate = () => { setEditing(null); setForm(EMPTY_FORM); setModalOpen(true) }
  const openEdit = (row) => { setEditing(row); setForm({ ...row, valor_pago: row.valor_pago?.toString() }); setModalOpen(true) }
  const closeModal = () => { setModalOpen(false); setEditing(null) }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const payload = { ...form, estudiante_id: parseInt(form.estudiante_id), valor_pago: parseFloat(form.valor_pago), medio_pago: form.medio_pago || null }
      if (editing) { await pagosService.update(editing.id, payload) } else { await pagosService.create(payload) }
      setAlert({ type: 'success', message: editing ? 'Pago actualizado' : 'Pago registrado' })
      closeModal(); fetchData()
    } catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error' }) }
  }

  const handleDelete = async (row) => {
    if (!confirm('¿Eliminar este pago?')) return
    try { await pagosService.delete(row.id); setAlert({ type: 'success', message: 'Eliminado' }); fetchData() }
    catch (err) { setAlert({ type: 'error', message: err.response?.data?.detail || 'Error' }) }
  }

  const getEstudiante = (id) => { const e = estudiantes.find(e => e.id === id); return e ? `${e.nombres} ${e.apellidos}` : id }

  const filteredData = filtro === 'todos' ? data : data.filter(d => d.estado_pago === filtro)

  const columns = [
    { key: 'estudiante_id', label: 'Estudiante', render: r => getEstudiante(r.estudiante_id) },
    { key: 'periodo', label: 'Período' },
    { key: 'valor_pago', label: 'Valor', render: r => `$${parseFloat(r.valor_pago).toLocaleString('es-CO')}` },
    { key: 'estado_pago', label: 'Estado', render: r => <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${estadoBadge[r.estado_pago] || ''}`}>{r.estado_pago}</span> },
    { key: 'fecha_pago', label: 'Fecha pago', render: r => r.fecha_pago ? new Date(r.fecha_pago).toLocaleDateString('es-CO') : '—' },
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-800">💰 Pagos de Matrícula</h1>
        <button className="btn-primary" onClick={openCreate}>+ Nuevo</button>
      </div>
      {alert && <Alert type={alert.type} message={alert.message} onClose={() => setAlert(null)} />}

      {/* Filtros */}
      <div className="flex gap-2 flex-wrap">
        {['todos', 'pendiente', 'pagado', 'en_mora'].map(f => (
          <button key={f} onClick={() => setFiltro(f)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${filtro === f ? 'bg-primary-600 text-white' : 'bg-white border border-gray-300 text-gray-600 hover:bg-gray-50'}`}>
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      <Table columns={columns} data={filteredData} loading={loading} emptyMessage="No hay pagos"
        actions={row => (
          <div className="flex gap-2 justify-end">
            <button onClick={() => openEdit(row)} className="text-xs text-primary-600 hover:underline">Editar</button>
            <button onClick={() => handleDelete(row)} className="text-xs text-red-500 hover:underline">Eliminar</button>
          </div>
        )}
      />

      <Modal isOpen={modalOpen} onClose={closeModal} title={editing ? 'Editar Pago' : 'Nuevo Pago'}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Estudiante *</label>
              <select className="input-field" value={form.estudiante_id} onChange={e => setForm(p => ({ ...p, estudiante_id: e.target.value }))} required disabled={!!editing}>
                <option value="">— Seleccione —</option>
                {estudiantes.map(e => <option key={e.id} value={e.id}>{e.nombres} {e.apellidos} ({e.codigo})</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Período *</label>
              <input className="input-field" placeholder="2024-1" value={form.periodo} onChange={e => setForm(p => ({ ...p, periodo: e.target.value }))} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Valor *</label>
              <input type="number" min="0" step="0.01" className="input-field" value={form.valor_pago} onChange={e => setForm(p => ({ ...p, valor_pago: e.target.value }))} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select className="input-field" value={form.estado_pago} onChange={e => setForm(p => ({ ...p, estado_pago: e.target.value }))}>
                {ESTADO_PAGO.map(o => <option key={o}>{o}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Medio de pago</label>
              <select className="input-field" value={form.medio_pago} onChange={e => setForm(p => ({ ...p, medio_pago: e.target.value }))}>
                <option value="">— Ninguno —</option>
                {MEDIO_PAGO.map(o => <option key={o}>{o}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Referencia</label>
              <input className="input-field" value={form.referencia} onChange={e => setForm(p => ({ ...p, referencia: e.target.value }))} />
            </div>
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" className="btn-secondary" onClick={closeModal}>Cancelar</button>
            <button type="submit" className="btn-primary">{editing ? 'Guardar' : 'Registrar pago'}</button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
