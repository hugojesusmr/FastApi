# ADR 002: Clean Architecture para el Backend

## Contexto
El sistema PDF Extractor necesita ser mantenible, escalable y fácil de testear (TDD).

## Decisión
Implementar una arquitectura de 4 capas: API Layer, Service Layer, Repository Layer, y Data Layer.

## Justificación
1.  **Desacoplamiento**: La lógica de negocio (Services) es independiente del protocolo de transporte (HTTP, gRPC, CLI) y de la base de datos (SQL).
2.  **Testabilidad**: Permite testear lógica de negocio sin conexión a la base de datos (mocking de repositorios).
3.  **Escalabilidad**: Facilita agregar nuevos endpoints (`pdf.py`, `dashboard.py`) sin modificar código existente.
EOF
,filePath: