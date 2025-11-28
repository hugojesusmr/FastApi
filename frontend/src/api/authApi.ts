import api from './ApiService';

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}
export interface LoginRequest {
  username: string;
  password: string;
}
export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
}

// Funciones de autenticación
export const authApi = {
  // POST /auth/login
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  // POST /auth/register
  register: async (userData: RegisterRequest): Promise<UserResponse> => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  // GET /auth/me
  getProfile: async (): Promise<UserResponse> => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  // Función helper para guardar token
  saveToken: (token: string) => {
    localStorage.setItem('access_token', token);
  },

  // Función helper para logout
  logout: () => {
    localStorage.removeItem('access_token');
  }
};