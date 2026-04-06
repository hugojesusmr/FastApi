# Instalación de React + TypeScript con Vite

## Requisitos Previos
- Node.js 16+ instalado
- npm o yarn disponible
- Python 3.12+ (para FastAPI)

## Paso 1: Crear Proyecto React + TypeScript

```bash
npm create vite@latest frontend -- --template react-ts
```

Este comando crea un nuevo proyecto con:
- React 18
- TypeScript
- Vite como bundler
- ESLint configurado

## Paso 2: Instalar Dependencias

```bash
cd frontend
npm install
```

## Paso 3: Estructura del Proyecto

```
frontend/
├── src/
│   ├── App.tsx
│   ├── App.css
│   ├── main.tsx
│   ├── vite-env.d.ts
│   └── components/
│       ├── Login.tsx
│       ├── Dashboard.tsx
│       └── Sidebar.tsx
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── eslint.config.js
```

## Paso 4: Configurar Vite para Monorepo

Edita `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api')
      }
    }
  },
  build: {
    outDir: '../backend/app/static/dist',
    emptyOutDir: true,
    sourcemap: false
  }
})
```

## Paso 5: Configurar TypeScript

El archivo `tsconfig.json` ya viene configurado, pero verifica que tenga:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## Paso 6: Instalar Dependencias Adicionales

```bash
npm install axios react-router-dom
npm install -D @types/react @types/react-dom
```

## Paso 7: Comandos Disponibles

```bash
# Desarrollo (hot reload)
npm run dev

# Build para producción
npm run build

# Preview del build
npm preview

# Lint del código
npm run lint
```

## Paso 8: Configurar FastAPI para Servir React

En `backend/app/main.py`, agrega:

```python
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Después de crear la app
app = FastAPI()

# Servir archivos estáticos de React
static_dir = Path(__file__).parent / "static" / "dist"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
```

## Paso 9: Estructura Final del Monorepo

```
FastApi/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── static/
│   │   │   └── dist/  (React compilado aquí)
│   │   ├── api/
│   │   ├── models/
│   │   └── ...
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
└── README.md
```

## Paso 10: Desarrollo Local

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Accede a `http://localhost:5173`

## Paso 11: Build para Producción

```bash
# En la carpeta frontend
npm run build

# Esto compilará React en backend/app/static/dist
# Luego solo necesitas ejecutar FastAPI
cd ../backend
python -m uvicorn app.main:app --port 8000
```

## Ejemplo: Componente Login con TypeScript

`frontend/src/components/Login.tsx`:

```typescript
import { useState } from 'react'
import axios from 'axios'

interface LoginData {
  username: string
  password: string
}

export function Login() {
  const [credentials, setCredentials] = useState<LoginData>({
    username: '',
    password: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await axios.post('/api/auth/login', credentials)
      localStorage.setItem('token', response.data.access_token)
      window.location.href = '/dashboard'
    } catch (err) {
      setError('Credenciales inválidas')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Usuario"
        value={credentials.username}
        onChange={(e) => setCredentials({...credentials, username: e.target.value})}
      />
      <input
        type="password"
        placeholder="Contraseña"
        value={credentials.password}
        onChange={(e) => setCredentials({...credentials, password: e.target.value})}
      />
      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? 'Cargando...' : 'Iniciar Sesión'}
      </button>
    </form>
  )
}
```

## Ventajas de esta Configuración

✅ Hot Module Replacement (HMR) en desarrollo  
✅ TypeScript para type safety  
✅ Proxy automático a FastAPI  
✅ Build optimizado para producción  
✅ Monorepo fácil de mantener  
✅ Separación clara frontend/backend  

## Troubleshooting

**Error: "Cannot find module"**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Puerto 5173 en uso**
```bash
npm run dev -- --port 5174
```

**CORS errors**
Asegúrate que FastAPI tenga CORS configurado:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
