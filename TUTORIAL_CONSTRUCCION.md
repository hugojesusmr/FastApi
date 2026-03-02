# 🎓 Tutorial: Construir FastAPI desde Cero - Paso a Paso

## 📚 Índice
1. [Fase 1: Configuración Inicial](#fase-1-configuración-inicial)
2. [Fase 2: Base de Datos](#fase-2-base-de-datos)
3. [Fase 3: Modelos y Esquemas](#fase-3-modelos-y-esquemas)
4. [Fase 4: Autenticación](#fase-4-autenticación)
5. [Fase 5: API Endpoints](#fase-5-api-endpoints)
6. [Fase 6: Frontend](#fase-6-frontend)

---

## FASE 1: Configuración Inicial

### Paso 1.1: Crear Estructura de Carpetas

```
mkdir FastApi
cd FastApi
mkdir app app/api app/core app/db app/models app/schemas app/crud app/utils
mkdir app/static app/static/css app/static/js app/static/img
mkdir app/templates app/templates/components
mkdir alembic alembic/versions
```

### Paso 1.2: Crear requirements.txt

```
fastapi==0.116.1
uvicorn==0.35.0
sqlalchemy==2.0.41
sqlmodel==0.0.24
aiomysql==0.2.0
pydantic==2.10.6
pydantic-settings==2.10.1
python-jose==3.3.0
cryptography==45.0.5
jinja2==3.1.6
alembic==1.16.5
polars==1.0.0
pandas==2.3.0
python-dotenv==1.0.1
```

### Paso 1.3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 1.4: Crear archivo .env

```
MYSQL_HOST=localhost
MYSQL_DB_NAME=fastapi_db
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_PORT=3306
TABLE_NAME=regions
```

### Diagrama de Estructura Inicial

```
┌─────────────────────────────────────┐
│      FastApi Project                │
├─────────────────────────────────────┤
│                                     │
│  ├── app/                           │
│  │   ├── api/          (Endpoints)  │
│  │   ├── core/         (Config)     │
│  │   ├── db/           (BD)         │
│  │   ├── models/       (Tablas)     │
│  │   ├── schemas/      (Validación) │
│  │   ├── static/       (CSS, JS)    │
│  │   └── templates/    (HTML)       │
│  │                                  │
│  ├── alembic/          (Migraciones)│
│  ├── .env              (Variables)  │
│  └── requirements.txt  (Deps)       │
│                                     │
└─────────────────────────────────────┘
```

---

## FASE 2: Base de Datos

### Paso 2.1: Configuración (app/core/config.py)

```python
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_DB_NAME: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_PORT: int
    TABLE_NAME: str

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB_NAME}"

settings = Settings()
```

### Paso 2.2: Sesión de BD (app/db/session.py)

```python
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionFactory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
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

### Diagrama de Conexión a BD

```
┌──────────────────────────────────────────────┐
│         Aplicación FastAPI                   │
└──────────────────────────────────────────────┘
                    │
                    ↓
        ┌───────────────────────┐
        │  app/core/config.py   │
        │  (DATABASE_URL)       │
        └───────────────────────┘
                    │
                    ↓
        ┌───────────────────────┐
        │  app/db/session.py    │
        │  (AsyncSessionFactory)│
        └───────────────────────┘
                    │
                    ↓
        ┌───────────────────────┐
        │   SQLAlchemy Engine   │
        │   (aiomysql driver)   │
        └───────────────────────┘
                    │
                    ↓
        ┌───────────────────────┐
        │   MySQL Database      │
        │   (fastapi_db)        │
        └───────────────────────┘
```

---

## FASE 3: Modelos y Esquemas

### Paso 3.1: Crear Modelos (app/models/models.py)

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

class Region(SQLModel, table=True):
    __tablename__ = "regions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    site_code: str = Field(index=True)
    location_name: str
    city: str
    state: str
    region: str
```

### Paso 3.2: Crear Esquemas (app/schemas/schemas.py)

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class RegionCreate(BaseModel):
    site_code: str
    location_name: str
    city: str
    state: str
    region: str

class RegionResponse(RegionCreate):
    id: int
```

### Diagrama de Modelos

```
┌─────────────────────────────────────┐
│      SQLModel (Modelos)             │
├─────────────────────────────────────┤
│                                     │
│  ┌──────────────┐  ┌──────────────┐ │
│  │    User      │  │   Region     │ │
│  ├──────────────┤  ├──────────────┤ │
│  │ id (PK)      │  │ id (PK)      │ │
│  │ email (UK)   │  │ site_code    │ │
│  │ username (UK)│  │ location     │ │
│  │ password     │  │ city         │ │
│  │ is_active    │  │ state        │ │
│  │ created_at   │  │ region       │ │
│  └──────────────┘  └──────────────┘ │
│                                     │
└─────────────────────────────────────┘
         ↓ (Validación)
┌─────────────────────────────────────┐
│    Pydantic Schemas                 │
├─────────────────────────────────────┤
│                                     │
│  UserCreate, UserLogin              │
│  RegionCreate, RegionResponse       │
│                                     │
└─────────────────────────────────────┘
```

---

## FASE 4: Autenticación

### Paso 4.1: Utilidades de Autenticación (app/core/auth.py)

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

SECRET_KEY = "tu-clave-secreta-muy-segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Paso 4.2: CRUD de Usuarios (app/crud/user.py)

```python
from sqlmodel import Session, select
from app.models.models import User
from app.core.auth import hash_password

async def create_user(session: Session, email: str, username: str, password: str):
    db_user = User(
        email=email,
        username=username,
        hashed_password=hash_password(password)
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def get_user_by_username(session: Session, username: str):
    statement = select(User).where(User.username == username)
    return await session.exec(statement)
```

### Diagrama de Flujo de Autenticación

```
┌─────────────────────────────────────────────┐
│   Usuario Ingresa Credenciales              │
└─────────────────────────────────────────────┘
                    │
                    ↓
        ┌───────────────────────┐
        │  POST /api/auth/login │
        └───────────────────────┘
                    │
                    ↓
        ┌───────────────────────┐
        │  Validar Credenciales │
        │  (verify_password)    │
        └───────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ↓                       ↓
    ✓ Válido              ✗ Inválido
        │                       │
        ↓                       ↓
    Crear JWT            Error 401
        │
        ↓
    Retornar Token
        │
        ↓
    localStorage.setItem('access_token')
        │
        ↓
    Redirigir a /dashboard
```

---

## FASE 5: API Endpoints

### Paso 5.1: Endpoints de Autenticación (app/api/auth.py)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.schemas import UserCreate, UserLogin
from app.crud.user import create_user, get_user_by_username
from app.core.auth import verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
async def register(user: UserCreate, session: Session = Depends(get_session)):
    db_user = await create_user(session, user.email, user.username, user.password)
    return {"message": "Usuario creado", "user_id": db_user.id}

@router.post("/login")
async def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = await get_user_by_username(session, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

### Paso 5.2: Enrutador Principal (app/api/router.py)

```python
from fastapi import APIRouter
from app.api import auth, regions, dashboard

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(regions.router)
api_router.include_router(dashboard.router)
```

### Diagrama de Endpoints

```
┌──────────────────────────────────────────┐
│         API Endpoints                    │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  /api/auth                         │  │
│  ├────────────────────────────────────┤  │
│  │  POST /register                    │  │
│  │  POST /login                       │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  /api/regions                      │  │
│  ├────────────────────────────────────┤  │
│  │  GET /                             │  │
│  │  POST /upload-excel                │  │
│  │  GET /{id}                         │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  /api/dashboard                    │  │
│  ├────────────────────────────────────┤  │
│  │  GET /stats                        │  │
│  └────────────────────────────────────┘  │
│                                          │
└──────────────────────────────────────────┘
```

---

## FASE 6: Frontend

### Paso 6.1: Template Base (app/templates/base.html)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Dashboard{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/dashboard.css">
    {% block extra_css %}{% endblock %}
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
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Paso 6.2: Login (app/templates/login.html)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Iniciar Sesión</title>
    <link rel="stylesheet" href="/static/css/login.css">
</head>
<body>
    <div class="login-wrapper">
        <div class="login-form-section">
            <h2 class="login-title">Iniciar Sesión</h2>
            <form id="loginForm">
                <input type="text" name="username" placeholder="Usuario" required>
                <input type="password" name="password" placeholder="Contraseña" required>
                <button type="submit">Entrar</button>
            </form>
        </div>
    </div>
    <script src="/static/js/login.js"></script>
</body>
</html>
```

### Diagrama de Flujo Frontend

```
┌─────────────────────────────────────┐
│      Usuario Abre Navegador         │
└─────────────────────────────────────┘
                │
                ↓
    ┌───────────────────────┐
    │  GET / (login.html)   │
    └───────────────────────┘
                │
                ↓
    ┌───────────────────────┐
    │  Ingresa Credenciales │
    └───────────────────────┘
                │
                ↓
    ┌───────────────────────┐
    │  login.js             │
    │  POST /api/auth/login │
    └───────────────────────┘
                │
        ┌───────┴───────┐
        │               │
        ↓               ↓
    ✓ Token        ✗ Error
        │               │
        ↓               ↓
    Guardar JWT    Mostrar Error
        │
        ↓
    GET /dashboard
        │
        ↓
    dashboard.html
        │
        ↓
    Mostrar Contenido
```

---

## 🔄 Flujo Completo de la Aplicación

```
┌──────────────────────────────────────────────────────────┐
│                  USUARIO FINAL                           │
└──────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ↓                ↓                ↓
    ┌────────┐      ┌────────┐      ┌────────┐
    │ Login  │      │Upload  │      │Regiones│
    └────────┘      └────────┘      └────────┘
        │                │                │
        ↓                ↓                ↓
    ┌──────────────────────────────────────────┐
    │         Frontend (HTML/CSS/JS)           │
    │  login.html, dashboard.html, regions.html│
    └──────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ↓                ↓                ↓
    ┌────────┐      ┌────────┐      ┌────────┐
    │ auth.py│      │regions │      │dashboard
    │        │      │.py     │      │.py
    └────────┘      └────────┘      └────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ↓
        ┌──────────────────────────────┐
        │   app/core/auth.py           │
        │   (Validación, JWT)          │
        └──────────────────────────────┘
                         │
                         ↓
        ┌──────────────────────────────┐
        │   app/crud/                  │
        │   (Operaciones BD)           │
        └──────────────────────────────┘
                         │
                         ↓
        ┌──────────────────────────────┐
        │   app/db/session.py          │
        │   (Conexión Asincrónica)     │
        └──────────────────────────────┘
                         │
                         ↓
        ┌──────────────────────────────┐
        │   MySQL Database             │
        │   (users, regions)           │
        └──────────────────────────────┘
```

---

## 📋 Checklist de Construcción

- [ ] Fase 1: Estructura y configuración
- [ ] Fase 2: Base de datos y conexión
- [ ] Fase 3: Modelos y esquemas
- [ ] Fase 4: Autenticación
- [ ] Fase 5: Endpoints API
- [ ] Fase 6: Frontend HTML/CSS/JS
- [ ] Pruebas de endpoints
- [ ] Despliegue

---

## 🚀 Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload

# Crear migraciones
alembic revision --autogenerate -m "Descripción"

# Aplicar migraciones
alembic upgrade head

# Ver logs
tail -f app.log
```

---

**Próximo paso**: Implementar cada fase siguiendo este tutorial
