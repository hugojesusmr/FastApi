import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import api from '../utils/api';
import type { MLDashboardResponse } from '../types/api';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const { username } = useAuth();
  const [data, setData] = useState<MLDashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/data');
        setData(response.data);
      } catch (err) {
        setError('Error cargando datos del dashboard');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="loading">Cargando...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dashboard-content">
      <h1>Bienvenido, {username}!</h1>
      <div className="dashboard-stats">
        {/* Placeholder based on MLDashboardResponse */}
        <div className="stat-card">
          <h3>Total Usuarios</h3>
          <p>{data?.data?.totalUsers || 0}</p>
        </div>
        {/* Add more stats */}
      </div>
      {/* Charts, tables etc */}
    </div>
  );
};

export default Dashboard;

