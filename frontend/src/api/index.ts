// Exportar todas las APIs desde un solo punto
export { authApi } from './authApi';
export { tareasApi } from './tareasApi';
export { dashboardApi } from './dashboardApi';
export { default as api } from './ApiService';

// Re-exportar tipos
export type { 
  LoginRequest, 
  RegisterRequest, 
  LoginResponse, 
  UserResponse 
} from './authApi';

export type { 
  TareaResponse 
} from './tareasApi';

export type { 
  DashboardData 
} from './dashboardApi';