# Sistema PDF Extractor - Guía de Construcción Paso a Paso

## 1. Configuración del Entorno

### 1.1 Estructura del Proyecto
```
FastApi/
├── backend/
│   ├── app/
│   │   ├── api/           # Endpoints HTTP
│   │   ├── core/          # Config, Auth, Utilidades
│   │   ├── db/            # Conexión BD
│   │   ├── models/        # Modelos SQLModel
│   │   ├── repositories/  # Acceso a BD
│   │   ├── schemas/       # Pydantic Schemas
│   │   ├── services/      # Lógica de negocio
│   │   ├── main.py        # Entry point FastAPI
│   │   └── static/        # Archivos estáticos
│   ├── requirements.txt
│   └── alembic/           # Migraciones
└── frontend/
    └── mi-app/           # React + Vite + TS
```

### 1.2 Tech Stack
- **Backend**: FastAPI 0.116.1, SQLite (async), Alembic, JWT + bcrypt, SQLModel, pdfplumber
- **Frontend**: React 19 + Vite + TypeScript + react-pdf

---

## 2. Backend - Paso a Paso

### Paso 1: Configuración Inicial
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi[all] uvicorn sqlmodel sqlalchemy alembic python-jose[cryptography] passlib[bcrypt] python-multipart pdfplumber
```

### Paso 2: Estructura de Archivos Backend
Crear la siguiente estructura:
```
backend/app/
├── __init__.py
├── main.py
├── api/
│   ├── __init__.py
│   ├── router.py
│   ├── auth.py
│   ├── pdf.py
│   └── dashboard.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── auth.py
├── db/
│   ├── __init__.py
│   └── connection.py
├── models/
│   ├── __init__.py
│   └── user.py
├── repositories/
│   ├── __init__.py
│   └── user.py
├── schemas/
│   ├── __init__.py
│   ├── user.py
│   ├── auth.py
│   └── pdf.py
└── services/
    ├── __init__.py
    ├── user.py
    └── pdf.py
```

### Paso 3: Configuración Core

**`backend/app/core/config.py`**
```python
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "tu-secret-key-aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**`backend/app/core/auth.py`**
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="No válido")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None: raise credentials_exception
    except JWTError: raise credentials_exception
    from app.repositories.user import UserRepository
    repo = UserRepository()
    user = await repo.get_by_username(username)
    if user is None: raise credentials_exception
    return user
```

### Paso 4: Modelos y Base de Datos

**`backend/app/db/connection.py`**
```python
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncConnection
from app.core.config import settings

DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite"

engine = create_async_engine(DATABASE_URL, echo=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session
```

**`backend/app/models/user.py`**
```python
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: Optional[str] = Field(default=None, unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
```

### Paso 5: Repositorios

**`backend/app/repositories/user.py`**
```python
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User

class UserRepository:
    async def get_by_username(self, username: str) -> User | None:
        # Implementar consulta a BD
        pass
    
    async def create(self, username: str, email: str, hashed_password: str) -> User:
        # Implementar creación
        pass
```

### Paso 6: Schemas Pydantic

**`backend/app/schemas/user.py`**
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool
```

**`backend/app/schemas/auth.py`**
```python
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str
```

**`backend/app/schemas/pdf.py`**
```python
from pydantic import BaseModel
from typing import Optional, List

class PdfExtractResponse(BaseModel):
    text: str
    page: int

class RegionRequest(BaseModel):
    page_number: int
    x0: float
    y0: float
    x1: float
    y1: float
    pdf_width: float
    pdf_height: float

class RegionExtractResponse(BaseModel):
    type: str
    text: Optional[str] = None
    headers: Optional[List[str]] = None
    rows: Optional[List[List[str]]] = None
    page_number: int
```

### Paso 7: Servicios

**`backend/app/services/user.py`**
```python
from passlib.context import CryptContext
from app.repositories.user import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def verify_password(self, plain, hashed): ...
    def get_password_hash(self, password): ...
    async def create_user(self, user_data: UserCreate): ...
    async def authenticate(self, username, password): ...
```

**`backend/app/services/pdf.py`**
```python
import pdfplumber
from io import BytesIO

class PdfService:
    async def extract_text(self, file):
        # Procesar PDF completo con pdfplumber
        pass
    
    async def extract_region(self, file, region):
        # Extraer región específica
        pass
```

### Paso 8: APIs

**`backend/app/api/auth.py`**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user_data: UserCreate):
    # Registrar usuario
    pass

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Login y retornar token JWT
    pass

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_active_user)):
    # Retornar usuario actual
    pass
```

**`backend/app/api/pdf.py`**
```python
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.services.pdf import PdfService
from app.schemas.pdf import PdfExtractResponse, RegionExtractResponse, RegionRequest
from app.core.auth import get_current_active_user

router = APIRouter(prefix="/pdf", tags=["pdf"])

@router.post("/extract")
async def extract_pdf(file: UploadFile = File(...), current_user = Depends(get_current_active_user)):
    service = PdfService()
    return await service.extract_text(file)

@router.post("/extract-region")
async def extract_region(file: UploadFile = File(...), region: str = Form(...), current_user = Depends(get_current_active_user)):
    service = PdfService()
    region_data = RegionRequest(**json.loads(region))
    return await service.extract_region(file, region_data)
```

**`backend/app/api/router.py`**
```python
from fastapi import APIRouter
from app.api import auth, pdf, dashboard

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(pdf.router)
api_router.include_router(dashboard.router)
```

### Paso 9: Main

**`backend/app/main.py`**
```python
from fastapi import FastAPI
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.connection import init_db

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(api_router, prefix="/api")
```

---

## 3. Frontend - Paso a Paso

### Paso 1: Crear Proyecto React
```bash
cd frontend
npm create vite@latest mi-app -- --template react-ts
cd mi-app
npm install
npm install react-router-dom axios react-pdf pdfjs-dist lucide-react
```

### Paso 2: Estructura
```
frontend/mi-app/src/
├── App.tsx
├── main.tsx
├── api/
├── components/
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Dashboard.tsx
│   ├── PdfUpload.tsx
│   └── PdfUpload.css
├── contexts/
│   └── AuthContext.tsx
├── hooks/
├── pages/
├── types/
└── utils/
```

### Paso 3: Configurar Router y Auth

**`src/contexts/AuthContext.tsx`**
- Proveer estado de autenticación
- Funciones login, logout, register
- Persistir token en localStorage

**`src/App.tsx`**
- Configurar Routes: /login, /register, /dashboard
- Proteger rutas privadas con RequireAuth

### Paso 4: Componentes PDF

El componente `PdfUpload.tsx` debe incluir:
1. Carga de PDF con `react-pdf`
2. Renderizado lazy de páginas (solo visibles)
3. Selección de región con mouse
4. Extracción de texto/tablas por región

---

## 4. Convenciones del Proyecto

1. **Toda interacción con BD** → Repository
2. **Lógica de negocio** → Service
3. **APIs** → Solo reciben/retornan Pydantic Schemas
4. **PDF** → Siempre procesado en memoria (BytesIO), nunca en disco
5. **SECRET_KEY** → Siempre en `.env`, nunca hardcodeada
6. **Autenticación** → JWT con Bearer token
7. **Estilo** → Clean Architecture: API → Service → Repository → DB