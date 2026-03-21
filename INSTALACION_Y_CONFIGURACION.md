# Guía de Instalación y Configuración Inicial - Sistema Ticketmaster

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de Librerías](#instalación-de-librerías)
3. [Configuración de PostgreSQL](#configuración-de-postgresql)
4. [Configuración de Redis](#configuración-de-redis)
5. [Configuración del Proyecto](#configuración-del-proyecto)
6. [Verificación de la Instalación](#verificación-de-la-instalación)


### Instalación de Dependencias del Sistema

#### En Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y \
    python3.9 \
    python3.9-venv \
    python3.9-dev \
    postgresql \
    postgresql-contrib \
    redis-server \
    git \
    curl \
    build-essential \
    libpq-dev
```

#### En macOS (con Homebrew):
```bash
brew install python@3.9 postgresql redis git
```

#### En Windows (WSL2):
```bash
# Dentro de WSL2 Ubuntu
sudo apt update
sudo apt install -y python3.9 python3.9-venv postgresql redis-server
```

---

## Instalación de Librerías

### Paso 1: Crear Entorno Virtual

```bash
# Navegar al directorio del proyecto
cd /home/hugo/proyectos/FastApi

# Crear entorno virtual
python3.9 -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### Paso 2: Actualizar pip

```bash
pip install --upgrade pip setuptools wheel
```

### Paso 3: Crear archivo requirements.txt

Crea el archivo `requirements.txt` en la raíz del proyecto:

```bash
cat > requirements.txt << 'EOF'
# Framework Web
fastapi==0.116.1
uvicorn==0.35.0
starlette==0.47.3

# Base de Datos
sqlalchemy==2.0.43
sqlmodel==0.0.24
asyncpg==0.30.0
alembic==1.16.5

# Validación de Datos
pydantic==2.12.5
pydantic-settings==2.10.1
pydantic-extra-types==2.10.5
email-validator==2.3.0

# Autenticación y Seguridad
PyJWT==2.8.1
bcrypt==4.1.2
python-dotenv==1.1.1

# Cache y Sesiones
redis==5.0.1

# Tareas Asincrónicas
celery==5.3.4
flower==2.0.1

# Pagos (Stripe)
stripe==7.8.0

# Email
python-multipart==0.0.20

# Utilidades
requests==2.31.0
httpx==0.28.1

# Testing
pytest==7.4.3
pytest-asyncio==0.23.2
pytest-cov==4.1.0
httpx==0.28.1

# Logging y Monitoreo
python-json-logger==2.0.7

# Desarrollo
black==23.12.1
flake8==6.1.0
isort==5.13.2
EOF
```

### Paso 4: Instalar Librerías

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

### Paso 5: Verificar Instalación de Librerías Críticas

```bash
# Verificar FastAPI
python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"

# Verificar SQLModel
python -c "import sqlmodel; print('SQLModel OK')"

# Verificar AsyncPG
python -c "import asyncpg; print('AsyncPG OK')"

# Verificar Redis
python -c "import redis; print('Redis OK')"

# Verificar Celery
python -c "import celery; print(f'Celery {celery.__version__}')"
```

---

## Configuración de PostgreSQL

### Paso 1: Iniciar PostgreSQL

#### En Linux/macOS:
```bash
# Iniciar servicio PostgreSQL
sudo systemctl start postgresql

# Verificar estado
sudo systemctl status postgresql

# Habilitar inicio automático
sudo systemctl enable postgresql
```

#### En Windows (WSL2):
```bash
sudo service postgresql start
```

### Paso 2: Acceder a PostgreSQL

```bash
# Conectarse como usuario postgres
sudo -u postgres psql

# O si tienes contraseña configurada
psql -U postgres -h localhost
```

### Paso 3: Crear Usuario y Base de Datos

Dentro de la consola de PostgreSQL (`psql`):

```sql
-- Crear usuario para la aplicación
CREATE USER ticketmaster WITH PASSWORD 'tu_contraseña_segura';

-- Crear base de datos
CREATE DATABASE ticketmaster_db OWNER ticketmaster;

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE ticketmaster_db TO ticketmaster;

-- Conectarse a la BD
\c ticketmaster_db

-- Dar permisos en esquema público
GRANT ALL PRIVILEGES ON SCHEMA public TO ticketmaster;

-- Salir
\q
```

### Paso 4: Verificar Conexión

```bash
# Conectarse con el nuevo usuario
psql -U ticketmaster -d ticketmaster_db -h localhost

# Dentro de psql, verificar conexión
SELECT version();

# Salir
\q
```

### Paso 5: Crear Extensiones Necesarias

```bash
# Conectarse como postgres
sudo -u postgres psql -d ticketmaster_db

# Crear extensiones
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

# Salir
\q
```

---

## Configuración de Redis

### Paso 1: Iniciar Redis

#### En Linux/macOS:
```bash
# Iniciar servicio Redis
sudo systemctl start redis-server

# Verificar estado
sudo systemctl status redis-server

# Habilitar inicio automático
sudo systemctl enable redis-server
```

#### En Windows (WSL2):
```bash
sudo service redis-server start
```

### Paso 2: Verificar Conexión a Redis

```bash
# Conectarse a Redis
redis-cli

# Dentro de redis-cli
ping

# Debería responder: PONG

# Salir
exit
```

### Paso 3: Configurar Redis (Opcional)

```bash
# Editar configuración de Redis
sudo nano /etc/redis/redis.conf

# Cambios recomendados:
# - maxmemory 256mb
# - maxmemory-policy allkeys-lru
# - appendonly yes (para persistencia)

# Reiniciar Redis
sudo systemctl restart redis-server
```

---

## Configuración del Proyecto

### Paso 1: Crear archivo .env

En la raíz del proyecto, crea `.env`:

```bash
cat > .env << 'EOF'
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

# ===== STRIPE (Pagos) =====
STRIPE_SECRET_KEY=sk_test_tu_clave_aqui
STRIPE_PUBLIC_KEY=pk_test_tu_clave_aqui

# ===== EMAIL =====
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_email@gmail.com
SMTP_PASSWORD=tu_contraseña_app
SENDER_EMAIL=noreply@ticketmaster.com

# ===== CELERY =====
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF
```

### Paso 2: Actualizar app/core/config.py

```python
# app/core/config.py
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    """
    Configuración de la aplicación cargada desde variables de entorno
    """
    
    # ===== BASE DE DATOS =====
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB_NAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    
    # ===== REDIS =====
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # ===== APLICACIÓN =====
    APP_NAME: str = "Ticketmaster"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # ===== SEGURIDAD =====
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ===== STRIPE =====
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLIC_KEY: Optional[str] = None
    
    # ===== EMAIL =====
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SENDER_EMAIL: Optional[str] = None
    
    # ===== CELERY =====
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construir URL de conexión a PostgreSQL"""
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB_NAME}"
        )
    
    @property
    def REDIS_URL(self) -> str:
        """Construir URL de conexión a Redis"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        env_file = ".env"
        env_prefix = ""

settings = Settings()
```

### Paso 3: Actualizar app/db/session.py

```python
# app/db/session.py
from app.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

# Crear motor de conexión
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Cambiar a True para ver queries SQL
    future=True,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,  # Verificar conexión antes de usar
)

# Generador de sesiones
AsyncSessionFactory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Función de inyección de dependencias
async def get_session() -> AsyncSession:
    """
    Generador de sesiones para inyección de dependencias
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Error en sesión: {e}")
            raise
        finally:
            await session.close()
```

### Paso 4: Crear app/db/cache.py

```python
# app/db/cache.py
import redis
from app.core.config import settings

# Conexión a Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_keepalive=True,
)

def get_redis():
    """Obtener cliente de Redis"""
    return redis_client

async def test_redis_connection():
    """Probar conexión a Redis"""
    try:
        redis_client.ping()
        return True
    except Exception as e:
        print(f"Error conectando a Redis: {e}")
        return False
```

---

## Verificación de la Instalación

### Paso 1: Verificar Conexión a PostgreSQL

```bash
# Crear script de prueba
cat > test_db_connection.py << 'EOF'
import asyncio
from app.db.session import engine
from app.core.config import settings

async def test_connection():
    print(f"Conectando a: {settings.DATABASE_URL}")
    try:
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1")
            print("✅ Conexión a PostgreSQL exitosa")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
EOF

# Ejecutar prueba
python test_db_connection.py
```

### Paso 2: Verificar Conexión a Redis

```bash
# Crear script de prueba
cat > test_redis_connection.py << 'EOF'
from app.db.cache import redis_client

try:
    redis_client.ping()
    print("✅ Conexión a Redis exitosa")
    
    # Prueba de escritura/lectura
    redis_client.set("test_key", "test_value")
    value = redis_client.get("test_key")
    print(f"✅ Valor guardado y recuperado: {value}")
    
    # Limpiar
    redis_client.delete("test_key")
except Exception as e:
    print(f"❌ Error: {e}")
EOF

# Ejecutar prueba
python test_redis_connection.py
```

### Paso 3: Verificar Todas las Librerías

```bash
# Crear script de verificación
cat > verify_installation.py << 'EOF'
import sys

libraries = {
    'fastapi': 'FastAPI',
    'sqlmodel': 'SQLModel',
    'asyncpg': 'AsyncPG',
    'redis': 'Redis',
    'celery': 'Celery',
    'pydantic': 'Pydantic',
    'jwt': 'PyJWT',
    'bcrypt': 'Bcrypt',
    'pytest': 'Pytest',
}

print("Verificando librerías instaladas...\n")

all_ok = True
for module, name in libraries.items():
    try:
        __import__(module)
        print(f"✅ {name}")
    except ImportError:
        print(f"❌ {name} - NO INSTALADO")
        all_ok = False

if all_ok:
    print("\n✅ Todas las librerías están instaladas correctamente")
    sys.exit(0)
else:
    print("\n❌ Faltan librerías por instalar")
    sys.exit(1)
EOF

# Ejecutar verificación
python verify_installation.py
```

### Paso 4: Verificar Estructura del Proyecto

```bash
# Crear estructura de carpetas
mkdir -p app/models
mkdir -p app/repositories
mkdir -p app/services
mkdir -p app/schemas
mkdir -p app/workers
mkdir -p tests

# Crear archivos __init__.py
touch app/models/__init__.py
touch app/repositories/__init__.py
touch app/services/__init__.py
touch app/schemas/__init__.py
touch app/workers/__init__.py
touch tests/__init__.py

# Verificar estructura
tree app/ -L 2
```

---

## Checklist de Verificación

```
✅ Python 3.9+ instalado
✅ Entorno virtual creado y activado
✅ Librerías instaladas (pip list)
✅ PostgreSQL corriendo (sudo systemctl status postgresql)
✅ Base de datos 'ticketmaster_db' creada
✅ Usuario 'ticketmaster' creado
✅ Redis corriendo (redis-cli ping)
✅ Archivo .env configurado
✅ app/core/config.py actualizado
✅ app/db/session.py actualizado
✅ app/db/cache.py creado
✅ Conexión a PostgreSQL verificada
✅ Conexión a Redis verificada
✅ Estructura de carpetas creada
```

---

## Próximos Pasos

Una vez completada esta configuración inicial:

1. **Crear Modelos** - Definir User, Event, Venue, Seat, etc.
2. **Crear Repositorios** - Acceso a datos
3. **Crear Servicios** - Lógica de negocio
4. **Crear Endpoints** - APIs REST
5. **Crear Tests** - Pruebas unitarias e integración
6. **Configurar Migraciones** - Alembic

---

## Solución de Problemas

### Error: "No module named 'asyncpg'"
```bash
pip install asyncpg
```

### Error: "Connection refused" en PostgreSQL
```bash
# Verificar si PostgreSQL está corriendo
sudo systemctl status postgresql

# Iniciar si no está corriendo
sudo systemctl start postgresql
```

### Error: "Connection refused" en Redis
```bash
# Verificar si Redis está corriendo
sudo systemctl status redis-server

# Iniciar si no está corriendo
sudo systemctl start redis-server
```

### Error: "FATAL: role 'ticketmaster' does not exist"
```bash
# Recrear usuario
sudo -u postgres psql
CREATE USER ticketmaster WITH PASSWORD 'tu_contraseña';
\q
```

### Error: "database 'ticketmaster_db' does not exist"
```bash
# Recrear base de datos
sudo -u postgres psql
CREATE DATABASE ticketmaster_db OWNER ticketmaster;
\q
```

---

## Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Celery Documentation](https://docs.celeryproject.io/)

