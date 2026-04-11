# Guía de Construcción: Backend PDF Extractor (Estructura OpenCode)

Este proyecto implementa un backend FastAPI siguiendo una arquitectura limpia y estructurada para **OpenCode** (`opencode_project/`).

## Estructura del Proyecto

```
opencode_project/
├── OPENCODE.md              # Config principal (Stack, Comandos, Reglas)
├── README.md              # Documentación usuario
├── docs/
│   ├── architecture.md    # Arquitectura del sistema
│   ├── decisions/         # ADRs
│   └── runbooks/          # Guías de operación
├── .opencode/             # Configuración de OpenCode
│   ├── settings.json
│   ├── hooks/
│   │   └── pre-commit.sh
│   └── skills/
│       ├── code-review/SKILL.md
│       └── refactor/SKILL.md
├── tools/
│   ├── scripts/
│   └── prompts/
└── src/
    ├── api/
    │   ├── OPENCODE.md      # Config capa API
    │   ├── router.py
    │   ├── auth.py
    │   ├── routes/
    │   ├── services/
    │   └── schemas/
    └── persistence/
        ├── OPENCODE.md      # Config capa datos
        ├── session.py
        ├── models/
        └── repositories/
```

---

## 1. Configuración del Proyecto (OPENCODE.md)

```markdown
# FastAPI PDF Extractor

## Tech Stack
- FastAPI 0.116.1, SQLModel, Alembic, SQLite/PostgreSQL
- Auth: JWT + bcrypt
- PDF: pdfplumber

## Estructura
- `src/api/`: Endpoints, Logica, Schemas
- `src/persistence/`: Modelos, Repositorios, DB

## Comandos
- Setup: `bash tools/scripts/setup.sh`
- Ejecutar: `cd src && uvicorn main:app --reload`
- Migraciones: `alembic upgrade head`
```

---

## 2. Configuración de OpenCode (`.opencode/`)

### `.opencode/settings.json`
```json
{
  "permissions": {
    "allow": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
  }
}
```

### `.opencode/hooks/pre-commit.sh`
```bash
#!/bin/bash
# Hook de validación pre-commit
echo "🔍 Validando sintaxis..."
python -m py_compile src/**/*.py
```

---

## 3. Implementación (Paso a Paso)

### Paso A: Estructura de Carpetas
```bash
mkdir -p opencode_project/{docs/{decisions,runbooks},.opencode/{hooks,skills/{code-review,refactor}},tools/{scripts,prompts},src/{api/{routes,services,schemas},persistence/{models,repositories}}}
```

### Paso B: Automatización (tools/)
- `tools/scripts/setup.sh`: Script para instalar dependencias y ejecutar migraciones.

### Paso C: Implementación de Código (`src/`)
1. **`src/persistence/models/user.py`**
2. **`src/persistence/session.py`**
3. **`src/persistence/repositories/user.py`**
4. **`src/api/schemas/user.py`**
5. **`src/api/services/user.py`**
6. **`src/api/routes/auth.py`**
7. **`src/api/router.py`**
8. **`src/main.py`**

---

## Próximos pasos

Para comenzar, ejecuta en tu terminal dentro de la carpeta raíz (`opencode_project/`):

1. **Crear carpetas**: (comando `mkdir -p ...` de arriba)
2. **Configurar entorno**: `python -m venv venv && source venv/bin/activate`
3. **Instalar dependencias**: `pip install -r src/requirements.txt`
4. **Migraciones**: `cd src && alembic init alembic && alembic upgrade head`
5. **Ejecutar**: `uvicorn main:app --reload`

¿Quieres que proceda a crear automáticamente esta estructura y los archivos principales usando esta nueva configuración?
