import { Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from '../components/ProtectedRoute'
import MainLayout from '../layouts/MainLayout'
import Login from '../pages/Login'
import Dashboard from '../pages/Dashboard'
import Estudiantes from '../pages/Estudiantes'
import Docentes from '../pages/Docentes'
import Asignaturas from '../pages/Asignaturas'
import Grupos from '../pages/Grupos'
import Matriculas from '../pages/Matriculas'
import Pagos from '../pages/Pagos'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route
        path="/"
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="estudiantes" element={<Estudiantes />} />
        <Route path="docentes" element={<Docentes />} />
        <Route path="asignaturas" element={<Asignaturas />} />
        <Route path="grupos" element={<Grupos />} />
        <Route path="matriculas" element={<Matriculas />} />
        <Route path="pagos" element={<Pagos />} />
      </Route>

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
