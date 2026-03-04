# 🎓 Tutorial Integrado: Diseño + Construcción FastAPI

## 📚 Índice
1. [Parte 1: Fundamentos y Diseño](#parte-1-fundamentos-y-diseño)
2. [Parte 2: Configuración e Inyección](#parte-2-configuración-e-inyección)
3. [Parte 3: Modelos y Validación](#parte-3-modelos-y-validación)
4. [Parte 4: Capa de Repositorio](#parte-4-capa-de-repositorio)
5. [Parte 5: Capa de Servicios](#parte-5-capa-de-servicios)
6. [Parte 6: API Endpoints](#parte-6-api-endpoints)
7. [Parte 7: Frontend](#parte-7-frontend)

---

# PARTE 1: Fundamentos y Diseño

## 🎯 ¿Por qué esta arquitectura?

### Problema: Código Monolítico

```
❌ MALO: Todo mezclado
┌─────────────────────────────────────┐
│  app.py                             │
├─────────────────────────────────────┤
│  - Endpoints                        │
│  - Lógica de negocio                │
│  - Acceso a BD                      │
│  - Validación                       │
│  - Autenticación                    │
│  - Todo junto = Difícil de mantener │
└─────────────────────────────────────┘

Problemas:
✗ Difícil de testear
✗ Difícil de mantener
✗ Difícil de escalar
✗ Acoplado
✗ No reutilizable
```

### Solución: Arquitectura en Capas

```
✅ BUENO: Separación de responsabilidades
┌─────────────────────────────────────┐
│  API Layer (Endpoints)              │
│  - Solo recibe y responde           │
│  - Delega a servicios               │
└─────────────────────────────────────┘
         ↓ (Inyección)
┌─────────────────────────────────────┐
│  Service Layer (Lógica)             │
│  - Reglas de negocio                │
│  - Validaciones                     │
│  - Orquestación                     │
└─────────────────────────────────────┘
         ↓ (Inyección)
┌─────────────────────────────────────┐
│  Repository Layer (Datos)           │
│  - CRUD operations                  │
│  - Consultas a BD                   │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Data Layer (BD)                    │
│  - MySQL                            │
└─────────────────────────────────────┘

Ventajas:
✓ Fácil de testear
✓ Fácil de mantener
✓ Fácil de escalar
✓ Desacoplado
✓ Reutilizable
```

## 🏗️ Principios SOLID Aplicados

### 1. Single Responsibility (SRP)

**¿Por qué?** Cada archivo tiene UNA responsabilidad

```
app/
├── core/config.py          → Solo carga configuración
├── db/session.py           → Solo gestiona conexión
├── models/models.py        → Solo define tablas
├── schemas/schemas.py      → Solo valida datos
├── repositories/user.py    → Solo accede a datos
├── services/user.py        → Solo lógica de negocio
└── api/auth.py             → Solo endpoints
```

### 2. Open/Closed (OCP)

**¿Por qué?** Abierto para extensión, cerrado para modificación

```
Hoy: UserRepository
Mañana: Agregar AdminRepository
Pasado: Agregar GuestRepository

Sin modificar código existente ✓
```

### 3. Liskov Substitution (LSP)

**¿Por qué?** Todas las implementaciones son intercambiables

```
Hoy: MySQLUserRepository
Mañana: PostgresUserRepository
Pasado: MongoDBUserRepository

Mismo código, diferente BD ✓
```

### 4. Interface Segregation (ISP)

**¿Por qué?** Interfaces pequeñas y específicas

```
❌ MALO:
IRepository (create, read, update, delete, search, export, import)

✅ BUENO:
ICreatable (create)
IReadable (read, search)
IUpdatable (update)
IDeletable (delete)
```

### 5. Dependency Inversion (DIP)

**¿Por qué?** Depender de abstracciones, no de implementaciones

```
❌ MALO:
UserService → MySQLUserRepository (Acoplado)

✅ BUENO:
UserService → IUserRepository (Interfaz)
                    ↓
            MySQLUserRepository (Implementación)
```

---

# PARTE 2: Configuración e Inyección

## Paso 2.1: Crear Estructura Base

```bash
mkdir -p FastApi/app/{api,core,db,models,schemas,repositories,services,utils}
mkdir -p FastApi/app/{static/{css,js,img},templates/components}
mkdir -p FastApi/alembic/versions
```

## Paso 2.2: Configuración (app/core/config.py)

**¿Por qué aquí?**
- **SRP**: Solo responsable de cargar configuración
- **DIP**: Centraliza todas las variables
- **Testeable**: Fácil de mockear en tests

```python
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """
    Centraliza todas las variables de entorno
    Principio: Single Responsibility
    """
    MYSQL_HOST: str
    MYSQL_DB_NAME: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_PORT: int
    SECRET_KEY: str = "tu-clave-secreta"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB_NAME}"

settings = Settings()
```

## Paso 2.3: Sesión de BD (app/db/session.py)

**¿Por qué aquí?**
- **SRP**: Solo gestiona conexión a BD
- **DIP**: Inyectable en cualquier lugar
- **Async**: No bloqueante

```python
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

# Crear motor asincrónico
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

# Factory para crear sesiones
AsyncSessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session():
    """
    Generador de sesiones para inyección de dependencias
    Principio: Dependency Inversion
    
    Uso en endpoints:
    @app.get("/users")
    async def get_users(session: Session = Depends(get_session)):
        ...
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## Diagrama: Inyección de Dependencias

```
┌──────────────────────────────────────────────┐
│         FastAPI Endpoint                     │
│  @app.get("/users")                          │
│  async def get_users(                        │
│      session: Session = Depends(get_session) │
│  ):                                          │
└──────────────────────────────────────────────┘
                    │
                    ↓ (FastAPI inyecta)
┌──────────────────────────────────────────────┐
│         get_session()                        │
│  - Crea AsyncSession                         │
│  - Retorna sesión                            │
│  - Maneja commit/rollback                    │
└──────────────────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────┐
│         AsyncSessionFactory                  │
│  - Crea sesiones asincrónicas                │
│  - Usa engine de SQLAlchemy                  │
└──────────────────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────┐
│         MySQL Database                       │
└──────────────────────────────────────────────┘

Ventajas:
✓ Desacoplado
✓ Testeable (mockear sesión)
✓ Reutilizable
✓ Limpio
```

---

# PARTE 3: Modelos y Validación

## Paso 3.1: Modelos SQLModel (app/models/models.py)

**¿Por qué SQLModel?**
- Combina Pydantic (validación) + SQLAlchemy (ORM)
- Type hints automáticos
- Validación automática

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    """
    Modelo de Usuario
    Principio: Single Responsibility
    - Solo define estructura de tabla
    - No contiene lógica de negocio
    """
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Region(SQLModel, table=True):
    """
    Modelo de Región
    Principio: Single Responsibility
    """
    __tablename__ = "regions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    site_code: str = Field(index=True)
    location_name: str
    city: str
    state: str
    region: str
```

## Paso 3.2: Esquemas Pydantic (app/schemas/schemas.py)

**¿Por qué separar modelos de esquemas?**
- **SRP**: Modelos = BD, Esquemas = API
- **Seguridad**: No exponer campos internos
- **Flexibilidad**: Diferentes esquemas para diferentes casos

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ============ USER SCHEMAS ============

class UserCreate(BaseModel):
    """
    Esquema para crear usuario
    - Valida email
    - Valida contraseña
    - NO incluye id (generado por BD)
    """
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    """
    Esquema para login
    - Solo username y password
    """
    username: str
    password: str

class UserResponse(BaseModel):
    """
    Esquema de respuesta
    - NO incluye password
    - Solo datos públicos
    """
    id: int
    email: str
    username: str
    is_active: bool

# ============ REGION SCHEMAS ============

class RegionCreate(BaseModel):
    """
    Esquema para crear región
    """
    site_code: str
    location_name: str
    city: str
    state: str
    region: str

class RegionResponse(RegionCreate):
    """
    Esquema de respuesta
    - Incluye id
    """
    id: int
```

## Diagrama: Separación Modelos vs Esquemas

```
┌─────────────────────────────────────┐
│      Base de Datos                  │
│  (Tabla users)                      │
├─────────────────────────────────────┤
│  id, email, username,               │
│  hashed_password, is_active,        │
│  created_at                         │
└─────────────────────────────────────┘
         ▲                    ▼
         │                    │
    ┌────┴────┐          ┌────┴────┐
    │          │          │         │
    │ Modelo   │          │ Esquema │
    │ (User)   │          │ (UserResponse)
    │          │          │         │
    │ Todos    │          │ Solo:   │
    │ los      │          │ id      │
    │ campos   │          │ email   │
    │          │          │ username│
    │          │          │ is_active
    └──────────┘          └─────────┘
         ▲                    ▲
         │                    │
    Lectura                Respuesta
    de BD                  a Cliente
```

---

# PARTE 4: Capa de Repositorio

## Paso 4.1: Interfaz Base (app/repositories/base.py)

**¿Por qué una interfaz?**
- **OCP**: Abierto para extensión
- **LSP**: Todas las implementaciones son intercambiables
- **DIP**: Depender de abstracción

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    """
    Interfaz genérica para repositorios
    Principio: Interface Segregation + Dependency Inversion
    """
    
    @abstractmethod
    async def create(self, obj: T) -> T:
        """Crear objeto"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        """Obtener por ID"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[T]:
        """Obtener todos"""
        pass
    
    @abstractmethod
    async def update(self, obj: T) -> T:
        """Actualizar"""
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Eliminar"""
        pass
```

## Paso 4.2: Repositorio de Usuario (app/repositories/user.py)

**¿Por qué aquí?**
- **SRP**: Solo acceso a datos de usuario
- **OCP**: Implementa interfaz sin modificarla
- **LSP**: Intercambiable con otros repositorios

```python
from sqlmodel import Session, select
from typing import Optional
from app.models.models import User
from app.repositories.base import IRepository

class UserRepository(IRepository[User]):
    """
    Implementación de repositorio para User
    Principio: Liskov Substitution
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, obj: User) -> User:
        """Crear usuario"""
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def get_by_id(self, id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        return await self.session.get(User, id)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        statement = select(User).where(User.username == username)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_all(self) -> list[User]:
        """Obtener todos los usuarios"""
        statement = select(User)
        result = await self.session.exec(statement)
        return result.all()
    
    async def update(self, obj: User) -> User:
        """Actualizar usuario"""
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def delete(self, id: int) -> bool:
        """Eliminar usuario"""
        user = await self.get_by_id(id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False
```

---

# PARTE 5: Capa de Servicios

## Paso 5.1: Servicio de Usuario (app/services/user.py)

**¿Por qué una capa de servicios?**
- **SRP**: Lógica de negocio separada
- **Testeable**: Mockear repositorio
- **Reutilizable**: Usar en múltiples endpoints

```python
from app.repositories.user import UserRepository
from app.models.models import User
from app.schemas.schemas import UserCreate, UserResponse
from app.core.auth import hash_password, verify_password, create_access_token
from fastapi import HTTPException

class UserService:
    """
    Servicio de Usuario
    Principio: Single Responsibility + Dependency Inversion
    """
    
    def __init__(self, user_repo: UserRepository):
        """
        Inyección de dependencia
        Principio: Dependency Inversion
        """
        self.user_repo = user_repo
    
    async def register_user(self, user_create: UserCreate) -> UserResponse:
        """
        Registrar nuevo usuario
        Lógica de negocio:
        1. Validar email único
        2. Validar username único
        3. Hashear contraseña
        4. Guardar en BD
        """
        # Validar email único
        existing_user = await self.user_repo.get_by_username(user_create.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username ya existe")
        
        # Crear usuario
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hash_password(user_create.password)
        )
        
        # Guardar
        created_user = await self.user_repo.create(db_user)
        
        return UserResponse(
            id=created_user.id,
            email=created_user.email,
            username=created_user.username,
            is_active=created_user.is_active
        )
    
    async def authenticate_user(self, username: str, password: str) -> dict:
        """
        Autenticar usuario
        Lógica de negocio:
        1. Buscar usuario
        2. Verificar contraseña
        3. Generar JWT
        """
        user = await self.user_repo.get_by_username(username)
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        access_token = create_access_token(data={"sub": user.username})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                is_active=user.is_active
            )
        }
```

## Diagrama: Flujo de Datos en Capas

```
┌─────────────────────────────────────┐
│  API Endpoint                       │
│  POST /api/auth/register            │
│  (Recibe UserCreate)                │
└─────────────────────────────────────┘
         │
         ↓ (Inyecta UserService)
┌─────────────────────────────────────┐
│  UserService                        │
│  - Valida reglas de negocio         │
│  - Hashea contraseña                │
│  - Orquesta operaciones             │
└─────────────────────────────────────┘
         │
         ↓ (Inyecta UserRepository)
┌─────────────────────────────────────┐
│  UserRepository                     │
│  - Crea objeto User                 │
│  - Inserta en BD                    │
│  - Retorna usuario creado           │
└─────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│  MySQL Database                     │
│  - Almacena usuario                 │
└─────────────────────────────────────┘
         │
         ↑ (Retorna datos)
┌─────────────────────────────────────┐
│  UserRepository                     │
│  - Retorna User                     │
└─────────────────────────────────────┘
         │
         ↑ (Transforma a Response)
┌─────────────────────────────────────┐
│  UserService                        │
│  - Retorna UserResponse             │
└─────────────────────────────────────┘
         │
         ↑ (Retorna JSON)
┌─────────────────────────────────────┐
│  API Endpoint                       │
│  - Retorna 201 Created              │
└─────────────────────────────────────┘
```

---

# PARTE 6: API Endpoints

## Paso 6.1: Endpoints de Autenticación (app/api/auth.py)

**¿Por qué aquí?**
- **SRP**: Solo recibe y responde
- **Delega**: A servicios la lógica
- **Limpio**: Código simple y legible

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.schemas import UserCreate, UserLogin
from app.services.user import UserService
from app.repositories.user import UserRepository

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", status_code=201)
async def register(
    user_create: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Registrar nuevo usuario
    
    Flujo:
    1. FastAPI valida UserCreate (Pydantic)
    2. Inyecta sesión
    3. Crea repositorio
    4. Crea servicio
    5. Llama register_user
    6. Retorna respuesta
    """
    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    
    return await user_service.register_user(user_create)

@router.post("/login")
async def login(
    user_login: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Autenticar usuario
    """
    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    
    return await user_service.authenticate_user(
        user_login.username,
        user_login.password
    )
```

---

# PARTE 7: Frontend

## Paso 7.1: Estructura HTML (app/templates/base.html)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Dashboard{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/dashboard.css">
</head>
<body>
    {% include "components/topbar.html" %}
    
    <div class="container">
        {% include "components/sidebar.html" %}
        <main class="main-content">
            {% block content %}{% endblock %}
        </main>
    </div>

    <script src="/static/js/dashboard.js"></script>
</body>
</html>
```

---

## 📋 RESUMEN: ¿Por qué cada parte?

| Parte | Responsabilidad | Principio SOLID |
|-------|-----------------|-----------------|
| **Config** | Cargar variables | SRP |
| **Session** | Gestionar conexión | SRP + DIP |
| **Models** | Definir tablas | SRP |
| **Schemas** | Validar datos | SRP |
| **Repository** | Acceso a datos | OCP + LSP + DIP |
| **Service** | Lógica de negocio | SRP + DIP |
| **API** | Endpoints | SRP |

---

## ✅ CHECKLIST DE CONSTRUCCIÓN

- [ ] Parte 1: Entender diseño
- [ ] Parte 2: Config + Session
- [ ] Parte 3: Models + Schemas
- [ ] Parte 4: Repository
- [ ] Parte 5: Service
- [ ] Parte 6: API
- [ ] Parte 7: Frontend
- [ ] Pruebas
- [ ] Despliegue

---

**Próximo paso**: Implementar cada parte siguiendo este tutorial integrado
