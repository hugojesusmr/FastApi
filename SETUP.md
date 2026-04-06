# FastAPI + React - Guía de Inicio

## Estructura del Proyecto

Se ha migrado la interfaz del backend (HTML/CSS) a componentes React con la misma estructura visual:

- **Layout.tsx** - Contenedor principal con Topbar y Sidebar
- **Topbar.tsx** - Barra superior con menú y usuario
- **Sidebar.tsx** - Barra lateral de navegación
- **styles/** - Archivos CSS con los estilos del backend

## Requisitos Previos

1. **PostgreSQL** corriendo en `localhost:5432`
   - Usuario: `postgres`
   - Contraseña: `53CR3T00!`
   - Base de datos: `midb`

2. **Node.js** y **npm** instalados

3. **Python 3.8+** instalado

## Instalación

### Backend

```bash
cd /home/hugo/proyectos/FastApi
pip install -r requirements.txt
cd backend
alembic upgrade head
```

### Frontend

```bash
cd /home/hugo/proyectos/FastApi/frontend/mi-app
npm install
```

## Ejecución

### Terminal 1 - Backend

```bash
cd /home/hugo/proyectos/FastApi/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend disponible en: `http://localhost:8000`

### Terminal 2 - Frontend

```bash
cd /home/hugo/proyectos/FastApi/frontend/mi-app
npm run dev
```

Frontend disponible en: `http://localhost:5173`

## Cambios Realizados

### Nuevos Componentes React
- ✅ Layout.tsx - Estructura base con Topbar y Sidebar
- ✅ Topbar.tsx - Barra superior con iconos de Lucide
- ✅ Sidebar.tsx - Navegación lateral con logout

### Nuevos Estilos
- ✅ styles/layout.css - Estilos base y responsive
- ✅ styles/topbar.css - Estilos de la barra superior
- ✅ styles/sidebar.css - Estilos de la barra lateral

### Archivos Creados en Backend
- ✅ app/__init__.py - Paquete Python
- ✅ app/static/index.html - Punto de entrada para SPA

## Características

- 🎨 Diseño Glass Morphism
- 📱 Responsive (Mobile, Tablet, Desktop)
- 🔐 Autenticación con JWT
- 🎯 Navegación con React Router
- 🎭 Iconos con Lucide React
