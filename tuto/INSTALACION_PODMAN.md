# Guía de Instalación y Configuración con Podman - Sistema Ticketmaster

## 📋 Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de Librerías](#instalación-de-librerías)
3. [Configuración de Podman](#configuración-de-podman)
4. [Levantar Contenedores](#levantar-contenedores)
5. [Configuración del Proyecto](#configuración-del-proyecto)
6. [Verificación de la Instalación](#verificación-de-la-instalación)

---

## Requisitos Previos

### Sistema Operativo
- Oracle Linux 9
- Podman instalado

### Software Requerido
```bash
# Verificar versiones instaladasj
python --version          # Python 3.9+
pip --version            # pip 21+
podman --version         # Podman 4.0+
```

### Instalación de Dependencias del Sistema

#### En Oracle Linux 9:
```bash
# Actualizar sistema
sudo dnf update -y

# Instalar Python y herramientas
sudo dnf install -y \
    python3.9 \
    python3.9-devel \
    python3-pip \
    podman \
    podman-compose \
    git \
    curl \
    gcc \
    make

# Verificar instalación
python3.9 --version
podman --version
```

### Habilitar Podman sin sudo (Opcional)

```bash
# Agregar usuario al grupo podman
sudo usermod -aG podman $USER

# Aplicar cambios (requiere logout/login)
newgrp podman

# Verificar
podman ps
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
source venv/bin/activate
```

### Paso 2: Actualizar pip

```bash
pip install --upgrade pip setuptools wheel
```

### Paso 3: Crear archivo requirements.txt

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

---

## Configuración de Podman

### Paso 1: Crear Red de Podman

```bash
# Crear red para los contenedores
podman network create ticketmaster-network

# Verificar red creada
podman network ls
```

### Paso 2: Crear Volúmenes Persistentes

```bash
# Volumen para PostgreSQL
podman volume create postgres-data

# Volumen para Redis
podman volume create redis-data

# Verificar volúmenes
podman volume ls
```

---

## Levantar Contenedores

### Opción 1: Usando docker-compose (Recomendado)

#### Paso 1: Crear archivo docker-compose.yml

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # ===== PostgreSQL =====
  postgres:
    image: docker.io/library/postgres:15-alpine
    container_name: ticketmaster-postgres
    environment:
      POSTGRES_USER: ticketmaster
      POSTGRES_PASSWORD: tu_contraseña_segura
      POSTGRES_DB: ticketmaster_db
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=C"
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - ticketmaster-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ticketmaster"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # ===== Redis =====
  redis:
    image: docker.io/library/redis:7-alpine
    container_name: ticketmaster-redis
    command: redis-server --appendonly yes --requirepass tu_contraseña_redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - ticketmaster-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local

networks:
  ticketmaster-network:
    driver: bridge
EOF
```

#### Paso 2: Levantar Contenedores con Podman Compose

```bash
# Instalar podman-compose si no está instalado
sudo dnf install -y podman-compose

# O instalarlo con pip
pip install podman-compose

# Levantar contenedores
podman-compose up -d

# Verificar estado
podman-compose ps

# Ver logs
podman-compose logs -f
```

### Opción 2: Usando Podman Directamente

#### Paso 1: Levantar PostgreSQL

```bash
podman run -d \
  --name ticketmaster-postgres \
  --network ticketmaster-network \
  -e POSTGRES_USER=ticketmaster \
  -e POSTGRES_PASSWORD=tu_contraseña_segura \
  -e POSTGRES_DB=ticketmaster_db \
  -p 5432:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  docker.io/library/postgres:15-alpine

# Verificar que está corriendo
podman ps | grep postgres
```

#### Paso 2: Levantar Redis

```bash
podman run -d \
  --name ticketmaster-redis \
  --network ticketmaster-network \
  -p 6379:6379 \
  -v redis-data:/data \
  docker.io/library/redis:7-alpine \
  redis-server --appendonly yes --requirepass tu_contraseña_redis

# Verificar que está corriendo
podman ps | grep redis
```

---

## Verificar Contenedores

### Paso 1: Listar Contenedores

```bash
# Ver todos los contenedores
podman ps -a

# Ver solo contenedores corriendo
podman ps
```

### Paso 2: Ver Logs

```bash
# Logs de PostgreSQL
podman logs ticketmaster-postgres

# Logs de Redis
podman logs ticketmaster-redis

# Seguir logs en tiempo real
podman logs -f ticketmaster-postgres
```

### Paso 3: Acceder a los Contenedores

```bash
# Acceder a PostgreSQL
podman exec -it ticketmaster-postgres psql -U ticketmaster -d ticketmaster_db

# Acceder a Redis
podman exec -it ticketmaster-redis redis-cli -a tu_contraseña_redis
```

---

## Configuración del Proyecto

### Paso 1: Crear archivo .env

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
REDIS_PASSWORD=tu_contraseña_redis
REDIS_DB=0

# ===== APLICACIÓN =====
APP_NAME=Ticketmaster
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# ===== SEGURIDAD =====
SECRET_KEY=tu_clave_secreta_muy_larga_y_segura_aqui_cambiar_en_produccion
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
CELERY_BROKER_URL=redis://:tu_contraseña_redis@localhost:6379/0
CELERY_RESULT_BACKEND=redis://:tu_contraseña_redis@localhost:6379/0
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
    REDIS_PASSWORD: Optional[str] = None
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
        if self.REDIS_PASSWORD:
            return (
                f"redis://:{self.REDIS_PASSWORD}@"
                f"{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
            )
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
    echo=False,
    future=True,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
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
    password=settings.REDIS_PASSWORD,
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

---

## Comandos Útiles de Podman

### Gestión de Contenedores

```bash
# Ver contenedores corriendo
podman ps

# Ver todos los contenedores
podman ps -a

# Detener contenedor
podman stop ticketmaster-postgres

# Iniciar contenedor
podman start ticketmaster-postgres

# Reiniciar contenedor
podman restart ticketmaster-postgres

# Eliminar contenedor
podman rm ticketmaster-postgres

# Ver logs
podman logs ticketmaster-postgres

# Seguir logs en tiempo real
podman logs -f ticketmaster-postgres
```

### Gestión de Volúmenes

```bash
# Listar volúmenes
podman volume ls

# Inspeccionar volumen
podman volume inspect postgres-data

# Eliminar volumen
podman volume rm postgres-data
```

### Gestión de Redes

```bash
# Listar redes
podman network ls

# Inspeccionar red
podman network inspect ticketmaster-network

# Eliminar red
podman network rm ticketmaster-network
```

### Acceder a Contenedores

```bash
# Acceder a PostgreSQL
podman exec -it ticketmaster-postgres psql -U ticketmaster -d ticketmaster_db

# Acceder a Redis
podman exec -it ticketmaster-redis redis-cli -a tu_contraseña_redis

# Ejecutar comando en contenedor
podman exec ticketmaster-postgres pg_dump -U ticketmaster ticketmaster_db > backup.sql
```

---

## Detener y Limpiar

### Opción 1: Con docker-compose

```bash
# Detener contenedores
podman-compose down

# Detener y eliminar volúmenes
podman-compose down -v

# Detener y eliminar todo (incluyendo imágenes)
podman-compose down -v --rmi all
```

### Opción 2: Con Podman

```bash
# Detener contenedores
podman stop ticketmaster-postgres ticketmaster-redis

# Eliminar contenedores
podman rm ticketmaster-postgres ticketmaster-redis

# Eliminar volúmenes
podman volume rm postgres-data redis-data

# Eliminar red
podman network rm ticketmaster-network
```

---

## Checklist de Verificación

```
✅ Python 3.9+ instalado
✅ Podman instalado
✅ Entorno virtual creado y activado
✅ Librerías instaladas (pip list)
✅ Red de Podman creada
✅ Volúmenes creados
✅ Contenedor PostgreSQL corriendo
✅ Contenedor Redis corriendo
✅ Archivo .env configurado
✅ app/core/config.py actualizado
✅ app/db/session.py actualizado
✅ app/db/cache.py creado
✅ Conexión a PostgreSQL verificada
✅ Conexión a Redis verificada
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

### Error: "Cannot connect to Podman"
```bash
# Verificar que Podman está corriendo
podman ps

# Si no funciona, reiniciar Podman
sudo systemctl restart podman
```

### Error: "Connection refused" en PostgreSQL
```bash
# Verificar que el contenedor está corriendo
podman ps | grep postgres

# Ver logs
podman logs ticketmaster-postgres

# Reiniciar contenedor
podman restart ticketmaster-postgres
```

### Error: "Connection refused" en Redis
```bash
# Verificar que el contenedor está corriendo
podman ps | grep redis

# Ver logs
podman logs ticketmaster-redis

# Reiniciar contenedor
podman restart ticketmaster-redis
```

### Error: "Port already in use"
```bash
# Cambiar puerto en docker-compose.yml o comando podman run
# Por ejemplo, usar 5433 en lugar de 5432:
# -p 5433:5432

# O encontrar qué proceso usa el puerto
sudo lsof -i :5432
```

### Error: "Permission denied" con Podman
```bash
# Agregar usuario al grupo podman
sudo usermod -aG podman $USER

# Aplicar cambios
newgrp podman

# Verificar
podman ps
```

---

## Referencias

- [Podman Documentation](https://docs.podman.io/)
- [Podman Compose](https://github.com/containers/podman-compose)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [Redis Docker Image](https://hub.docker.com/_/redis)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

