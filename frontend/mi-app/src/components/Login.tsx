import React, { useState, type FormEvent } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';
import { User, Lock } from 'lucide-react';
import api from '../utils/api';
import type { UserLogin, UserCreate } from '../types/api';
import './Login.css';

const Login: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const auth = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';
      const data: UserLogin | UserCreate = isLogin 
        ? { username: formData.username, password: formData.password }
        : formData;

      const response = await api.post(endpoint, data);

      if (isLogin) {
        auth.login(response.data.access_token, formData.username);
        navigate(from, { replace: true });
      } else {
        setIsLogin(true);
        setError('Usuario creado exitosamente. Ahora inicia sesión.');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error de autenticación');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = () => {
    setIsLogin(!isLogin);
    setError('');
  };

  return (
    <div className="login-page">
      <div className="login-wrapper">
        <div className="login-header">
          <div className="logo">
            <User size={28} />
          </div>
          <h2 className="login-title">{isLogin ? 'Bienvenido' : 'Registrarse'}</h2>
        </div>

        <form onSubmit={handleSubmit}>
          {error && (
            <div className={`error-message ${error.includes('exitoso') ? 'success' : ''}`}>
              {error}
            </div>
          )}

          <div className="form-group">
            <label>Usuario</label>
            <div className="input-wrapper">
              <div className="icon-box">
                <User size={20} />
              </div>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Contraseña</label>
            <div className="input-wrapper">
              <div className="icon-box">
                <Lock size={20} />
              </div>
              <input
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                required
              />
            </div>
          </div>

          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? 'Cargando...' : (isLogin ? 'Iniciar Sesión' : 'Crear Cuenta')}
          </button>

          <div className="toggle-container">
            <p className="toggle-button">
              {isLogin ? '¿No tienes cuenta?' : '¿Ya tienes cuenta?'}
              <span onClick={handleToggle} className="toggle-link">
                {isLogin ? ' Regístrate' : ' Iniciar sesión'}
              </span>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
