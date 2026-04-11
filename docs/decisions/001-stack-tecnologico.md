# ADR 001: Selección del Stack Tecnológico

## Contexto
Se requiere construir un backend rápido, escalable y mantenible para extraer texto de archivos PDF.

## Decisión
Usar **FastAPI** con **SQLModel** y **SQLite** (con migración a PostgreSQL) como stack base.

## Justificación
1.  **FastAPI**: Soporte nativo para async/await, tipado estricto (Pydantic), rendimiento superior y documentación automática (OpenAPI).
2.  **SQLModel**: Combina `SQLAlchemy` (potencia) y `Pydantic` (facilidad de uso), permitiendo definir modelos únicos tanto para BD como para esquemas de API.
3.  **SQLite/PostgreSQL**: Facilidad de desarrollo local (SQLite) con portabilidad a producción (PostgreSQL) usando `SQLAlchemy`.
EOF
,filePath: