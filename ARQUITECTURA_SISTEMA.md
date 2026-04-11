# Arquitectura del Sistema - Lector y Extractor de PDFs

## Tabla de Contenidos
1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Flujo de Autenticación](#flujo-de-autenticación)
5. [Flujo de Extracción de PDF](#flujo-de-extracción-de-pdf)
6. [Capas del Backend](#capas-del-backend)
7. [Endpoints](#endpoints)
8. [Dependencias](#dependencias)

---

## Visión General

```
┌─────────────────────────────────────────────────────────────────┐
│                     SISTEMA PDF EXTRACTOR                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Usuario se registra o inicia sesión                        │
│  2. Sistema valida identidad y entrega token JWT               │
│  3. Usuario sube un archivo PDF                                │
│  4. Sistema extrae el texto de cada página en memoria          │
│  5. Sistema retorna el contenido extraído al usuario           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Stack                                                          │
│  ├── Backend:  FastAPI + SQLModel + SQLite / PostgreSQL         │
│  ├── Frontend: React 19 + TypeScript + Vite 8                  │
│  └── Auth:     JWT + bcrypt                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Arquitectura del Sistema

```
┌──────────────────────────────────────────────────────────────────┐
│                     FRONTEND  (React + Vite)                     │
│                                                                  │
│   /login          /dashboard                                     │
│   ┌────────────┐  ┌──────────────────────────────────────────┐  │
│   │ Login.tsx  │  │ Dashboard.tsx                            │  │
│   │ ─────────  │  │ ──────────────────────────────────────── │  │
│   │ Registro   │  │ PdfUpload.tsx  (solo si hay token)       │  │
│   │ Login      │  │ ─────────────────────────────────────    │  │
│   └────────────┘  │ Seleccionar PDF → ver texto extraído     │  │
│                   └──────────────────────────────────────────┘  │
│                                                                  │
│   AuthContext.tsx → guarda token JWT en localStorage            │
│   ProtectedRoute.tsx → redirige a /login si no hay token        │
│   utils/api.ts → agrega token en cada petición automáticamente  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
     Auth (sin token)              PDF (con token Bearer)
              │                             │
              ▼                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                      BACKEND  (FastAPI)                          │
│                                                                  │
│   /api/auth                        /api/pdf                      │
│   ┌──────────────────────────┐     ┌──────────────────────────┐  │
│   │ POST /register           │     │ POST /extract            │  │
│   │ POST /login              │     │ ─────────────────────    │  │
│   │ GET  /me                 │     │ Requiere JWT válido      │  │
│   │ ────────────────────     │     │ Valida archivo PDF       │  │
│   │ Valida credenciales      │     │ Abre en memoria          │  │
│   │ Hashea con bcrypt        │     │ Extrae texto por página  │  │
│   │ Retorna JWT token        │     │ Retorna resultado        │  │
│   └──────────────────────────┘     └──────────────────────────┘  │
│                                                                  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ Solo auth escribe en BD
                             ▼
              ┌──────────────────────────┐
              │    SQLite / PostgreSQL   │
              │  ┌────────────────────┐  │
              │  │  Tabla: users      │  │
              │  │  ─────────────     │  │
              │  │  id                │  │
              │  │  email             │  │
              │  │  username          │  │
              │  │  hashed_password   │  │
              │  │  is_active         │  │
              │  │  created_at        │  │
              │  └────────────────────┘  │
              └──────────────────────────┘
```

---

## Estructura de Carpetas

```
FastApi/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py          [EXISTENTE] endpoints de autenticación
│   │   │   ├── dashboard.py     [EXISTENTE]
│   │   │   ├── pdf.py           [NUEVO]     endpoint de extracción
│   │   │   └── router.py        [ACTUALIZAR] incluir pdf router
│   │   │
│   │   ├── core/
│   │   │   ├── auth.py          [EXISTENTE] JWT, bcrypt, validación token
│   │   │   └── config.py        [EXISTENTE] variables de entorno
│   │   │
│   │   ├── db/
│   │   │   └── session.py       [EXISTENTE] conexión async a BD
│   │   │
│   │   ├── models/
│   │   │   └── user.py          [EXISTENTE] modelo User
│   │   │
│   │   ├── repositories/
│   │   │   └── user.py          [EXISTENTE] consultas a BD
│   │   │
│   │   ├── schemas/
│   │   │   ├── user.py          [EXISTENTE] UserCreate, UserLogin, UserResponse
│   │   │   └── pdf.py           [NUEVO]     PdfPageResponse, PdfExtractResponse
│   │   │
│   │   ├── services/
│   │   │   ├── user.py          [EXISTENTE] lógica de usuarios
│   │   │   └── pdf.py           [NUEVO]     lógica de extracción PDF
│   │   │
│   │   └── main.py              [EXISTENTE] FastAPI + CORS + router
│   │
│   ├── .env
│   └── requirements.txt         [AGREGAR]   pdfplumber, python-multipart
│
└── frontend/
    └── mi-app/src/
        ├── components/
        │   ├── Login.tsx         [EXISTENTE] registro e inicio de sesión
        │   ├── Dashboard.tsx     [EXISTENTE] integrar PdfUpload
        │   ├── Layout.tsx        [EXISTENTE]
        │   ├── ProtectedRoute.tsx[EXISTENTE] guarda rutas privadas
        │   ├── Sidebar.tsx       [EXISTENTE]
        │   ├── Topbar.tsx        [EXISTENTE]
        │   └── PdfUpload.tsx     [NUEVO]     carga y muestra resultado
        │
        ├── contexts/
        │   └── AuthContext.tsx   [EXISTENTE] manejo de token JWT
        │
        ├── types/
        │   ├── api.ts            [EXISTENTE]
        │   └── pdf.ts            [NUEVO]     tipos PdfPage, PdfExtractResponse
        │
        └── utils/
            └── api.ts            [EXISTENTE] axios + interceptor JWT
```

---

## Flujo de Autenticación

```
  USUARIO                  FRONTEND                   BACKEND                    BD
     │                        │                          │                        │
     │── entra a /login ──────▶│                          │                        │
     │                        │                          │                        │
     │                        │                          │                        │
     │  [REGISTRO]            │                          │                        │
     │── llena formulario ───▶│                          │                        │
     │   email, username,     │── POST /api/auth/register ──────────────────────▶│
     │   password             │                          │── hashea password      │
     │                        │                          │── guarda usuario ─────▶│
     │                        │◀─────────────── UserResponse (id, username) ─────│
     │◀── "Ahora inicia sesión"│                          │                        │
     │                        │                          │                        │
     │  [LOGIN]               │                          │                        │
     │── username + password ▶│                          │                        │
     │                        │── POST /api/auth/login ──▶│                        │
     │                        │                          │── busca usuario ──────▶│
     │                        │                          │◀─────────────── User ──│
     │                        │                          │── verifica password    │
     │                        │◀──────── { access_token } ─────────────────────── │
     │                        │── guarda token en        │                        │
     │                        │   localStorage           │                        │
     │◀── redirige a /dashboard│                          │                        │
```

---

## Flujo de Extracción de PDF

```
  USUARIO                  FRONTEND                   BACKEND
     │                        │                          │
     │── selecciona PDF ──────▶│                          │
     │                        │── POST /api/pdf/extract ──▶│
     │                        │   Header: Bearer <token>  │
     │                        │   Body: archivo PDF       │
     │                        │                          │
     │                        │                     ┌────┴────────────────────┐
     │                        │                     │ 1. Verifica JWT token   │
     │                        │                     │    ¿válido?             │
     │                        │                     └────┬──────────┬─────────┘
     │                        │                          │ SÍ       │ NO
     │                        │                          │          ▼
     │                        │                          │     401 Unauthorized
     │                        │                          │
     │                        │                     ┌────┴────────────────────┐
     │                        │                     │ 2. Valida archivo       │
     │                        │                     │    ¿es .pdf?            │
     │                        │                     │    ¿menor a 10MB?       │
     │                        │                     └────┬──────────┬─────────┘
     │                        │                          │ SÍ       │ NO
     │                        │                          │          ▼
     │                        │                          │     400 Bad Request
     │                        │                          │
     │                        │                     ┌────┴────────────────────┐
     │                        │                     │ 3. Lee PDF en memoria   │
     │                        │                     │    BytesIO(content)     │
     │                        │                     │    pdfplumber.open()    │
     │                        │                     └────┬────────────────────┘
     │                        │                          │
     │                        │                     ┌────┴────────────────────┐
     │                        │                     │ 4. Por cada página:     │
     │                        │                     │    · extrae texto       │
     │                        │                     │    · cuenta palabras    │
     │                        │                     └────┬────────────────────┘
     │                        │                          │
     │                        │◀─── { filename,          │
     │                        │       total_pages,        │
     │                        │       pages: [            │
     │                        │         { page_number,    │
     │                        │           text_content,   │
     │                        │           word_count }    │
     │                        │       ] }                 │
     │◀── muestra resultado ──│                          │
```

---

## Capas del Backend

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer                               │
│   auth.py          pdf.py          dashboard.py                 │
│   Recibe peticiones HTTP, valida auth, delega a services        │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                       Service Layer                             │
│   user.py (registro, autenticación)                             │
│   pdf.py  (validación, extracción de texto)                     │
│   Contiene la lógica de negocio                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     Repository Layer                            │
│   user.py  (consultas a BD)                                     │
│   Solo accede a la base de datos                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                       Data Layer                                │
│   models/user.py   → estructura de la tabla users              │
│   schemas/user.py  → forma de los datos de entrada y salida    │
│   schemas/pdf.py   → forma de la respuesta de extracción       │
│   db/session.py    → conexión async a SQLite / PostgreSQL       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Endpoints

| Método | Ruta | Descripción | Auth | Estado |
|--------|------|-------------|------|--------|
| POST | /api/auth/register | Crear usuario (email, username, password) | No | Existente |
| POST | /api/auth/login | Login → retorna JWT token | No | Existente |
| GET | /api/auth/me | Datos del usuario autenticado | Sí | Existente |
| POST | /api/pdf/extract | Extraer texto de un PDF | Sí | Nuevo |

---

## Dependencias

```
BACKEND
├── Existentes
│   ├── fastapi          servidor web
│   ├── sqlmodel         ORM async
│   ├── aiosqlite        driver SQLite async
│   ├── asyncpg          driver PostgreSQL async
│   ├── pydantic-settings variables de entorno
│   ├── PyJWT            generación y validación de tokens
│   ├── bcrypt           hash de contraseñas
│   └── python-dotenv    lectura del .env
│
└── Nuevas a instalar
    ├── pdfplumber       extracción de texto de PDFs
    └── python-multipart recepción de archivos en FastAPI

FRONTEND
└── Existentes
    ├── react + react-dom
    ├── react-router-dom v7
    ├── axios            peticiones HTTP con interceptor JWT
    └── lucide-react     íconos
```

---

## Pendiente / Mejoras recomendadas

```
[ ] Extracción de tablas    → pdfplumber page.extract_tables()
[ ] Extracción de imágenes  → PyMuPDF (fitz)
[ ] Búsqueda en el texto    → filtrar páginas por palabra clave
[ ] Soporte multi-columna   → PDFs con layout complejo
[ ] Mover SECRET_KEY al .env
```
