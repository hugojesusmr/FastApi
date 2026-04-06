# Componentes React + TypeScript - Login

## Instrucciones de Instalación

### Paso 1: Crear estructura de carpetas

```bash
cd /home/hugo/proyectos/FastApi/frontend
mkdir -p src/{components,pages,stores,services,types,utils,layouts,assets/{css,images,fonts},router}
touch src/main.tsx src/App.tsx src/index.css
```

### Paso 2: Instalar dependencias

```bash
npm install
```

### Paso 3: Copiar archivos

Copia los siguientes archivos en sus respectivas ubicaciones.

---

## 1. src/types/index.ts

```typescript
export interface User {
  id: number
  email: string
  username: string
  is_active: boolean
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

## 2. src/services/api.ts

```typescript
import axios, { AxiosInstance } from 'axios'

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

  async register(email: string, username: string, password: string) {
    return this.api.post('/api/auth/register', { email, username, password })
  }

  async login(username: string, password: string) {
    return this.api.post('/api/auth/login', { username, password })
  }

  async getCurrentUser() {
    return this.api.get('/api/auth/me')
  }
}

export default new ApiService()
```

---

## 3. src/stores/authStore.ts

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

---

## 4. src/components/LoginForm.tsx

```typescript
import React, { useState } from 'react'
import { Mail, Lock, Loader } from 'lucide-react'
import { useAuthStore } from '@stores/authStore'

interface LoginFormProps {
  onSuccess?: () => void
  onToggleMode?: () => void
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess, onToggleMode }) => {
  const { login, isLoading } = useAuthStore()
  const [formError, setFormError] = useState<string | null>(null)

  const [form, setForm] = useState({
    username: '',
    password: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
    setFormError(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setFormError(null)

    try {
      await login(form.username, form.password)
      localStorage.setItem('username', form.username)
      onSuccess?.()
    } catch (err: any) {
      setFormError(err.response?.data?.detail || 'Error al iniciar sesión')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {formError && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
          {formError}
        </div>
      )}

      <div className="form-group">
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Usuario
        </label>
        <div className="input-wrapper">
          <div className="icon-box">
            <Mail className="w-5 h-5 text-gray-400" />
          </div>
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            placeholder="tu_usuario"
            className="flex-1 bg-transparent border-none outline-none px-4 py-3 text-gray-700"
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Contraseña
        </label>
        <div className="input-wrapper">
          <div className="icon-box">
            <Lock className="w-5 h-5 text-gray-400" />
          </div>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            placeholder="••••••••"
            className="flex-1 bg-transparent border-none outline-none px-4 py-3 text-gray-700"
            required
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-bold py-3 px-4 rounded-xl transition disabled:opacity-50 flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <Loader className="w-4 h-4 animate-spin" />
            Iniciando sesión...
          </>
        ) : (
          'Iniciar Sesión'
        )}
      </button>

      <div className="text-center mt-4">
        <p className="text-gray-600 text-sm">
          ¿No tienes cuenta?{' '}
          <button
            type="button"
            onClick={onToggleMode}
            className="text-blue-600 hover:text-blue-700 font-semibold"
          >
            Regístrate
          </button>
        </p>
      </div>
    </form>
  )
}
```

---

## 5. src/components/RegisterForm.tsx

```typescript
import React, { useState } from 'react'
import { Mail, Lock, User, Loader } from 'lucide-react'
import { useAuthStore } from '@stores/authStore'

interface RegisterFormProps {
  onSuccess?: () => void
  onToggleMode?: () => void
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess, onToggleMode }) => {
  const { register, isLoading } = useAuthStore()
  const [formError, setFormError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  const [form, setForm] = useState({
    email: '',
    username: '',
    password: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
    setFormError(null)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setFormError(null)
    setSuccessMessage(null)

    try {
      await register(form.email, form.username, form.password)
      setSuccessMessage('Registro exitoso. Ahora puedes iniciar sesión.')
      setForm({ email: '', username: '', password: '' })
      setTimeout(() => {
        onToggleMode?.()
      }, 2000)
    } catch (err: any) {
      setFormError(err.response?.data?.detail || 'Error en el registro')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {formError && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
          {formError}
        </div>
      )}

      {successMessage && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg">
          {successMessage}
        </div>
      )}

      <div className="form-group">
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Email
        </label>
        <div className="input-wrapper">
          <div className="icon-box">
            <Mail className="w-5 h-5 text-gray-400" />
          </div>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            placeholder="tu@email.com"
            className="flex-1 bg-transparent border-none outline-none px-4 py-3 text-gray-700"
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Usuario
        </label>
        <div className="input-wrapper">
          <div className="icon-box">
            <User className="w-5 h-5 text-gray-400" />
          </div>
          <input
            type="text"
            name="username"
            value={form.username}
            onChange={handleChange}
            placeholder="tu_usuario"
            className="flex-1 bg-transparent border-none outline-none px-4 py-3 text-gray-700"
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Contraseña
        </label>
        <div className="input-wrapper">
          <div className="icon-box">
            <Lock className="w-5 h-5 text-gray-400" />
          </div>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            placeholder="••••••••"
            className="flex-1 bg-transparent border-none outline-none px-4 py-3 text-gray-700"
            required
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-bold py-3 px-4 rounded-xl transition disabled:opacity-50 flex items-center justify-center gap-2"
      >
        {isLoading ? (
          <>
            <Loader className="w-4 h-4 animate-spin" />
            Registrando...
          </>
        ) : (
          'Registrarse'
        )}
      </button>

      <div className="text-center mt-4">
        <p className="text-gray-600 text-sm">
          ¿Ya tienes cuenta?{' '}
          <button
            type="button"
            onClick={onToggleMode}
            className="text-blue-600 hover:text-blue-700 font-semibold"
          >
            Inicia sesión
          </button>
        </p>
      </div>
    </form>
  )
}
```

---

## 6. src/pages/Login.tsx

```typescript
import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '@stores/authStore'
import { LoginForm } from '@components/LoginForm'
import { RegisterForm } from '@components/RegisterForm'
import { Codesandbox } from 'lucide-react'

export const Login: React.FC = () => {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()
  const [isLoginMode, setIsLoginMode] = useState(true)

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/events')
    }
  }, [isAuthenticated, navigate])

  const handleLoginSuccess = () => {
    navigate('/events')
  }

  const toggleMode = () => {
    setIsLoginMode(!isLoginMode)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-blue-100 p-3 rounded-2xl">
              <Codesandbox className="w-8 h-8 text-blue-600" />
            </div>
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-500 to-blue-600 bg-clip-text text-transparent mb-2">
            {isLoginMode ? 'Iniciar Sesión' : 'Registrarse'}
          </h1>
          <p className="text-gray-600 text-sm">
            {isLoginMode
              ? 'Ingresa tus credenciales para continuar'
              : 'Crea una nueva cuenta para comenzar'}
          </p>
        </div>

        {/* Forms */}
        {isLoginMode ? (
          <LoginForm onSuccess={handleLoginSuccess} onToggleMode={toggleMode} />
        ) : (
          <RegisterForm onSuccess={handleLoginSuccess} onToggleMode={toggleMode} />
        )}
      </div>
    </div>
  )
}
```

---

## 7. src/router/index.tsx

```typescript
import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@stores/authStore'
import { Login } from '@pages/Login'

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />
}

export const Router: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  )
}
```

---

## 8. src/main.tsx

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

---

## 9. src/App.tsx

```typescript
import React from 'react'
import { Router } from '@router/index'

const App: React.FC = () => {
  return <Router />
}

export default App
```

---

## 10. src/index.css

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

/* Estilos personalizados del login */
.form-group {
  @apply text-left mb-4;
}

.input-wrapper {
  @apply flex items-center bg-gray-100 rounded-xl overflow-hidden transition-all duration-300;
  box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.05), inset -2px -2px 4px rgba(255, 255, 255, 0.8);
}

.input-wrapper:focus-within {
  @apply bg-blue-50;
  box-shadow: inset 2px 2px 4px rgba(0, 0, 0, 0.05), inset -2px -2px 4px rgba(255, 255, 255, 0.8), 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.icon-box {
  @apply flex justify-center items-center w-12 h-12 bg-white bg-opacity-50 border-r border-gray-200;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.animate-shake {
  animation: shake 0.3s ease-in-out;
}
```

---

## Ejecución

```bash
# 1. Instalar dependencias
npm install

# 2. Iniciar servidor de desarrollo
npm run dev

# 3. Acceder a la aplicación
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
```

---

## Estructura Final

```
frontend/
├── src/
│   ├── components/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── pages/
│   │   └── Login.tsx
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
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .env.local
```

