# 🎓 Sistema de Gestión Académica Universitaria

Sistema web completo para la gestión académica universitaria con arquitectura preparada para distribución de datos en el futuro.

## 📦 Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 |
| Base de datos | PostgreSQL |
| Migraciones | Alembic |
| Autenticación | JWT (python-jose) + Bcrypt |
| Frontend | React 18, Vite, TailwindCSS |
| HTTP Client | Axios |
| Routing | React Router v6 |

---

## 🗂️ Estructura del Proyecto

```
BD_Proyect/
├── backend/
│   ├── app/
│   │   ├── core/          ← Configuración, BD, seguridad, dependencias
│   │   ├── models/        ← Modelos SQLAlchemy
│   │   ├── schemas/       ← Schemas Pydantic (validación)
│   │   ├── repositories/  ← Acceso a datos (patrón Repository)
│   │   ├── services/      ← Lógica de negocio
│   │   ├── routers/       ← Endpoints FastAPI
│   │   └── seed/          ← Datos iniciales
│   ├── alembic/           ← Migraciones de BD
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── src/
    │   ├── components/    ← Componentes reutilizables
    │   ├── pages/         ← Páginas de la app
    │   ├── layouts/       ← Layout principal
    │   ├── routes/        ← Configuración de rutas
    │   ├── services/      ← Llamadas a la API
    │   └── context/       ← Estado global (auth)
    └── package.json
```

---

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+

---

### ⚙️ Backend

#### 1. Crear base de datos en PostgreSQL
```sql
CREATE DATABASE academia_db;
```

#### 2. Configurar variables de entorno
```bash
cd backend
cp .env.example .env
```

Editar `.env` con tus credenciales:
```env
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/academia_db
SECRET_KEY=una-clave-secreta-muy-larga-y-segura-aqui
```

#### 3. Crear entorno virtual e instalar dependencias
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

#### 4. Ejecutar migraciones
```bash
cd backend
alembic upgrade head
```

#### 5. Cargar datos iniciales (seed)
```bash
cd backend
python -m app.seed.seed_data
```

Esto crea:
- 3 Facultades
- 6 Programas académicos
- 10 Docentes
- 15 Asignaturas
- 20 Grupos
- 30 Estudiantes
- Matrículas, notas y pagos de ejemplo
- **Usuarios de prueba** (ver abajo)

#### 6. Iniciar el servidor
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

El backend estará disponible en: **http://localhost:8000**

Documentación Swagger: **http://localhost:8000/docs**

---

### 🖥️ Frontend

#### 1. Instalar dependencias
```bash
cd frontend
npm install
```

#### 2. Iniciar servidor de desarrollo
```bash
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

---

## 👤 Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `admin` | `Admin123!` | Administrador |
| `coordinador1` | `Coord123!` | Coordinador |
| `administrativo1` | `Adm123!` | Administrativo |

---

## 🔌 API Endpoints

### Autenticación
| Método | Endpoint | Descripción |
|--------|---------|-------------|
| POST | `/auth/login` | Iniciar sesión |
| GET | `/auth/me` | Usuario actual |

### Recursos CRUD
| Recurso | Endpoints base |
|---------|---------------|
| Facultades | `/facultades` |
| Programas | `/programas` |
| Estudiantes | `/estudiantes` |
| Docentes | `/docentes` |
| Asignaturas | `/asignaturas` |
| Grupos | `/grupos` |
| Matrículas | `/matriculas` |
| Notas | `/notas` |
| Pagos | `/pagos` |
| Usuarios | `/usuarios` |

Cada recurso soporta: `GET /`, `GET /{id}`, `POST /`, `PUT /{id}`, `DELETE /{id}`

### Reportes Académicos
| Endpoint | Descripción |
|---------|-------------|
| `GET /reportes/estudiantes-por-programa` | Total estudiantes por programa |
| `GET /reportes/carga-docente` | Carga académica por docente |
| `GET /reportes/promedio-estudiantes` | Promedios académicos |
| `GET /reportes/estudiantes-riesgo` | Estudiantes en riesgo |
| `GET /reportes/asignaturas-mayor-perdida` | Asignaturas con mayor pérdida |
| `GET /reportes/grupos-limite-cupo` | Grupos cerca al cupo máximo |
| `GET /reportes/pagos-pendientes` | Pagos pendientes o en mora |
| `GET /reportes/ranking-estudiantes` | Ranking por promedio |
| `GET /reportes/historial-academico/{id}` | Historial de un estudiante |
| `GET /reportes/docentes-mas-reprobados` | Docentes con más reprobados |

---

## 🏗️ Arquitectura

### Patrón por Capas

```
Request → Router → Service → Repository → Database
                  ↕ Lógica     ↕ Acceso
                  de negocio   a datos
```

- **Routers**: solo reciben/devuelven datos HTTP
- **Services**: contienen todas las reglas de negocio
- **Repositories**: única capa que toca SQLAlchemy/SQL
- **Models**: definición de tablas y relaciones
- **Schemas**: validación de entrada/salida (Pydantic)

### Reglas de Negocio Implementadas
- ✅ No se permite sobrecupo en grupos
- ✅ Notas solo entre 0.0 y 5.0
- ✅ Solo estudiantes activos pueden matricularse
- ✅ Solo grupos activos aceptan matrículas
- ✅ No se permiten matrículas duplicadas
- ✅ Correos y códigos únicos validados
- ✅ Nota final calculada automáticamente (30/30/40%)
- ✅ Estado de aprobación automático (≥3.0 = aprobado)

---

## 🔮 Preparación para Distribución Futura

El código está preparado arquitectónicamente para evolucionar hacia:

| Fase | Tecnología | Preparación |
|------|-----------|-------------|
| Réplicas de lectura | PostgreSQL Streaming Replication | `database.py` centralizado |
| Sharding por facultad | Particionamiento | Clave `facultad_id` en modelos |
| Nodo de pagos | PostgreSQL independiente | `PagoMatricula` aislado |
| Historial académico | Solo lectura / OLAP | `Nota` separable |
| Consultas federadas | FDW / Citus | Repositories abstraídos |

**Archivos clave a modificar cuando se distribuya:**
1. `backend/app/core/database.py` → agregar múltiples engines
2. `backend/app/core/config.py` → agregar URLs por nodo
3. `backend/app/repositories/base.py` → enrutamiento de sesión
4. `backend/app/core/dependencies.py` → dependency por facultad

---

## 🛠️ Comandos Útiles

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial de migraciones
alembic history

# Ejecutar seed
python -m app.seed.seed_data

# Correr backend en modo debug
uvicorn app.main:app --reload --log-level debug
```

---

## 📝 Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DATABASE_URL` | URL de conexión PostgreSQL | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Clave para firmar JWT | `cadena-larga-aleatoria` |
| `ALGORITHM` | Algoritmo JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración del token | `60` |
| `DEBUG` | Modo debug | `True` / `False` |
| `ALLOWED_ORIGINS` | CORS origins | `http://localhost:5173` |

---

## 🐛 Solución de Problemas

**Error: "relation does not exist"**
```bash
alembic upgrade head  # Ejecutar migraciones pendientes
```

**Error: "CORS blocked"**
Verificar que `ALLOWED_ORIGINS` en `.env` incluya la URL del frontend.

**Error al hacer login**
Verificar que el seed se haya ejecutado correctamente con `python -m app.seed.seed_data`

**Error: "Module not found"**
Asegurarse de estar en el directorio `backend/` al ejecutar los comandos.
