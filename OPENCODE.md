# FastAPI Backend - Sistema de Autenticación (Configuración OpenCode)

## Tech Stack
- **Framework**: FastAPI 0.116.1
- **DB**: SQLite (async) + Alembic
- **Auth**: JWT + bcrypt
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Server**: Uvicorn

## Arquitectura
`backend/app/` (Clean Architecture: API → Service → Repository → DB)

## Estructura
- `backend/app/api/`: Endpoints HTTP
- `backend/app/core/`: Config, Auth, Utilidades
- `backend/app/db/`: Conexión BD
- `backend/app/models/`: Modelos SQLModel
- `backend/app/repositories/`: Acceso a BD
- `backend/app/schemas/`: Pydantic Schemas
- `backend/app/services/`: Lógica de negocio

## Frontend
- `frontend/mi-app/`: React + Vite + TS (Ver `frontend/mi-app/OPENCODE.md`)

## Comandos Principales
```bash
# Setup
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Migraciones
alembic revision --autogenerate -m "mensaje"
alembic upgrade head

# Ejecutar
uvicorn app.main:app --reload --port 8000
```

## Convenciones
- Toda interacción con DB va por `Repository`.
- Toda lógica de negocio va por `Service`.
- APIs solo reciben/retornan Pydantic Schemas.
EOF
