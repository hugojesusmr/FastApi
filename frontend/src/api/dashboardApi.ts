import api from './ApiService';

export interface DashboardData {
  metrics: {
    total_tasks: number;
    completed_tasks: number;
    pending_tasks: number;
    high_priority_tasks: number;
    avg_completion_time: number;
  };
  productivity_trends: Array<{
    date: string;
    completed_count: number;
    created_count: number;
    efficiency_score: number;
  }>;
  priority_distribution: Array<{
    priority: string;
    count: number;
    percentage: number;
  }>;
  assignee_performance: Array<{
    assignee: string;
    completed_tasks: number;
    avg_time: number;
    efficiency_score: number;
  }>;
  bottlenecks: string[];
  predictions: {
    tasks_next_week: number;
    completion_rate_forecast: number;
    high_risk_tasks: number;
    resource_utilization: number;
    sla_compliance_forecast: number;
  };
}

export const dashboardApi = {
  getDashboardData: async (): Promise<DashboardData> => {
    const response = await api.get('/dashboard/data');
    return response.data;
  }
};