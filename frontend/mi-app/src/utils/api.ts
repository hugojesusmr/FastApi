import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const api = axios.create({
  baseURL: '/api', // Proxied to backend
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

