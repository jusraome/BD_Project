export default function Loader({ text = 'Cargando...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin" />
      <p className="mt-3 text-sm text-gray-500">{text}</p>
    </div>
  )
}
