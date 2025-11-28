import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { dashboardApi, DashboardData } from '../api';

interface MLDashboardProps {
  token: string;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

const MLDashboard: React.FC<MLDashboardProps> = ({ token }) => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Actualizar cada 30 segundos
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      console.log('🔄 Cargando datos del dashboard...');
      const dashboardData = await dashboardApi.getDashboardData();
      console.log('✅ Datos recibidos:', dashboardData);
      setData(dashboardData);
      setError(null);
    } catch (err: any) {
      console.error('💥 Error completo:', err);
      setError(err.response?.data?.detail || err.message || 'Error al cargar datos');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '200px' }}>
        <div style={{ 
          width: '40px', 
          height: '40px', 
          border: '4px solid #f3f4f6', 
          borderTop: '4px solid #4f46e5', 
          borderRadius: '50%', 
          animation: 'spin 1s linear infinite' 
        }}></div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        background: '#fef2f2', 
        border: '1px solid #fecaca', 
        borderRadius: '8px', 
        padding: '16px',
        color: '#dc2626'
      }}>
        ⚠️ {error}
      </div>
    );
  }

  if (!data) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
      
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '32px' }}>🧠</span>
          <h2 style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937', margin: 0 }}>ML Analytics Dashboard</h2>
        </div>
        <div style={{ fontSize: '14px', color: '#6b7280' }}>
          Última actualización: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Métricas Principales */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
        gap: '16px' 
      }}>
        <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span style={{ fontSize: '32px', marginRight: '16px' }}>🎯</span>
            <div>
              <p style={{ fontSize: '14px', fontWeight: '500', color: '#6b7280', margin: '0 0 4px 0' }}>Total Tareas</p>
              <p style={{ fontSize: '24px', fontWeight: '600', color: '#1f2937', margin: 0 }}>{data.metrics.total_tasks}</p>
            </div>
          </div>
        </div>

        <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span style={{ fontSize: '32px', marginRight: '16px' }}>📈</span>
            <div>
              <p style={{ fontSize: '14px', fontWeight: '500', color: '#6b7280', margin: '0 0 4px 0' }}>Completadas</p>
              <p style={{ fontSize: '24px', fontWeight: '600', color: '#1f2937', margin: 0 }}>{data.metrics.completed_tasks}</p>
            </div>
          </div>
        </div>

        <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span style={{ fontSize: '32px', marginRight: '16px' }}>⏰</span>
            <div>
              <p style={{ fontSize: '14px', fontWeight: '500', color: '#6b7280', margin: '0 0 4px 0' }}>Pendientes</p>
              <p style={{ fontSize: '24px', fontWeight: '600', color: '#1f2937', margin: 0 }}>{data.metrics.pending_tasks}</p>
            </div>
          </div>
        </div>

        <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span style={{ fontSize: '32px', marginRight: '16px' }}>⚠️</span>
            <div>
              <p style={{ fontSize: '14px', fontWeight: '500', color: '#6b7280', margin: '0 0 4px 0' }}>Alta Prioridad</p>
              <p style={{ fontSize: '24px', fontWeight: '600', color: '#1f2937', margin: 0 }}>{data.metrics.high_priority_tasks}</p>
            </div>
          </div>
        </div>

        <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <span style={{ fontSize: '32px', marginRight: '16px' }}>👥</span>
            <div>
              <p style={{ fontSize: '14px', fontWeight: '500', color: '#6b7280', margin: '0 0 4px 0' }}>Tiempo Promedio</p>
              <p style={{ fontSize: '24px', fontWeight: '600', color: '#1f2937', margin: 0 }}>{data.metrics.avg_completion_time}h</p>
            </div>
          </div>
        </div>
      </div>

      {/* Gráficas Principales */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', 
        gap: '24px' 
      }}>
        {/* Tendencias de Productividad */}
        <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937', marginBottom: '16px' }}>Tendencias de Productividad</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data.productivity_trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="completed_count" stroke="#10b981" name="Completadas" />
              <Line type="monotone" dataKey="created_count" stroke="#3b82f6" name="Creadas" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Distribución de Prioridades */}
        <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937', marginBottom: '16px' }}>Distribución por Prioridad</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={data.priority_distribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="percentage"
                nameKey="priority"
              >
                {data.priority_distribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Performance de Asignados */}
      <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
        <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937', marginBottom: '16px' }}>Performance por Asignado</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data.assignee_performance.slice(0, 8)}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="assignee" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="completed_tasks" fill="#3b82f6" name="Tareas Completadas" />
            <Bar dataKey="efficiency_score" fill="#10b981" name="Score de Eficiencia" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Predicciones ML y Cuellos de Botella */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: '24px' 
      }}>
        {/* Predicciones */}
        <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937', marginBottom: '16px' }}>🔮 Predicciones ML</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '14px', color: '#6b7280' }}>Tareas próxima semana:</span>
              <span style={{ fontWeight: '600', color: '#3b82f6' }}>{data.predictions.tasks_next_week}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '14px', color: '#6b7280' }}>Tasa de finalización:</span>
              <span style={{ fontWeight: '600', color: '#10b981' }}>{data.predictions.completion_rate_forecast}%</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '14px', color: '#6b7280' }}>Tareas de alto riesgo:</span>
              <span style={{ fontWeight: '600', color: '#ef4444' }}>{data.predictions.high_risk_tasks}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '14px', color: '#6b7280' }}>Utilización de recursos:</span>
              <span style={{ fontWeight: '600', color: '#8b5cf6' }}>{data.predictions.resource_utilization}%</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '14px', color: '#6b7280' }}>Cumplimiento SLA:</span>
              <span style={{ fontWeight: '600', color: '#4f46e5' }}>{data.predictions.sla_compliance_forecast}%</span>
            </div>
          </div>
        </div>

        {/* Cuellos de Botella */}
        <div style={{ background: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)', padding: '24px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#1f2937', marginBottom: '16px' }}>⚠️ Cuellos de Botella Detectados</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {data.bottlenecks.length > 0 ? (
              data.bottlenecks.map((bottleneck, index) => (
                <div key={index} style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
                  <span style={{ color: '#f59e0b', fontSize: '16px' }}>⚠️</span>
                  <span style={{ fontSize: '14px', color: '#374151' }}>{bottleneck}</span>
                </div>
              ))
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{ color: '#10b981', fontSize: '16px' }}>📈</span>
                <span style={{ fontSize: '14px', color: '#374151' }}>No se detectaron cuellos de botella</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MLDashboard;