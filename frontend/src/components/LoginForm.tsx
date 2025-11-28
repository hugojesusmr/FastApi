import React, { useState } from 'react';
import { authApi } from '../api';
import './LoginForm.css';

const LoginForm: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isLogin) {
        const response = await authApi.login({
          username: formData.username,
          password: formData.password
        });
        authApi.saveToken(response.access_token);
        // Actualizar el estado de autenticación
        window.dispatchEvent(new Event('auth-changed'));
      } else {
        await authApi.register({
          email: formData.email,
          username: formData.username,
          password: formData.password
        });
        setIsLogin(true);
        setError('Registro exitoso. Ahora puedes iniciar sesión.');
      }
    } catch (err: any) {
      console.error('Error:', err);
      if (err.code === 'ERR_NETWORK') {
        setError('No se puede conectar al servidor. Asegúrate de que el backend esté ejecutándose en http://localhost:8000');
      } else if (err.response?.status === 401) {
        setError('Credenciales incorrectas');
      } else if (err.response?.status === 400) {
        setError(err.response?.data?.detail || 'Datos inválidos');
      } else {
        setError(err.response?.data?.detail || 'Error en la operación');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h2 className="login-title">
            {isLogin ? 'Iniciar Sesión' : 'Registrarse'}
          </h2>
          <p className="login-subtitle">
            {isLogin ? 'Accede a tu cuenta' : 'Crea una nueva cuenta'}
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <div>
            {!isLogin && (
              <div className="form-group">
                <label htmlFor="email" className="form-label">
                  Email
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  required={!isLogin}
                  value={formData.email}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="tu@email.com"
                />
              </div>
            )}

            <div className="form-group">
              <label htmlFor="username" className="form-label">
                Usuario
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="form-input"
                placeholder="tu_usuario"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password" className="form-label">
                Contraseña
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="form-input"
                placeholder="••••••••"
              />
            </div>
          </div>

          {error && (
            <div className={`error-message ${error.includes('exitoso') ? 'success' : 'error'}`}>
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="submit-button"
          >
            {loading ? 'Procesando...' : (isLogin ? 'Iniciar Sesión' : 'Registrarse')}
          </button>

          <div className="toggle-container">
            <button
              type="button"
              onClick={() => {
                setIsLogin(!isLogin);
                setError('');
                setFormData({ email: '', username: '', password: '' });
              }}
              className="toggle-button"
            >
              {isLogin ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;