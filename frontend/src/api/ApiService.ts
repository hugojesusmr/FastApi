import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Los interceptores de Axios son funciones que se ejecutan antes o después de que se envíe una solicitud HTTP o se reciba una respuesta.

const api: AxiosInstance = axios.create({
    baseURL: "http://localhost:8000",
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptores de solicitud: Se utilizan para modificar solicitudes antes de que se envíen,como agregar encabezados de autenticación o lograr detalles de la solicitud.
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Interceptores de respuesta: Se utilizan para modificar respuestas después de que se reciben, como transformar datos o manejar errores. 
api.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;