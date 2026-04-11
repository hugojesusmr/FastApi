# Backend FastAPI - Guía de Construcción Paso a Paso

**Proyecto:** Sistema de Autenticación JWT  
**Arquitectura:** Clean Architecture (Models → Repository → Service → API)  
**Base de datos:** SQLite async + Alembic (migraciones)  
**Auth:** JWT + bcrypt

---

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py           # Router principal
│   │   ├── auth.py             # Endpoints de autenticación
│   │   └── dashboard.py        # Endpoints del dashboard
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuración (.env)
│   │   └── auth.py             # Utilidades JWT/bcrypt
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py          # Conexión a BD async
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py             # Modelo User (SQLModel)
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user.py             # Acceso a datos User
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py             # Schemas Pydantic (E/S)
│   ├── services/
│   │   ├── __init__.py
│   │   └── user.py             # Lógica de negocio User
│   ├── templates/               # Plantillas HTML (Jinja2)
│   └── static/                  # CSS, JS, imágenes
├── alembic/                    # Migraciones de BD
├── alembic.ini                 # Configuración Alembic
├── requirements.txt            # Dependencias
├── .env                        # Variables de entorno
└── venv/                       # Entorno virtual
```

---

## PASO 1: Preparación del Entorno

```bash
# Entrar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Crear estructura de carpetas
mkdir -p app/{api,core,db,models,repositories,schemas,services,static,templates}
```

---

## PASO 2: requirements.txt

```txt
fastapi==0.116.1
uvicorn==0.35.0
sqlalchemy==2.0.41
sqlmodel==0.0.24
aiosqlite==0.20.0
alembic==1.16.5
python-dotenv==1.1.1
pydantic==2.10.6
pydantic-settings==2.10.1
PyJWT
bcrypt==4.1.2
email-validator==2.1.0
```

```bash
pip install -r requirements.txt
```

---

## PASO 3: Variables de Entorno (.env)

```bash
cat > .env << 'EOF'
DB_TYPE=sqlite
SQLITE_PATH=./fastapi_app.db
TABLE_NAME=tareas
EOF
```

---

## PASO 4: Configuración (app/core/config.py)

```python
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    DB_TYPE: str = "sqlite"
    SQLITE_PATH: str = "./fastapi_app.db"
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_DB_NAME: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_PORT: int = 5432
    TABLE_NAME: str = "tareas"

    class Config:
        env_file = ".env"
        env_prefix = ''

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "postgres":
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB_NAME}"
        return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"

settings = Settings()
```

**Propósito:** Lee variables de entorno y genera `DATABASE_URL` según el tipo de BD.

---

## PASO 5: Sesión de Base de Datos (app/db/session.py)

```python
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession 

connect_args = {"check_same_thread": False} if settings.DB_TYPE == "sqlite" else {}
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    connect_args=connect_args)

AsyncSessionFactory = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise    
        finally:  
            await session.close()
```

**Flujo:**
1. `engine` → Conexión async a SQLite/PostgreSQL
2. `AsyncSessionFactory` → Factory de sesiones
3. `get_session()` → Dependency injection (crea sesión por request)

---

## PASO 6: Modelo de Usuario (app/models/user.py)

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**SQLModel** combina SQLAlchemy + Pydantic (modelo de datos + validación).

---

## PASO 7: Schemas Pydantic (app/schemas/user.py)

```python
from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    
    class Config:
        from_attributes = True
```

**Propósito:**
- `UserCreate` → Entrada para registro
- `UserLogin` → Entrada para login
- `UserResponse` → Salida (sin password)

---

## PASO 8: Repository (app/repositories/user.py)

```python
from sqlmodel import Session, select
from typing import Optional
from app.models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
    
    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()
    
    async def get_by_id(self, id: int) -> Optional[User]:
        return await self.session.get(User, id)
```

**Patrón Repository:** Toda interacción con la BD pasa por aquí. Separa SQL de lógica de negocio.

---

## PASO 9: Utilidades de Auth (app/core/auth.py)

```python
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session
from app.models.user import User

SECRET_KEY = "s3cr3t00!!"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    result = await session.exec(select(User).where(User.username == username))
    user = result.first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return current_user
```

**Funciones:**
- `hash_password()` → Encripta con bcrypt
- `verify_password()` → Verifica password
- `create_access_token()` → Genera JWT
- `get_current_user()` → Valida token y obtiene usuario
- `get_current_active_user()` → Verifica que usuario esté activo

---

## PASO 10: Service Layer (app/services/user.py)

```python
from app.repositories.user import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.auth import hash_password, verify_password, create_access_token
from fastapi import HTTPException
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def register_user(self, user_create: UserCreate) -> UserResponse:
        existing_email = await self.user_repo.get_by_email(user_create.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email ya existe")
        
        existing_user = await self.user_repo.get_by_username(user_create.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username ya existe")
        
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hash_password(user_create.password)
        )
        
        created_user = await self.user_repo.create(db_user)
        
        return UserResponse(
            id=created_user.id,
            email=created_user.email,
            username=created_user.username,
            is_active=created_user.is_active
        )
    
    async def authenticate_user(self, username: str, password: str) -> dict:
        user = await self.user_repo.get_by_username(username)
        
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        password_valid = verify_password(password, user.hashed_password)
        
        if not password_valid:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
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

**Service Layer:** Lógica de negocio separada de la API. Valida reglas de negocio.

---

## PASO 11: API Endpoints (app/api/auth.py)

```python
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.core.auth import get_current_active_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        return await user_service.register_user(user)
    except Exception as e:
        print(f"Error en registro: {str(e)}")
        raise

@router.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    return await user_service.authenticate_user(user.username, user.password)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

---

## PASO 12: Router Principal (app/api/router.py)

```python
from fastapi import APIRouter
from app.api.auth import router as auth_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
```

---

## PASO 13: App Principal (app/main.py)

```python
from fastapi import FastAPI
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
```

---

## PASO 14: Migraciones con Alembic

```bash
# Inicializar Alembic
alembic init alembic

# Editar alembic.ini: sqlalchemy.url = sqlite+aiosqlite:///./fastapi_app.db

# Crear primera migración
alembic revision --autogenerate -m "inicial"

# Aplicar migraciones
alembic upgrade head
```

---

## PASO 15: Ejecutar el Servidor

```bash
uvicorn app.main:app --reload --port 8000
```

---

## Pruebas con curl

```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"testuser","password":"password123"}'

# 2. Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# 3. Obtener usuario actual (con token)
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer TOKEN_OBTENIDO_DEL_LOGIN"
```

---

## Diagrama de Flujo de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     REQUEST HTTP                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  API Layer (app/api/auth.py)                               │
│  - Recibe request HTTP                                     │
│  - Valida schemas con Pydantic                            │
│  - Dependency injection de session                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Service Layer (app/services/user.py)                     │
│  - Lógica de negocio                                      │
│  - Validaciones (email único, username único)             │
│  - Coordina repository y auth utilities                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌─────────────────────┐  ┌─────────────────────┐
│ Repository Layer    │  │ Auth Utilities      │
│ (app/repositories)  │  │ (app/core/auth.py)  │
│ - CRUD en DB        │  │ - hash/verify pass  │
│ - Queries           │  │ - JWT tokens        │
└─────────────────────┘  └─────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│  Database (SQLite/PostgreSQL)                              │
│  - Tabla users                                             │
│  - Migraciones con Alembic                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Resumen de Archivos Creados

| Archivo | Responsabilidad |
|---------|-----------------|
| `app/core/config.py` | Lee variables de entorno |
| `app/db/session.py` | Conexión async a BD |
| `app/models/user.py` | Modelo de datos User |
| `app/schemas/user.py` | Schemas de entrada/salida |
| `app/repositories/user.py` | Acceso a datos |
| `app/services/user.py` | Lógica de negocio |
| `app/core/auth.py` | JWT y bcrypt |
| `app/api/auth.py` | Endpoints REST |
| `app/api/router.py` | Router principal |
| `app/main.py` | App FastAPI |
