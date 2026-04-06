# Estructura Completa del Proyecto - Backend + Frontend React

## 📋 Tabla de Contenidos
1. [Estructura General](#estructura-general)
2. [Reorganización del Proyecto](#reorganización-del-proyecto)
3. [Backend - FastAPI](#backend---fastapi)
4. [Frontend - React + TypeScript](#frontend---react--typescript)
5. [Configuración de CORS](#configuración-de-cors)
6. [Ejecución del Proyecto](#ejecución-del-proyecto)

---

## Estructura General

### Antes (Monolítico)
```
FastApi/
├── app/
│   ├── static/
│   ├── templates/
│   └── main.py
├── alembic/
└── requirements.txt
```

### Después (Separado)
```
ticketmaster/
├── backend/                    # FastAPI
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── schemas/
│   │   ├── workers/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── .env
│   ├── requirements.txt
│   ├── docker-compose.yml
│   └── README.md
│
└── frontend/                   # React + TypeScript
    ├── src/
    │   ├── components/
    │   │   ├── LoginForm.tsx
    │   │   ├── RegisterForm.tsx
    │   │   └── Header.tsx
    │   ├── pages/
    │   │   ├── Login.tsx
    │   │   ├── Events.tsx
    │   │   └── Dashboard.tsx
    │   ├── stores/
    │   │   └── authStore.ts
    │   ├── services/
    │   │   └── api.ts
    │   ├── types/
    │   │   └── index.ts
    │   ├── router/
    │   │   └── index.tsx
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── index.css
    ├── public/
    ├── index.html
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    ├── .env.local
    └── README.md
```

---

## Reorganización del Proyecto

### Paso 1: Crear estructura de carpetas

```bash
# Navegar a la carpeta raíz
cd /home/hugo/proyectos/FastApi

# Crear carpeta backend y mover archivos
mkdir -p backend
mv app backend/
mv alembic backend/
mv alembic.ini backend/
mv requirements.txt backend/
mv .env backend/
mv docker-compose.yml backend/ 2>/dev/null || true
mv migrate.sh backend/ 2>/dev/null || true
mv clean_migrations.sh backend/ 2>/dev/null || true
mv reset_alembic.py backend/ 2>/dev/null || true

# Crear carpeta frontend (ya existe)
# mkdir -p frontend

# Crear archivos de configuración en backend
touch backend/Dockerfile
touch backend/entrypoint.sh
```

### Paso 2: Actualizar backend/app/main.py

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Ticketmaster API",
    description="API para sistema de venta de boletos",
    version="1.0.0"
)

# Configurar CORS para React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Vite dev server
        "http://localhost:3000",      # Producción local
        "http://localhost:8080",      # Alternativa
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar routers
from app.api.router import api_router

# Incluir routers
app.include_router(api_router)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API is running"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Ticketmaster API",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

### Paso 3: Crear backend/Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Paso 4: Crear backend/docker-compose.yml

```yaml
version: '3.8'

services:
  postgres:
    image: docker.io/library/postgres:15-alpine
    container_name: ticketmaster-postgres
    environment:
      POSTGRES_USER: ticketmaster
      POSTGRES_PASSWORD: tu_contraseña_segura
      POSTGRES_DB: ticketmaster_db
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - ticketmaster-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ticketmaster"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: docker.io/library/redis:7-alpine
    container_name: ticketmaster-redis
    command: redis-server --appendonly yes
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - ticketmaster-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local

networks:
  ticketmaster-network:
    driver: bridge
```

### Paso 5: Crear backend/.env

```bash
# ===== BASE DE DATOS =====
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB_NAME=ticketmaster_db
POSTGRES_USER=ticketmaster
POSTGRES_PASSWORD=tu_contraseña_segura

# ===== REDIS =====
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# ===== APLICACIÓN =====
APP_NAME=Ticketmaster
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# ===== SEGURIDAD =====
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Paso 6: Crear backend/requirements.txt

```
fastapi==0.116.1
uvicorn==0.35.0
sqlalchemy==2.0.43
sqlmodel==0.0.24
asyncpg==0.30.0
alembic==1.16.5
pydantic==2.12.5
pydantic-settings==2.10.1
pydantic-extra-types==2.10.5
email-validator==2.3.0
PyJWT==2.8.1
bcrypt==4.1.2
python-dotenv==1.1.1
redis==5.0.1
celery==5.3.4
flower==2.0.1
stripe==7.8.0
python-multipart==0.0.20
requests==2.31.0
httpx==0.28.1
pytest==7.4.3
pytest-asyncio==0.23.2
pytest-cov==4.1.0
python-json-logger==2.0.7
```

---

## Backend - FastAPI

### Estructura de carpetas backend

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── auth.py
│   │   ├── events.py
│   │   ├── tickets.py
│   │   └── orders.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── auth.py
│   │   └── security.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py
│   │   └── cache.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── event.py
│   │   └── ticket.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── event.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── event.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── event.py
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   └── tasks.py
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_events.py
│
├── .env
├── alembic.ini
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
└── README.md
```

---

## Frontend - React + TypeScript

### Estructura de carpetas frontend

```
frontend/
├── src/
│   ├── components/
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   │
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Events.tsx
│   │   ├── EventDetail.tsx
│   │   ├── Checkout.tsx
│   │   └── Dashboard.tsx
│   │
│   ├── stores/
│   │   ├── authStore.ts
│   │   └── eventsStore.ts
│   │
│   ├── services/
│   │   ├── api.ts
│   │   ├── authService.ts
│   │   └── eventsService.ts
│   │
│   ├── types/
│   │   └── index.ts
│   │
│   ├── utils/
│   │   ├── constants.ts
│   │   └── helpers.ts
│   │
│   ├── router/
│   │   └── index.tsx
│   │
│   ├── assets/
│   │   ├── css/
│   │   ├── images/
│   │   └── fonts/
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
│
├── public/
│   └── favicon.ico
│
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
├── .env.local
└── README.md
```

### Paso 1: Crear frontend/package.json

```json
{
  "name": "ticketmaster-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "zustand": "^4.4.1",
    "axios": "^1.6.2",
    "lucide-react": "^0.292.0",
    "dayjs": "^1.11.10",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8",
    "tailwindcss": "^3.3.6",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16"
  }
}
```

### Paso 2: Crear frontend/.env.local

```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Ticketmaster
VITE_APP_VERSION=1.0.0
```

### Paso 3: Crear frontend/vite.config.ts

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@stores': path.resolve(__dirname, './src/stores'),
      '@services': path.resolve(__dirname, './src/services'),
      '@types': path.resolve(__dirname, './src/types'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@router': path.resolve(__dirname, './src/router'),
      '@assets': path.resolve(__dirname, './src/assets'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
    },
  },
})
```

### Paso 4: Crear frontend/tsconfig.json

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
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@pages/*": ["src/pages/*"],
      "@stores/*": ["src/stores/*"],
      "@services/*": ["src/services/*"],
      "@types/*": ["src/types/*"],
      "@utils/*": ["src/utils/*"],
      "@router/*": ["src/router/*"],
      "@assets/*": ["src/assets/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Paso 5: Crear frontend/index.html

```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Ticketmaster - Venta de Boletos</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

## Configuración de CORS

### Backend - app/main.py (ya configurado arriba)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Ejecución del Proyecto

### Opción 1: Ejecución Manual

#### Terminal 1 - Backend

```bash
# Navegar a backend
cd /home/hugo/proyectos/FastApi/backend

# Activar entorno virtual
source venv/bin/activate

# Levantar contenedores (PostgreSQL y Redis)
podman-compose up -d

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend

```bash
# Navegar a frontend
cd /home/hugo/proyectos/FastApi/frontend

# Instalar dependencias (primera vez)
npm install

# Iniciar servidor de desarrollo
npm run dev
```

### Opción 2: Usando Docker Compose

#### Crear docker-compose.yml en raíz

```yaml
version: '3.8'

services:
  postgres:
    image: docker.io/library/postgres:15-alpine
    container_name: ticketmaster-postgres
    environment:
      POSTGRES_USER: ticketmaster
      POSTGRES_PASSWORD: tu_contraseña_segura
      POSTGRES_DB: ticketmaster_db
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - ticketmaster-network

  redis:
    image: docker.io/library/redis:7-alpine
    container_name: ticketmaster-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - ticketmaster-network

  backend:
    build: ./backend
    container_name: ticketmaster-backend
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_HOST=postgres
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - redis
    networks:
      - ticketmaster-network
    volumes:
      - ./backend:/app

volumes:
  postgres-data:
  redis-data:

networks:
  ticketmaster-network:
    driver: bridge
```

#### Ejecutar con Docker Compose

```bash
# Desde la raíz del proyecto
cd /home/hugo/proyectos/FastApi

# Levantar todos los servicios
podman-compose up -d

# Ver logs
podman-compose logs -f

# Detener servicios
podman-compose down
```

---

## Acceso a la Aplicación

```
Frontend:     http://localhost:5173
Backend API:  http://localhost:8000
API Docs:     http://localhost:8000/docs
Health Check: http://localhost:8000/health
```

---

## Estructura Final del Proyecto

```
/home/hugo/proyectos/FastApi/
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── tests/
│   ├── .env
│   ├── requirements.txt
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── .env.local
│   └── README.md
│
├── docker-compose.yml
└── README.md
```

---

## Próximos Pasos

1. ✅ Reorganizar proyecto en backend y frontend
2. ✅ Configurar React + TypeScript
3. ✅ Configurar CORS
4. ⏭️ Crear componentes React (LoginForm, RegisterForm)
5. ⏭️ Crear páginas React (Login, Events, Dashboard)
6. ⏭️ Implementar autenticación
7. ⏭️ Crear modelos de datos en backend
8. ⏭️ Crear endpoints API
9. ⏭️ Conectar frontend con backend
10. ⏭️ Desplegar en producción

