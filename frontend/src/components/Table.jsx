import Loader from './Loader'

/**
 * Tabla reutilizable
 *
 * Props:
 *  - columns: [{ key, label, render? }]
 *  - data: array de objetos
 *  - loading: boolean
 *  - emptyMessage: string
 *  - actions: (row) => ReactNode
 */
export default function Table({ columns, data, loading, emptyMessage = 'No hay datos', actions }) {
  if (loading) return <Loader />

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200">
      <table className="min-w-full divide-y divide-gray-200 bg-white">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((col) => (
              <th key={col.key} className="table-header">
                {col.label}
              </th>
            ))}
            {actions && <th className="table-header text-right">Acciones</th>}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {data.length === 0 ? (
            <tr>
              <td
                colSpan={columns.length + (actions ? 1 : 0)}
                className="text-center py-10 text-gray-400 text-sm"
              >
                {emptyMessage}
              </td>
            </tr>
          ) : (
            data.map((row, idx) => (
              <tr key={row.id ?? idx} className="hover:bg-gray-50 transition-colors">
                {columns.map((col) => (
                  <td key={col.key} className="table-cell">
                    {col.render ? col.render(row) : row[col.key] ?? '—'}
                  </td>
                ))}
                {actions && (
                  <td className="table-cell text-right">
                    {actions(row)}
                  </td>
                )}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
