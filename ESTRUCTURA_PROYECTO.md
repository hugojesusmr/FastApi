# 📋 Estructura del Proyecto FastAPI - Guía Completa

## 🎯 Descripción General
Este es un proyecto **FastAPI** con gestión de usuarios, autenticación, carga de archivos y administración de regiones. Utiliza **MySQL** como base de datos, **SQLModel** para ORM, y **Jinja2** para templates HTML.

---

## 📁 Estructura de Carpetas

```
FastApi/
├── alembic/                    # Migraciones de base de datos
│   ├── versions/               # Historial de migraciones
│   ├── env.py                  # Configuración de Alembic
│   └── script.py.mako          # Template para nuevas migraciones
│
├── app/                        # Aplicación principal
│   ├── api/                    # Endpoints de la API
│   │   ├── auth.py             # Endpoints de autenticación
│   │   ├── dashboard.py        # Endpoints del dashboard
│   │   ├── regions.py          # Endpoints de regiones
│   │   └── router.py           # Enrutador principal
│   │
│   ├── core/                   # Configuración central
│   │   ├── auth.py             # Lógica de autenticación
│   │   └── config.py           # Variables de entorno
│   │
│   ├── crud/                   # Operaciones CRUD
│   │   └── region.py           # CRUD de regiones
│   │
│   ├── db/                     # Base de datos
│   │   └── session.py          # Sesión de base de datos
│   │
│   ├── models/                 # Modelos de datos
│   │   └── models.py           # Definición de tablas
│   │
│   ├── schemas/                # Esquemas Pydantic
│   │   └── schemas.py          # Validación de datos
│   │
│   ├── static/                 # Archivos estáticos
│   │   ├── css/                # Estilos CSS
│   │   │   ├── dashboard.css
│   │   │   ├── login.css
│   │   │   └── regions.css
│   │   ├── js/                 # Scripts JavaScript
│   │   │   ├── dashboard.js
│   │   │   ├── login.js
│   │   │   └── regions.js
│   │   └── img/                # Imágenes
│   │
│   ├── templates/              # Templates HTML
│   │   ├── components/         # Componentes reutilizables
│   │   │   ├── sidebar.html
│   │   │   └── topbar.html
│   │   ├── base.html           # Template base
│   │   ├── dashboard.html      # Página del dashboard
│   │   ├── login.html          # Página de login
│   │   ├── regions.html        # Página de regiones
│   │   └── region_detail.html  # Detalle de región
│   │
│   ├── utils/                  # Utilidades
│   │   ├── logica_procesamiento.py
│   │   └── polars_transform.py
│   │
│   └── main.py                 # Punto de entrada de FastAPI
│
├── .env                        # Variables de entorno
├── alembic.ini                 # Configuración de Alembic
├── requirements.txt            # Dependencias Python
├── Dockerfile                  # Configuración Docker
├── entrypoint.sh               # Script de inicio
└── migrate.sh                  # Script de migraciones
```

---

## 🔧 Componentes Principales

### 1️⃣ **Backend - FastAPI**

#### `app/main.py` - Punto de Entrada
```python
- Crea la aplicación FastAPI
- Configura CORS para permitir solicitudes cruzadas
- Monta archivos estáticos (CSS, JS, imágenes)
- Configura Jinja2 para templates
- Define rutas principales:
  - GET / → login.html
  - GET /dashboard → dashboard.html
  - GET /regions → regions.html
  - GET /region-detail → region_detail.html
```

#### `app/core/config.py` - Configuración
```python
- Carga variables de entorno desde .env
- Construye URL de conexión a MySQL
- Variables necesarias:
  - MYSQL_HOST
  - MYSQL_DB_NAME
  - MYSQL_USER
  - MYSQL_PASSWORD
  - MYSQL_PORT
  - TABLE_NAME
```

#### `app/db/session.py` - Conexión a BD
```python
- Crea motor asincrónico de SQLAlchemy
- Configura sesiones AsyncSession
- Proporciona generador get_session() para inyección de dependencias
- Maneja commits y rollbacks automáticos
```

### 2️⃣ **Modelos de Datos**

#### `app/models/models.py`
```python
User:
  - id (PK)
  - email (único)
  - username (único)
  - hashed_password
  - is_active
  - created_at

Region:
  - id (PK)
  - site_code
  - location_name
  - service_panda
  - city
  - state
  - tipo_de_red
  - region
  - coordinador
  - ingeniero
  - km
  - ingenieria
  - kmz
```

### 3️⃣ **API Endpoints**

#### `app/api/router.py` - Enrutador Principal
```python
- Incluye routers de:
  - auth.py (autenticación)
  - dashboard.py (dashboard)
  - regions.py (regiones)
```

#### `app/api/auth.py` - Autenticación
```python
POST /api/auth/register
  - Registra nuevo usuario
  - Valida email y username únicos
  - Hashea contraseña

POST /api/auth/login
  - Valida credenciales
  - Retorna JWT token
```

#### `app/api/regions.py` - Gestión de Regiones
```python
GET /api/regions
  - Lista todas las regiones

POST /api/regions/upload-excel
  - Carga archivo Excel
  - Procesa datos con Polars
  - Inserta en base de datos

GET /api/regions/{id}
  - Obtiene detalle de región
```

#### `app/api/dashboard.py` - Dashboard
```python
GET /api/dashboard/stats
  - Retorna estadísticas generales
  - Archivos procesados, en proceso, errores
```

### 4️⃣ **Frontend - HTML/CSS/JS**

#### Templates HTML
```
base.html
  ├── Estructura base de todas las páginas
  ├── Incluye topbar y sidebar
  └── Define bloques para contenido dinámico

login.html
  ├── Formulario de login/registro
  ├── Validación en cliente
  └── Almacena JWT en localStorage

dashboard.html
  ├── Página principal después de login
  ├── Tabs: Resumen, Cargar, Análisis, Configuración
  └── Gráficos y estadísticas

regions.html
  ├── Tabla de regiones
  ├── Búsqueda y filtros
  └── Carga de archivos Excel

components/
  ├── sidebar.html → Navegación lateral
  └── topbar.html → Barra superior
```

#### Estilos CSS
```
login.css
  - Diseño centrado con efecto 3D
  - Glassmorphism con brillo blanco
  - Inputs y botones estilizados

dashboard.css
  - Layout con sidebar y contenido
  - Cards con efecto 3D
  - Responsive design
  - Scrollbar personalizado

regions.css
  - Tabla de datos
  - Filtros y búsqueda
  - Modal para detalles
```

#### Scripts JavaScript
```
login.js
  - Manejo de formulario de login
  - Validación de datos
  - Almacenamiento de token JWT

dashboard.js
  - Cambio de tabs
  - Carga de archivos con Dropzone
  - Actualización de estadísticas

regions.js
  - Carga de tabla de regiones
  - Filtros y búsqueda
  - Modales de detalle
```

---

## 🔄 Flujo de Datos

### 1. **Autenticación**
```
Usuario → login.html
    ↓
login.js → POST /api/auth/login
    ↓
auth.py → Valida credenciales
    ↓
Retorna JWT token
    ↓
localStorage.setItem('access_token')
    ↓
Redirige a /dashboard
```

### 2. **Carga de Archivos**
```
Usuario → dashboard.html (tab Cargar)
    ↓
Selecciona archivo Excel
    ↓
dashboard.js → POST /api/regions/upload-excel
    ↓
regions.py → Procesa con Polars
    ↓
Inserta en BD (Region)
    ↓
Retorna confirmación
    ↓
Actualiza tabla de regiones
```

### 3. **Visualización de Regiones**
```
Usuario → regions.html
    ↓
regions.js → GET /api/regions
    ↓
regions.py → Consulta BD
    ↓
Retorna lista de regiones
    ↓
Renderiza tabla HTML
    ↓
Aplica filtros y búsqueda
```

---

## 🗄️ Base de Datos

### Conexión
```
Tipo: MySQL
Driver: aiomysql (asincrónico)
ORM: SQLModel (Pydantic + SQLAlchemy)
Migraciones: Alembic
```

### Tablas
```
users
├── id (INT, PK)
├── email (VARCHAR, UNIQUE)
├── username (VARCHAR, UNIQUE)
├── hashed_password (VARCHAR)
├── is_active (BOOLEAN)
└── created_at (DATETIME)

regions
├── id (INT, PK)
├── site_code (VARCHAR)
├── location_name (VARCHAR)
├── service_panda (VARCHAR)
├── city (VARCHAR)
├── state (VARCHAR)
├── tipo_de_red (VARCHAR)
├── region (VARCHAR)
├── coordinador (VARCHAR)
├── ingeniero (VARCHAR)
├── km (FLOAT)
├── ingenieria (VARCHAR)
└── kmz (VARCHAR)
```

---

## 📦 Dependencias Principales

```
FastAPI==0.116.1              # Framework web
SQLAlchemy==2.0.41            # ORM
SQLModel==0.0.24              # Modelos con Pydantic
aiomysql==0.2.0               # Driver MySQL asincrónico
Jinja2==3.1.6                 # Templates HTML
Pydantic==2.10.6              # Validación de datos
python-jose==3.3.0            # JWT tokens
cryptography==45.0.5          # Encriptación
Alembic==1.16.5               # Migraciones BD
Polars==1.0.0                 # Procesamiento de datos
Pandas==2.3.0                 # Análisis de datos
Dropzone.js                   # Carga de archivos (frontend)
```

---

## 🚀 Flujo de Inicio

### 1. **Instalación**
```bash
pip install -r requirements.txt
```

### 2. **Configuración**
```bash
# Crear archivo .env con:
MYSQL_HOST=localhost
MYSQL_DB_NAME=fastapi_db
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_PORT=3306
TABLE_NAME=regions
```

### 3. **Migraciones**
```bash
bash migrate.sh
# O manualmente:
alembic upgrade head
```

### 4. **Ejecución**
```bash
uvicorn app.main:app --reload
# Accede a http://localhost:8000
```

---

## 🎨 Diseño UI/UX

### Características de Diseño
- **Glassmorphism**: Efecto de cristal translúcido
- **Efecto 3D**: Profundidad con sombras y transformaciones
- **Brillo Blanco**: Sombras internas blancas para luminosidad
- **Responsive**: Adaptable a dispositivos móviles
- **Animaciones**: Transiciones suaves y fluidas

### Paleta de Colores
```
Primario: #00d4ff (Azul eléctrico)
Secundario: #0099ff (Azul oscuro)
Fondo: #ffffff (Blanco)
Texto: #2d3748 (Gris oscuro)
Bordes: rgba(0, 212, 255, 0.2)
```

---

## 🔐 Seguridad

### Autenticación
- JWT tokens con expiración
- Contraseñas hasheadas con bcrypt
- CORS configurado

### Validación
- Pydantic schemas para validación
- Validación en cliente y servidor
- Sanitización de inputs

---

## 📝 Notas Importantes

1. **Async/Await**: Todo el código usa operaciones asincrónicas
2. **Inyección de Dependencias**: FastAPI maneja automáticamente las dependencias
3. **Migraciones**: Usar Alembic para cambios en BD
4. **Variables de Entorno**: Nunca commitear .env
5. **CORS**: Configurado para desarrollo, ajustar en producción

---

## 🐳 Docker

```dockerfile
# Dockerfile incluido para containerización
# Construir: docker build -t fastapi-app .
# Ejecutar: docker run -p 8000:8000 fastapi-app
```

---

## 📞 Endpoints Disponibles

```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/regions
POST   /api/regions/upload-excel
GET    /api/regions/{id}
GET    /api/dashboard/stats
GET    /
GET    /dashboard
GET    /regions
GET    /region-detail
```

---

**Última actualización**: 2024
**Versión**: 1.0
