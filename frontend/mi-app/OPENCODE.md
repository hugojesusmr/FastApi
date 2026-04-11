# Frontend - React + Vite + TypeScript (Configuración OpenCode)

## Tech Stack
- React 19
- TypeScript
- Vite 8
- Axios (con interceptor JWT)

## Estructura
- `src/components/`: Componentes UI reutilizables
- `src/contexts/`: Manejo de estado (AuthContext)
- `src/utils/`: APIs y helpers
- `src/types/`: Definiciones de TypeScript

## Reglas
- Usar componentes funcionales con TypeScript (`FC`).
- Estilos en archivos `.css` (por componente).
- Peticiones API siempre mediante `src/utils/api.ts` (para incluir token JWT).
EOF
