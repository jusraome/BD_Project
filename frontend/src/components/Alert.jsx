import { useState, useEffect } from 'react'

const variants = {
  success: 'bg-green-50 border-green-400 text-green-800',
  error: 'bg-red-50 border-red-400 text-red-800',
  warning: 'bg-yellow-50 border-yellow-400 text-yellow-800',
  info: 'bg-blue-50 border-blue-400 text-blue-800',
}

const icons = {
  success: '✓',
  error: '✕',
  warning: '⚠',
  info: 'ℹ',
}

export default function Alert({ type = 'info', message, onClose, autoClose = 4000 }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    if (autoClose) {
      const t = setTimeout(() => {
        setVisible(false)
        onClose?.()
      }, autoClose)
      return () => clearTimeout(t)
    }
  }, [autoClose, onClose])

  if (!visible || !message) return null

  return (
    <div className={`flex items-center gap-3 border-l-4 p-4 rounded-r-lg mb-4 ${variants[type]}`}>
      <span className="font-bold text-lg">{icons[type]}</span>
      <p className="flex-1 text-sm font-medium">{message}</p>
      <button onClick={() => { setVisible(false); onClose?.() }} className="text-current opacity-60 hover:opacity-100">
        ✕
      </button>
    </div>
  )
}
