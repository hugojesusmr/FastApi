# Arquitectura del Sistema - PDF Extractor

## 1. Visión General
El sistema **PDF Extractor** es una aplicación diseñada para cargar documentos PDF, extraer texto de ellos y devolver el contenido estructurado por página.

## 2. Stack Tecnológico
- **Backend**: FastAPI (Python 3.12+), SQLModel, Alembic, SQLite/PostgreSQL.
- **Frontend**: React 19 + TypeScript.
- **Auth**: JWT + bcrypt.
- **PDF**: pdfplumber.

## 3. Arquitectura Backend (Clean Architecture)
El backend sigue estrictamente 4 capas para garantizar mantenibilidad y testabilidad:

1.  **API Layer (`src/api/`)**: Gestión de rutas, schemas Pydantic y delegación a servicios.
2.  **Service Layer (`src/api/services/`)**: Lógica de negocio pura (validaciones, coordinación).
3.  **Repository Layer (`src/persistence/repositories/`)**: Consultas SQL contra la DB.
4.  **Data Layer (`src/persistence/models/`, `session.py`)**: Definición de datos y conexión.

## 4. Flujo de Datos
- `Request` (HTTP) -> `API Endpoint` -> `Service` -> `Repository` -> `DB`
- `Response` (JSON) <- `API Endpoint` <- `Service` <- `Repository` <- `DB`
EOF
,filePath: