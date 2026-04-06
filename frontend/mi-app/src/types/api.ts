// Tipos para API (infer from backend schemas)

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserCreate {
  email: string;
  username: string;
  password: string;
}

export interface UserResponse {
  id: number;
  email: string;
  username: string;
}

// Ajustar según MLDashboardResponse from backend
export interface MLDashboardResponse {
  // Definir campos según service
  data: any; // Placeholder
}

