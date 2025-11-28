import React, { useState, useEffect } from 'react';
import { authApi } from '../api';
import MLDashboard from './MLDashboard';
import './Dashboard.css';

interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const loadUserProfile = async () => {
      try {
        const userProfile = await authApi.getProfile();
        setUser(userProfile);
      } catch (error) {
        // Si hay error, redirigir al login
        authApi.logout();
        window.location.href = '/';
      } finally {
        setLoading(false);
      }
    };

    loadUserProfile();
  }, []);

  const handleLogout = () => {
    authApi.logout();
    window.dispatchEvent(new Event('auth-changed'));
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="dashboard-loading-text">
          Cargando...
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="dashboard-header-content">
          <h1 className="dashboard-title">
            Sistema de Tareas
          </h1>
          
          <div className="dashboard-user-section">
            <span className="dashboard-welcome-text">
              Bienvenido, {user?.username}
            </span>
            <button
              onClick={handleLogout}
              className="dashboard-logout-btn"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="dashboard-nav">
        <div className="dashboard-nav-content">
          <button
            onClick={() => setActiveTab('overview')}
            className={`dashboard-nav-btn ${activeTab === 'overview' ? 'active' : ''}`}
          >
            🏠 Resumen
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`dashboard-nav-btn ${activeTab === 'analytics' ? 'active' : ''}`}
          >
            📊 ML Analytics
          </button>
          <button
            onClick={() => setActiveTab('tasks')}
            className={`dashboard-nav-btn ${activeTab === 'tasks' ? 'active' : ''}`}
          >
            📋 Tareas
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <main className="dashboard-main">
        {activeTab === 'overview' && (
          <>
            {/* Welcome Message */}
            <div className="dashboard-welcome-card">
              <h2 className="dashboard-welcome-title">
                ¡Sesión iniciada correctamente!
              </h2>
              <p className="dashboard-welcome-subtitle">
                Bienvenido al sistema de gestión de tareas, {user?.username}
              </p>
            </div>

        {/* User Info Card */}
        <div className="dashboard-card">
          <h3 className="dashboard-card-title">
            Información del Usuario
          </h3>
          
          <div className="dashboard-user-info">
            <div className="dashboard-info-item">
              <span className="dashboard-info-label">Usuario:</span>
              <span className="dashboard-info-value">{user?.username}</span>
            </div>
            <div className="dashboard-info-item">
              <span className="dashboard-info-label">Email:</span>
              <span className="dashboard-info-value">{user?.email}</span>
            </div>
            <div className="dashboard-info-item">
              <span className="dashboard-info-label">Estado:</span>
              <span className={`dashboard-info-value ${user?.is_active ? 'active' : 'inactive'}`}>
                {user?.is_active ? 'Activo' : 'Inactivo'}
              </span>
            </div>
            <div className="dashboard-info-item">
              <span className="dashboard-info-label">Registrado:</span>
              <span className="dashboard-info-value">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString('es-ES') : 'N/A'}
              </span>
            </div>
          </div>
        </div>
          </>
        )}

        {activeTab === 'analytics' && (
          <MLDashboard token={localStorage.getItem('access_token') || ''} />
        )}

        {activeTab === 'tasks' && (
          <div className="dashboard-card">
            <h3 className="dashboard-card-title">
              Gestión de Tareas
            </h3>
            <p className="dashboard-info-text">
              Funcionalidad de tareas próximamente...
            </p>
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;