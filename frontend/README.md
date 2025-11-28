# Sistema de Carga de Archivos Moderno

Sistema moderno de carga de archivos con React, TypeScript y FastAPI.

## Características

- ✅ Drag & Drop de archivos
- ✅ Selección múltiple de archivos
- ✅ Validación de tipos y tamaños
- ✅ Barra de progreso
- ✅ Previsualización de archivos
- ✅ Manejo de errores
- ✅ Interfaz responsive con Tailwind CSS

## Instalación

```bash
# Instalar dependencias
npm install

# Instalar Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Iniciar desarrollo
npm start
```

## Uso del Componente

```tsx
import { FileUpload } from './components/FileUpload';
import { useFileUpload } from './hooks/useFileUpload';

function App() {
  const { uploadFiles, isUploading, progress } = useFileUpload();

  const handleFiles = async (files: File[]) => {
    await uploadFiles(files, {
      url: 'http://localhost:8000/api/upload-multiple'
    });
  };

  return (
    <FileUpload
      onFilesSelected={handleFiles}
      maxFiles={10}
      maxSize={50}
      acceptedTypes={['image/*', 'application/pdf']}
      multiple={true}
    />
  );
}
```

## API FastAPI

El backend incluye endpoints para:

- `POST /api/upload` - Subir un archivo
- `POST /api/upload-multiple` - Subir múltiples archivos

## Configuración

Ajusta la URL del API en `App.tsx`:

```tsx
const API_URL = 'http://localhost:8000/api';
```