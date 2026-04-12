# Guía: Cómo y Por Qué se Construye con `.opencode` + Spec Driven Development

## ¿Qué es Spec Driven Development?

Spec Driven Development (SDD) es una práctica donde **la especificación es lo primero** que se escribe antes de tocar código. La especificación describe:

- Qué debe hacer el sistema
- Cómo deben comportarse sus partes
- Qué reglas no se pueden romper

En este proyecto, la especificación vive en dos lugares:
- `ARQUITECTURA_SISTEMA.md` → el "qué" y el "cómo" del sistema completo
- `.opencode/` → las reglas que el agente de IA debe seguir al construir

La idea central es: **el agente no inventa, ejecuta la especificación**.

---

## Estructura del `.opencode` y por qué existe cada parte

```
.opencode/
├── settings.json
├── hooks/
│   └── pre-commit.sh
└── skills/
    ├── backend-layer/
    │   └── SKILL.md
    ├── code-review/
    │   └── SKILL.md
    ├── react-component/
    │   └── SKILL.md
    └── refactor/
        └── SKILL.md
```

---

## `settings.json` — La especificación de objetivos

```json
{
  "permissions": { "allow": ["Bash", "Read", "Write", "Edit", "Glob", "Grep"] },
  "goals": [
    "Mantener arquitectura Clean Architecture en backend/",
    "Separar concerns: API → Service → Repository",
    ...
  ]
}
```

### Por qué existe

Es el contrato principal entre el desarrollador y el agente. Cada `goal` es una regla de negocio o arquitectural que el agente debe respetar en **cada acción que tome**, sin que el desarrollador tenga que repetirla en cada prompt.

### Cómo aplica SDD aquí

En SDD, la especificación se escribe antes del código. El `settings.json` cumple ese rol: antes de que el agente escriba una sola línea, ya sabe que los PDFs se procesan en memoria, que la `SECRET_KEY` va en `.env`, y que la arquitectura es Clean Architecture. El agente no toma decisiones de diseño, las ejecuta.

### Regla práctica

Cada vez que el sistema evoluciona (nuevo módulo, nueva restricción), primero se actualiza `settings.json`, luego se le pide al agente que construya. Nunca al revés.

---

## `skills/backend-layer/SKILL.md` — La especificación de construcción

```markdown
## Orden obligatorio al crear una entidad nueva
1. models/       → define la tabla en BD
2. schemas/      → define entrada y salida de datos
3. repositories/ → consultas a BD
4. services/     → lógica de negocio
5. api/          → endpoint HTTP
```

### Por qué existe

Sin esta skill, el agente podría crear un endpoint antes de tener el schema, o poner lógica de negocio directamente en el endpoint. Esta skill especifica el **orden y la responsabilidad de cada capa**.

### Cómo aplica SDD aquí

En SDD, la especificación define el proceso de construcción, no solo el resultado. Esta skill es exactamente eso: el proceso paso a paso que garantiza que cada entidad nueva siga la misma arquitectura. El agente no decide cómo construir, sigue el orden especificado.

### Por qué el orden models → schemas → api

- `models` primero porque define la fuente de verdad (la BD)
- `schemas` segundo porque define los contratos de entrada/salida antes de escribir lógica
- `repositories` tercero porque encapsula el acceso a datos antes de que el service lo use
- `services` cuarto porque la lógica de negocio depende del repository, no al revés
- `api` último porque solo orquesta, no decide

---

## `skills/code-review/SKILL.md` — La especificación de calidad

```markdown
### Service Layer
- [ ] PDF: valida extensión `.pdf` y tamaño máximo 10MB antes de procesar
- [ ] PDF: procesado en memoria con `BytesIO`, sin guardar en disco
- [ ] SECRET_KEY leída desde `.env`, nunca hardcodeada
```

### Por qué existe

Define qué significa "código correcto" en este proyecto. Sin esta skill, una revisión de código dependería del criterio del momento. Con ella, el agente tiene un checklist fijo y reproducible.

### Cómo aplica SDD aquí

En SDD, los criterios de aceptación se escriben antes del código. Esta skill es la lista de criterios de aceptación técnicos. Cuando el agente revisa código, no opina, verifica contra la especificación. Si un endpoint no usa `Depends(get_current_active_user)`, falla el criterio, independientemente de si "funciona".

### Por qué los checks son específicos al proyecto

Un checklist genérico ("¿tiene manejo de errores?") no aporta valor. Los checks deben reflejar las decisiones de arquitectura del proyecto: en este sistema, procesar un PDF en disco es un error aunque funcione, porque viola la especificación de privacidad y rendimiento.

---

## `skills/react-component/SKILL.md` — La especificación del frontend

```markdown
## Componentes del sistema
- Login.tsx          → registro e inicio de sesión
- Dashboard.tsx      → vista principal tras autenticarse
- PdfUpload.tsx      → carga de PDF y muestra resultado por página
- ProtectedRoute.tsx → redirige a /login si no hay token

## Reglas
- [ ] Peticiones API siempre mediante `src/utils/api.ts`
- [ ] Token JWT se maneja solo desde `AuthContext`
```

### Por qué existe

Especifica dos cosas: qué componentes existen y cuáles son sus responsabilidades. Evita que el agente cree un componente que haga peticiones HTTP directamente con `fetch` en vez de usar `api.ts`, o que maneje el token fuera de `AuthContext`.

### Cómo aplica SDD aquí

La lista de componentes es el inventario de la UI especificado de antemano. El agente no inventa componentes nuevos ni duplica responsabilidades porque la especificación ya define qué existe y para qué sirve cada uno.

---

## `skills/refactor/SKILL.md` — La especificación de corrección

```markdown
## Cuándo refactorizar
- Lógica de negocio encontrada en un endpoint → mover a `Service`
- Query SQL encontrada en un `Service` → mover a `Repository`
- SECRET_KEY hardcodeada → mover a `.env`
```

### Por qué existe

Define cuándo el código está en el lugar equivocado y cómo corregirlo. Sin esta skill, el agente podría "arreglar" código moviéndolo a un lugar incorrecto o rompiendo contratos existentes.

### Cómo aplica SDD aquí

En SDD, el refactor no es libre, es guiado por la especificación. Esta skill convierte el refactor en un proceso determinista: si encuentras X en el lugar Y, muévelo al lugar Z siguiendo estos pasos. No hay ambigüedad.

---

## `hooks/pre-commit.sh` — La especificación ejecutable

```bash
python -m py_compile app/**/*.py && echo "✅ Python OK"
npx tsc --noEmit && echo "✅ TypeScript OK"
```

### Por qué existe

Es la especificación que se auto-verifica. Antes de cada commit, el sistema comprueba que el código cumple los contratos básicos de sintaxis en ambas capas (backend y frontend).

### Cómo aplica SDD aquí

En SDD, la especificación debe ser verificable. El hook convierte dos reglas implícitas ("el código debe compilar") en verificaciones automáticas. Si el agente genera código con un error de sintaxis, el hook lo detecta antes de que llegue al repositorio.

---

## El flujo completo con SDD

```
1. ESPECIFICAR
   └── Actualizar ARQUITECTURA_SISTEMA.md con el nuevo requerimiento
   └── Actualizar settings.json con nuevos goals si aplica
   └── Actualizar la SKILL relevante con nuevos criterios

2. CONSTRUIR
   └── El agente lee la especificación (settings.json + SKILL.md)
   └── Sigue el orden: models → schemas → repositories → services → api
   └── No toma decisiones de diseño, ejecuta la especificación

3. VERIFICAR
   └── El agente usa code-review/SKILL.md como checklist
   └── El hook pre-commit valida sintaxis automáticamente
   └── Si algo falla el checklist → refactor/SKILL.md define cómo corregir

4. EVOLUCIONAR
   └── Nuevo requerimiento → volver al paso 1
   └── La especificación siempre va adelante del código
```

---

## Por qué `.opencode` en la raíz y no dentro de `backend/` o `frontend/`

Porque la especificación es del **sistema completo**, no de una capa. El agente necesita contexto de ambas capas para tomar decisiones coherentes: sabe que `PdfUpload.tsx` consume `/api/pdf/extract-region`, que ese endpoint usa `PdfService`, y que `PdfService` procesa en memoria. Esa cadena completa es la especificación, y vive en un solo lugar.

Si hubiera un `.opencode` por carpeta, el agente tendría visión parcial y podría tomar decisiones que son correctas localmente pero incorrectas para el sistema.

---

## Resumen: qué hace cada archivo

| Archivo | Rol en SDD | Pregunta que responde |
|---|---|---|
| `settings.json` | Especificación de objetivos | ¿Qué reglas nunca se rompen? |
| `backend-layer/SKILL.md` | Especificación de proceso | ¿En qué orden y cómo se construye? |
| `code-review/SKILL.md` | Criterios de aceptación | ¿Qué significa que el código esté correcto? |
| `react-component/SKILL.md` | Inventario y contratos UI | ¿Qué componentes existen y qué hace cada uno? |
| `refactor/SKILL.md` | Especificación de corrección | ¿Cuándo y cómo se mueve código mal ubicado? |
| `pre-commit.sh` | Especificación ejecutable | ¿El código compila antes de hacer commit? |
| `OPENCODE.md` | Contexto del sistema | ¿Qué es este proyecto y cómo se ejecuta? |
