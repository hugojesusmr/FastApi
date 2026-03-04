# 🏗️ Diseño Arquitectónico - FastAPI Project

## 📚 Índice
1. [Principios SOLID](#principios-solid)
2. [Patrones de Diseño](#patrones-de-diseño)
3. [Arquitectura General](#arquitectura-general)
4. [Diagramas UML](#diagramas-uml)
5. [Flujos de Datos](#flujos-de-datos)

---

## 🎯 PRINCIPIOS SOLID

### 1. Single Responsibility Principle (SRP)

**Concepto**: Cada clase debe tener una única responsabilidad

```
┌─────────────────────────────────────────────────┐
│         Aplicación FastAPI                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  app/core/config.py                      │   │
│  │  Responsabilidad: Cargar configuración   │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  app/db/session.py                       │   │
│  │  Responsabilidad: Gestionar conexión BD  │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  app/core/auth.py                        │   │
│  │  Responsabilidad: Autenticación y JWT    │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  app/crud/user.py                        │   │
│  │  Responsabilidad: Operaciones CRUD User  │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  app/api/auth.py                         │   │
│  │  Responsabilidad: Endpoints de auth      │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 2. Open/Closed Principle (OCP)

**Concepto**: Abierto para extensión, cerrado para modificación

```
┌─────────────────────────────────────────────────┐
│         Base Repository (Abstracta)             │
├─────────────────────────────────────────────────┤
│  - create()                                     │
│  - read()                                       │
│  - update()                                     │
│  - delete()                                     │
└─────────────────────────────────────────────────┘
         ▲                    ▲
         │                    │
    ┌────┴────┐          ┌────┴────┐
    │          │          │         │
    │ UserRepo │          │RegionRepo
    │          │          │         │
    └──────────┘          └─────────┘
    
Extensión sin modificación de la base
```

### 3. Liskov Substitution Principle (LSP)

**Concepto**: Las subclases deben ser intercambiables por sus superclases

```
┌──────────────────────────────────────┐
│      BaseRepository<T>               │
├──────────────────────────────────────┤
│  async def create(item: T) -> T      │
│  async def get(id: int) -> T         │
│  async def update(item: T) -> T      │
│  async def delete(id: int) -> bool   │
└──────────────────────────────────────┘
         ▲
         │ Implementa
         │
    ┌────┴──────────────────┐
    │                       │
┌───┴────────┐      ┌──────┴────┐
│ UserRepo   │      │ RegionRepo │
│ (User)     │      │ (Region)   │
└────────────┘      └────────────┘

Ambas pueden usarse donde se espera BaseRepository
```

### 4. Interface Segregation Principle (ISP)

**Concepto**: Muchas interfaces específicas es mejor que una general

```
┌─────────────────────────────────────┐
│  ❌ MALO: IRepository (muy grande)  │
├─────────────────────────────────────┤
│  - create()                         │
│  - read()                           │
│  - update()                         │
│  - delete()                         │
│  - search()                         │
│  - export()                         │
│  - import()                         │
│  - validate()                       │
└─────────────────────────────────────┘

┌──────────────────────────────────────┐
│  ✅ BUENO: Interfaces Segregadas     │
├──────────────────────────────────────┤
│  ICreatable                          │
│  ├─ create()                         │
│                                      │
│  IReadable                           │
│  ├─ read()                           │
│  ├─ search()                         │
│                                      │
│  IUpdatable                          │
│  ├─ update()                         │
│                                      │
│  IDeletable                          │
│  ├─ delete()                         │
└──────────────────────────────────────┘
```

### 5. Dependency Inversion Principle (DIP)

**Concepto**: Depender de abstracciones, no de implementaciones concretas

```
┌─────────────────────────────────────┐
│  ❌ MALO: Dependencia Directa       │
├─────────────────────────────────────┤
│                                     │
│  UserService                        │
│      │                              │
│      └──→ MySQLUserRepository       │
│           (Acoplado)                │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  ✅ BUENO: Inyección de Dependencias│
├─────────────────────────────────────┤
│                                     │
│  UserService                        │
│      │                              │
│      └──→ IUserRepository (Interfaz)│
│           ▲                         │
│           │ Implementa              │
│           │                         │
│      MySQLUserRepository            │
│      (Desacoplado)                  │
│                                     │
└─────────────────────────────────────┘
```

---

## 🎨 PATRONES DE DISEÑO

### 1. Repository Pattern

**Propósito**: Abstraer la lógica de acceso a datos

```
┌──────────────────────────────────────────┐
│         Capa de Aplicación               │
│  (UserService, RegionService)            │
└──────────────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────┐
│      Repository Pattern                  │
│  ┌────────────────────────────────────┐  │
│  │  IUserRepository (Interfaz)        │  │
│  │  - create_user()                   │  │
│  │  - get_user()                      │  │
│  │  - update_user()                   │  │
│  │  - delete_user()                   │  │
│  └────────────────────────────────────┘  │
│           ▲                               │
│           │ Implementa                    │
│           │                               │
│  ┌────────┴────────────────────────────┐ │
│  │  MySQLUserRepository                │ │
│  │  - create_user()                    │ │
│  │  - get_user()                       │ │
│  │  - update_user()                    │ │
│  │  - delete_user()                    │ │
│  └─────────────────────────────────────┘ │
└──────────────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────┐
│      Capa de Datos                       │
│  (SQLAlchemy, MySQL)                     │
└──────────────────────────────────────────┘
```

### 2. Service Layer Pattern

**Propósito**: Encapsular lógica de negocio

```
┌──────────────────────────────────────────┐
│         API Endpoints                    │
│  (auth.py, regions.py)                   │
└──────────────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────┐
│      Service Layer                       │
│  ┌────────────────────────────────────┐  │
│  │  UserService                       │  │
│  │  - register_user()                 │  │
│  │  - authenticate_user()             │  │
│  │  - validate_credentials()          │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  RegionService                     │  │
│  │  - create_region()                 │  │
│  │  - get_regions()                   │  │
│  │  - process_excel()                 │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────┐
│      Repository Layer                    │
│  (CRUD operations)                       │
└──────────────────────────────────────────┘
```

### 3. Dependency Injection Pattern

**Propósito**: Inyectar dependencias en lugar de crearlas

```
┌──────────────────────────────────────────┐
│         FastAPI Dependency Injection     │
├──────────────────────────────────────────┤
│                                          │
│  @app.get("/users")                      │
│  async def get_users(                    │
│      session: Session = Depends(         │
│          get_session                     │
│      )                                    │
│  ):                                       │
│      # session inyectada automáticamente │
│      return await user_repo.get_all()    │
│                                          │
└──────────────────────────────────────────┘

Ventajas:
✓ Desacoplamiento
✓ Testeable
✓ Flexible
✓ Reutilizable
```

### 4. Factory Pattern

**Propósito**: Crear objetos sin especificar sus clases concretas

```
┌──────────────────────────────────────────┐
│      RepositoryFactory                   │
├──────────────────────────────────────────┤
│                                          │
│  def create_repository(type: str):       │
│      if type == "user":                  │
│          return UserRepository()         │
│      elif type == "region":              │
│          return RegionRepository()       │
│      else:                               │
│          raise ValueError()              │
│                                          │
└──────────────────────────────────────────┘

Uso:
repo = RepositoryFactory.create_repository("user")
```

### 5. Strategy Pattern

**Propósito**: Encapsular algoritmos intercambiables

```
┌──────────────────────────────────────────┐
│      IAuthStrategy (Interfaz)            │
│  - authenticate()                        │
└──────────────────────────────────────────┘
         ▲
         │ Implementa
         │
    ┌────┴──────────────────┐
    │                       │
┌───┴──────────┐    ┌──────┴────────┐
│ JWTStrategy  │    │ OAuth2Strategy │
│              │    │                │
└──────────────┘    └────────────────┘

Permite cambiar estrategia en tiempo de ejecución
```

---

## 🏛️ ARQUITECTURA GENERAL

### Arquitectura en Capas

```
┌─────────────────────────────────────────────────────┐
│              Presentation Layer                     │
│  (HTML, CSS, JavaScript - Frontend)                 │
└─────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────┐
│              API Layer                              │
│  (FastAPI Endpoints - auth.py, regions.py)          │
└─────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────┐
│              Service Layer                          │
│  (Lógica de Negocio - UserService, RegionService)   │
└─────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────┐
│              Repository Layer                       │
│  (Acceso a Datos - UserRepository, RegionRepository)│
└─────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────┐
│              Data Layer                             │
│  (Base de Datos - MySQL)                            │
└─────────────────────────────────────────────────────┘
```

### Estructura de Carpetas Según Arquitectura

```
app/
├── api/                    # Presentation Layer
│   ├── auth.py            # Endpoints de autenticación
│   ├── regions.py         # Endpoints de regiones
│   └── router.py          # Enrutador principal
│
├── services/              # Service Layer
│   ├── user_service.py    # Lógica de usuarios
│   └── region_service.py  # Lógica de regiones
│
├── repositories/          # Repository Layer
│   ├── base.py            # Repositorio base
│   ├── user_repo.py       # Repositorio de usuarios
│   └── region_repo.py     # Repositorio de regiones
│
├── models/                # Data Layer
│   └── models.py          # Modelos SQLModel
│
├── schemas/               # Validación
│   └── schemas.py         # Esquemas Pydantic
│
├── core/                  # Configuración
│   ├── config.py          # Variables de entorno
│   └── auth.py            # Lógica de autenticación
│
└── db/                    # Conexión BD
    └── session.py         # Sesión de BD
```

---

## 📊 DIAGRAMAS UML

### Diagrama de Clases - Autenticación

```
┌─────────────────────────────────────┐
│         User (Modelo)               │
├─────────────────────────────────────┤
│ - id: int                           │
│ - email: str                        │
│ - username: str                     │
│ - hashed_password: str              │
│ - is_active: bool                   │
│ - created_at: datetime              │
├─────────────────────────────────────┤
│ + get_id(): int                     │
│ + is_active(): bool                 │
└─────────────────────────────────────┘
         ▲
         │ Usa
         │
┌─────────────────────────────────────┐
│    UserRepository (Interfaz)        │
├─────────────────────────────────────┤
│ + create_user(): User               │
│ + get_user_by_id(): User            │
│ + get_user_by_username(): User      │
│ + update_user(): User               │
│ + delete_user(): bool               │
└─────────────────────────────────────┘
         ▲
         │ Implementa
         │
┌─────────────────────────────────────┐
│  MySQLUserRepository                │
├─────────────────────────────────────┤
│ - session: AsyncSession             │
├─────────────────────────────────────┤
│ + create_user(): User               │
│ + get_user_by_id(): User            │
│ + get_user_by_username(): User      │
│ + update_user(): User               │
│ + delete_user(): bool               │
└─────────────────────────────────────┘
         ▲
         │ Usa
         │
┌─────────────────────────────────────┐
│      UserService                    │
├─────────────────────────────────────┤
│ - user_repo: UserRepository         │
│ - auth_service: AuthService         │
├─────────────────────────────────────┤
│ + register_user(): User             │
│ + authenticate_user(): Token        │
│ + validate_credentials(): bool      │
└─────────────────────────────────────┘
         ▲
         │ Usa
         │
┌─────────────────────────────────────┐
│      AuthEndpoints                  │
├─────────────────────────────────────┤
│ - user_service: UserService         │
├─────────────────────────────────────┤
│ + POST /register                    │
│ + POST /login                       │
└─────────────────────────────────────┘
```

### Diagrama de Secuencia - Login

```
Usuario          Frontend         API            Service         Repository       BD
  │                 │              │                │                │            │
  │─ Ingresa ──────→│              │                │                │            │
  │  credenciales   │              │                │                │            │
  │                 │              │                │                │            │
  │                 │─ POST /login→│                │                │            │
  │                 │              │                │                │            │
  │                 │              │─ authenticate→ │                │            │
  │                 │              │                │                │            │
  │                 │              │─ get_user ────→│                │            │
  │                 │              │                │─ SELECT ──────→│            │
  │                 │              │                │                │─ Query ───→│
  │                 │              │                │                │←─ User ────│
  │                 │              │                │←─ User ────────│            │
  │                 │              │                │                │            │
  │                 │              │─ verify_pwd ──→│                │            │
  │                 │              │                │                │            │
  │                 │              │← JWT Token ────│                │            │
  │                 │← Token ──────│                │                │            │
  │                 │              │                │                │            │
  │←─ Token ────────│              │                │                │            │
  │                 │              │                │                │            │
```

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Application                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │         API Layer                                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │ auth.py  │  │regions.py│  │dashboard │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘        │   │
│  └──────────────────────────────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────┴──────────────────────────┐    │
│  │         Service Layer                           │    │
│  │  ┌──────────────┐  ┌──────────────┐             │    │
│  │  │ UserService  │  │RegionService │             │    │
│  │  └──────────────┘  └──────────────┘             │    │
│  └──────────────────────┬──────────────────────────┘    │
│                         │                               │
│  ┌──────────────────────┴──────────────────────────┐    │
│  │      Repository Layer                           │    │
│  │  ┌──────────────┐  ┌──────────────┐             │    │
│  │  │ UserRepository│ │RegionRepository            │    │
│  │  └──────────────┘  └──────────────┘             │    │
│  └──────────────────────┬──────────────────────────┘    │
│                         │                               │
│  ┌──────────────────────┴──────────────────────────┐    │
│  │      Core Layer                                 │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │    │
│  │  │ config.py│  │ auth.py  │  │session.py│       │    │
│  │  └──────────┘  └──────────┘  └──────────┘       │    │
│  └──────────────────────┬──────────────────────────┘    │
│                         │                               │
└─────────────────────────┼───────────────────────────────┘
                          │
                          ↓
                  ┌──────────────────┐
                  │  MySQL Database  │
                  └──────────────────┘
```

---

## 🔄 FLUJOS DE DATOS

### Flujo de Registro

```
┌─────────────────────────────────────────────────────────┐
│  1. Usuario Ingresa Datos                               │
│     (email, username, password)                         │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. Frontend Valida (Pydantic Schema)                   │
│     - Email válido                                      │
│     - Username no vacío                                 │
│     - Password cumple requisitos                        │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. API Endpoint (POST /api/auth/register)              │
│     - Recibe datos validados                            │
│     - Llama a UserService.register_user()               │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. Service Layer (UserService)                         │
│     - Valida reglas de negocio                          │
│     - Verifica email único                              │
│     - Verifica username único                           │
│     - Hashea contraseña                                 │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  5. Repository Layer (UserRepository)                   │
│     - Crea objeto User                                  │
│     - Inserta en BD                                     │
│     - Retorna usuario creado                            │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  6. Respuesta al Cliente                                │
│     - Status 201 Created                                │
│     - Datos del usuario creado                          │
└─────────────────────────────────────────────────────────┘
```

### Flujo de Carga de Archivo

```
┌─────────────────────────────────────────────────────────┐
│  1. Usuario Selecciona Archivo Excel                    │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  2. Frontend (Dropzone.js)                              │
│     - Valida tipo de archivo                            │
│     - Prepara FormData                                  │
│     - POST /api/regions/upload-excel                    │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  3. API Endpoint                                        │
│     - Recibe archivo                                    │
│     - Valida extensión                                  │
│     - Llama a RegionService.process_excel()             │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  4. Service Layer (RegionService)                       │
│     - Lee archivo con Polars                            │
│     - Valida estructura de datos                        │
│     - Transforma datos                                  │
│     - Valida reglas de negocio                          │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  5. Repository Layer (RegionRepository)                 │
│     - Crea objetos Region                               │
│     - Inserta en lote en BD                             │
│     - Retorna cantidad insertada                        │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│  6. Respuesta al Cliente                                │
│     - Status 200 OK                                     │
│     - Cantidad de registros insertados                  │
│     - Errores (si los hay)                              │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 RESUMEN DE DECISIONES ARQUITECTÓNICAS

| Aspecto | Decisión | Razón |
|--------|----------|-------|
| **Framework** | FastAPI | Async, rápido, documentación automática |
| **ORM** | SQLModel | Combina Pydantic + SQLAlchemy |
| **BD** | MySQL | Relacional, confiable, escalable |
| **Autenticación** | JWT | Stateless, seguro, escalable |
| **Arquitectura** | Capas | Separación de responsabilidades |
| **Patrones** | Repository + Service | Testeable, mantenible |
| **Validación** | Pydantic | Type hints, validación automática |
| **Async** | AsyncIO | Mejor rendimiento, no bloqueante |

---

## ✅ CHECKLIST DE DISEÑO

- [ ] Principios SOLID aplicados
- [ ] Patrones de diseño identificados
- [ ] Arquitectura en capas definida
- [ ] Diagramas UML creados
- [ ] Flujos de datos documentados
- [ ] Responsabilidades claras
- [ ] Interfaces definidas
- [ ] Inyección de dependencias planificada
- [ ] Manejo de errores considerado
- [ ] Seguridad considerada

---

**Próximo paso**: Implementar según este diseño
