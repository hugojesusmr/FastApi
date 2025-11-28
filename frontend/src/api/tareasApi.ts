import api from './ApiService';

// Tipos para tareas (basado en tus esquemas del backend)
export interface TareaResponse {
  id_tarea: string;
  grupo_de_asignacion?: string;
  plataforma?: string;
  nombre_de_tarea?: string;
  prioridad?: string;
  incidente?: string;
  estado?: string;
  fecha_de_creacion?: string;
  // ... otros campos según tu esquema
}

// Funciones para tareas
export const tareasApi = {
  // Subir archivo de tareas
  uploadFile: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/tareas/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Obtener todas las tareas
  getTareas: async (): Promise<TareaResponse[]> => {
    const response = await api.get('/tareas');
    return response.data;
  },

  // Obtener tarea por ID
  getTarea: async (id: string): Promise<TareaResponse> => {
    const response = await api.get(`/tareas/${id}`);
    return response.data;
  }
};