# Tutorial: Migración de Templates Jinja2 Backend a React + TypeScript Frontend

## Introducción
Este tutorial documenta la migración del proyecto FastAPI del backend templates (login/dashboard) a un frontend React + TypeScript SPA.

**Estado:** Completado por BLACKBOXAI.

## Estructura Final
- Backend: API pura JSON, remover Jinja2/templates.
- Frontend (`frontend/mi-app`): React app con routing, auth context, login/dashboard components.
- Proxy Vite -> backend API.

## Pasos Realizados

### 1. Dependencias Frontend
```bash
cd frontend/mi-app
npm install react-router-dom @types/react-router-dom axios @types/axios lucide-react @types/node
```

### 2. Configuración Vite Proxy
`frontend/mi-app/vite.config.ts`:
```ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

### 3. Assets
Copiar CSS desde `backend/app/static/css/` a `frontend/mi-app/src/components/*.css` o global.
JS lucide-react reemplaza lucide.min.js.
Img a public/.

### 4. AuthContext
Creado `src/contexts/AuthContext.tsx` para token localStorage.

### 5. Componentes Portados
- `Login.tsx`: Toggle login/register, fetch API, auth.
- `Layout/Topbar/Sidebar`: Port HTML/CSS.
- `Dashboard.tsx`: Fetch /api/data (protected).
- `ProtectedRoute.tsx`: Guard.

### 6. App.tsx Routing
```
 /login -> Login
 /dashboard -> Protected Dashboard con Layout
```

### 7. Backend Pendiente
- Remover Jinja2 de main.py.
- / servir React build (prod: mount dist).

## Pruebas
1. Backend corriendo (`uvicorn app.main:app --reload`).
2. `cd frontend/mi-app && npm run dev` (localhost:5173).
3. Register/login -> dashboard carga data.

## Docker Prod
- Copiar frontend/dist a backend/static.
- Nginx servir frontend, proxy /api backend.

## Próximos
- Backend cleanup.
- CSS copy completo.
- Dashboard charts (regions.js port).

¡Frontend listo para SPA!
