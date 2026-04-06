# Configuración de React + TypeScript - Ticketmaster Frontend

## 📋 Tabla de Contenidos
1. [Instalación Inicial](#instalación-inicial)
2. [Estructura de Carpetas](#estructura-de-carpetas)
3. [Archivos de Configuración](#archivos-de-configuración)
4. [Tipos TypeScript](#tipos-typescript)
5. [Servicios API](#servicios-api)
6. [Stores (Zustand)](#stores-zustand)
7. [Componentes React](#componentes-react)
8. [Router](#router)
9. [Ejecución](#ejecución)

---

## Instalación Inicial

### Paso 1: Navegar a la carpeta frontend

```bash
cd /home/hugo/proyectos/FastApi/frontend
```

### Paso 2: Instalar dependencias

```bash
npm install
```

### Paso 3: Crear estructura de carpetas

```bash
mkdir -p src/{components,pages,stores,services,types,utils,layouts,assets/{css,images,fonts},router}
```

### Paso 4: Crear archivos iniciales

```bash
touch src/main.tsx
touch src/App.tsx
touch src/index.css
```

---

## Estructura de Carpetas

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── EventCard.tsx
│   │
│   ├── pages/               # Páginas principales
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Events.tsx
│   │   ├── EventDetail.tsx
│   │   ├── Checkout.tsx
│   │   └── Dashboard.tsx
│   │
│   ├── stores/              # Estado global (Zustand)
│   │   ├── authStore.ts
│   │   ├── eventsStore.ts
│   │   └── cartStore.ts
│   │
│   ├── services/            # Servicios API
│   │   ├── api.ts
│   │   ├── authService.ts
│   │   ├── eventsService.ts
│   │   └── ordersService.ts
│   │
│   ├── types/               # Tipos TypeScript
│   │   └── index.ts
│   │
│   ├── utils/               # Utilidades
│   │   ├── constants.ts
│   │   └── helpers.ts
│   │
│   ├── layouts/             # Layouts
│   │   ├── MainLayout.tsx
│   │   └── AuthLayout.tsx
│   │
│   ├── router/              # Configuración de rutas
│   │   └── index.tsx
│   │
│   ├── assets/              # Recursos estáticos
│   │   ├── css/
│   │   ├── images/
│   │   └── fonts/
│   │
│   ├── App.tsx              # Componente principal
│   ├── main.tsx             # Punto de entrada
│   └── index.css            # Estilos globales
│
├── public/                  # Archivos públicos
├── index.html               # HTML principal
├── package.json
├── tsconfig.json
├── vite.config.ts
├── .env.local
└── README.md
```

---

## Archivos de Configuración

### .env.local

```bash
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Ticketmaster
VITE_APP_VERSION=1.0.0
```

### tailwind.config.js

```bash
npx tailwindcss init -p
```

Luego editar `tailwind.config.js`:

```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### postcss.config.js

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

---

## Tipos TypeScript

### src/types/index.ts

```typescript
export interface User {
  id: number
  email: string
  username: string
  is_active: boolean
}

export interface Event {
  id: number
  name: string
  description: string
  venue_id: number
  date_time: string
  total_seats: number
  available_seats: number
  status: 'ACTIVE' | 'CANCELLED' | 'COMPLETED'
  image_url?: string
}

export interface Seat {
  id: number
  event_id: number
  section: string
  row: string
  number: number
  status: 'AVAILABLE' | 'RESERVED' | 'SOLD'
  price: number
}

export interface Reservation {
  id: number
  user_id: number
  event_id: number
  seat_ids: number[]
  status: 'PENDING' | 'CONFIRMED' | 'EXPIRED' | 'CANCELLED'
  expires_at: string
}

export interface Order {
  id: number
  user_id: number
  total_price: number
  status: 'PENDING' | 'PAID' | 'CANCELLED'
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface ApiError {
  detail: string
}
```

---

## Servicios API

### src/services/api.ts

```typescript
import axios, { AxiosInstance } from 'axios'
import { useAuthStore } from '@stores/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiService {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Interceptor para agregar token
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    })

    // Interceptor para manejar errores
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token')
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }
    )
  }

  // Auth
  async register(email: string, username: string, password: string) {
    return this.api.post('/api/auth/register', { email, username, password })
  }

  async login(username: string, password: string) {
    return this.api.post('/api/auth/login', { username, password })
  }

  async getCurrentUser() {
    return this.api.get('/api/auth/me')
  }

  // Events
  async getEvents(filters?: Record<string, any>) {
    return this.api.get('/api/events', { params: filters })
  }

  async getEvent(id: number) {
    return this.api.get(`/api/events/${id}`)
  }

  // Seats
  async getSeats(eventId: number) {
    return this.api.get(`/api/events/${eventId}/seats`)
  }

  // Reservations
  async createReservation(eventId: number, seatIds: number[]) {
    return this.api.post('/api/reservations', {
      event_id: eventId,
      seat_ids: seatIds,
    })
  }

  // Orders
  async createOrder(reservationId: number) {
    return this.api.post('/api/orders', {
      reservation_id: reservationId,
    })
  }

  async getOrder(id: number) {
    return this.api.get(`/api/orders/${id}`)
  }

  // Payments
  async processPayment(orderId: number, amount: number, token: string) {
    return this.api.post('/api/payments', {
      order_id: orderId,
      amount,
      token,
    })
  }
}

export default new ApiService()
```

---

## Stores (Zustand)

### src/stores/authStore.ts

```typescript
import { create } from 'zustand'
import type { User, AuthResponse } from '@types/index'
import apiService from '@services/api'

interface AuthStore {
  user: User | null
  token: string | null
  isLoading: boolean
  error: string | null
  isAuthenticated: boolean
  register: (email: string, username: string, password: string) => Promise<void>
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  fetchCurrentUser: () => Promise<void>
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: localStorage.getItem('access_token'),
  isLoading: false,
  error: null,
  isAuthenticated: !!localStorage.getItem('access_token'),

  register: async (email: string, username: string, password: string) => {
    set({ isLoading: true, error: null })
    try {
      await apiService.register(email, username, password)
      set({ isLoading: false })
    } catch (err: any) {
      const error = err.response?.data?.detail || 'Error en el registro'
      set({ error, isLoading: false })
      throw err
    }
  },

  login: async (username: string, password: string) => {
    set({ isLoading: true, error: null })
    try {
      const response = await apiService.login(username, password)
      const data: AuthResponse = response.data

      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('user', JSON.stringify(data.user))

      set({
        token: data.access_token,
        user: data.user,
        isAuthenticated: true,
        isLoading: false,
      })
    } catch (err: any) {
      const error = err.response?.data?.detail || 'Error en el login'
      set({ error, isLoading: false })
      throw err
    }
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    })
  },

  fetchCurrentUser: async () => {
    const token = localStorage.getItem('access_token')
    if (!token) return

    try {
      const response = await apiService.getCurrentUser()
      set({ user: response.data })
    } catch (err) {
      set({ user: null, token: null, isAuthenticated: false })
    }
  },
}))
```

### src/stores/eventsStore.ts

```typescript
import { create } from 'zustand'
import type { Event, Seat } from '@types/index'
import apiService from '@services/api'

interface EventsStore {
  events: Event[]
  currentEvent: Event | null
  seats: Seat[]
  isLoading: boolean
  error: string | null
  fetchEvents: (filters?: Record<string, any>) => Promise<void>
  fetchEvent: (id: number) => Promise<void>
  fetchSeats: (eventId: number) => Promise<void>
}

export const useEventsStore = create<EventsStore>((set) => ({
  events: [],
  currentEvent: null,
  seats: [],
  isLoading: false,
  error: null,

  fetchEvents: async (filters?: Record<string, any>) => {
    set({ isLoading: true, error: null })
    try {
      const response = await apiService.getEvents(filters)
      set({ events: response.data, isLoading: false })
    } catch (err: any) {
      const error = err.response?.data?.detail || 'Error al cargar eventos'
      set({ error, isLoading: false })
    }
  },

  fetchEvent: async (id: number) => {
    set({ isLoading: true, error: null })
    try {
      const response = await apiService.getEvent(id)
      set({ currentEvent: response.data, isLoading: false })
    } catch (err: any) {
      const error = err.response?.data?.detail || 'Error al cargar evento'
      set({ error, isLoading: false })
    }
  },

  fetchSeats: async (eventId: number) => {
    set({ isLoading: true, error: null })
    try {
      const response = await apiService.getSeats(eventId)
      set({ seats: response.data, isLoading: false })
    } catch (err: any) {
      const error = err.response?.data?.detail || 'Error al cargar asientos'
      set({ error, isLoading: false })
    }
  },
}))
```

---

## Componentes React

### src/components/LoginForm.tsx

```typescript
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@stores/authStore'
import { Mail, Lock } from 'lucide-react'

export const LoginForm: React.FC = () => {
  const navigate = useNavigate()
  const { login, isLoading, error } = useAuthStore()

  const [form, setForm] = useState({
    username: '',
    password: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await login(form.username, form.password)
      navigate('/events')
    } catch (err) {
      console.error('Login failed:', err)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label className="block text-gray-700 font-semibold mb-2">
          Usuario
        </label>
        <div className="flex items-center border border-gray-300 rounded-lg">
          <Mail className="w-5 h-5 text-gray-400 ml-3" />
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            placeholder="tu_usuario"
            className="flex-1 px-4 py-2 outline-none"
            required
          />
        </div>
      </div>

      <div>
        <label className="block text-gray-700 font-semibold mb-2">
          Contraseña
        </label>
        <div className="flex items-center border border-gray-300 rounded-lg">
          <Lock className="w-5 h-5 text-gray-400 ml-3" />
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            placeholder="••••••••"
            className="flex-1 px-4 py-2 outline-none"
            required
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition disabled:opacity-50"
      >
        {isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
      </button>
    </form>
  )
}
```

### src/pages/Login.tsx

```typescript
import React from 'react'
import { Link } from 'react-router-dom'
import { LoginForm } from '@components/LoginForm'

export const Login: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          Ticketmaster
        </h1>

        <LoginForm />

        <p className="text-center mt-4 text-gray-600">
          ¿No tienes cuenta?{' '}
          <Link to="/register" className="text-blue-600 hover:underline font-semibold">
            Regístrate
          </Link>
        </p>
      </div>
    </div>
  )
}
```

---

## Router

### src/router/index.tsx

```typescript
import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@stores/authStore'
import { Login } from '@pages/Login'
import { Register } from '@pages/Register'
import { Events } from '@pages/Events'
import { EventDetail } from '@pages/EventDetail'
import { Checkout } from '@pages/Checkout'

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

export const Router: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/events"
          element={
            <ProtectedRoute>
              <Events />
            </ProtectedRoute>
          }
        />
        <Route
          path="/events/:id"
          element={
            <ProtectedRoute>
              <EventDetail />
            </ProtectedRoute>
          }
        />
        <Route
          path="/checkout"
          element={
            <ProtectedRoute>
              <Checkout />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Navigate to="/events" />} />
      </Routes>
    </BrowserRouter>
  )
}
```

---

## Archivos Principales

### src/main.tsx

```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { Router } from '@router/index'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Router />
  </React.StrictMode>,
)
```

### src/App.tsx

```typescript
import React from 'react'
import { Router } from '@router/index'

const App: React.FC = () => {
  return <Router />
}

export default App
```

### src/index.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', system-ui, sans-serif;
  background-color: #f9fafb;
  color: #1f2937;
}

html {
  scroll-behavior: smooth;
}
```

---

## Ejecución

### Paso 1: Instalar dependencias

```bash
cd /home/hugo/proyectos/FastApi/frontend
npm install
```

### Paso 2: Iniciar servidor de desarrollo

```bash
npm run dev
```

### Paso 3: Acceder a la aplicación

```
Frontend: http://localhost:5173
Backend:  http://localhost:8000
```

---

## Estructura Final del Proyecto

```
ticketmaster/
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── requirements.txt
│   └── main.py
│
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   ├── stores/
    │   ├── services/
    │   ├── types/
    │   ├── router/
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── index.css
    ├── public/
    ├── index.html
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts
    └── .env.local
```

---

## Próximos Pasos

1. ✅ Configurar React + TypeScript
2. ✅ Crear Stores (Zustand)
3. ✅ Crear Servicios (Axios)
4. ⏭️ Crear Componentes de Páginas
5. ⏭️ Implementar Autenticación
6. ⏭️ Implementar Listado de Eventos
7. ⏭️ Implementar Selección de Asientos
8. ⏭️ Implementar Checkout
9. ⏭️ Implementar Pagos (Stripe)
10. ⏭️ Desplegar en Producción

