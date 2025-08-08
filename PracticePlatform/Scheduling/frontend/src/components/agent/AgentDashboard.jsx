// =============================================================================
// FILE: frontend/src/components/agent/AgentDashboard.jsx
// =============================================================================
import React, { useState, useEffect } from 'react';
import {
  Bot,
  Activity,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  BarChart3,
  TrendingUp,
  TrendingDown,
  Users,
  Calendar,
  FileText,
  Settings,
  RefreshCw,
  Download,
  Trash2,
  Play,
  Pause
} from 'lucide-react';
import { toast } from 'react-toastify';
import { agentService } from '../../services/agentService';

const AgentDashboard = () => {
  const [agentStatus, setAgentStatus] = useState(null);
  const [healthStatus, setHealthStatus] = useState(null);
  const [performanceMetrics, setPerformanceMetrics] = useState(null);
  const [taskStatistics, setTaskStatistics] = useState(null);
  const [activeTasks, setActiveTasks] = useState([]);
  const [taskHistory, setTaskHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [
        statusData,
        healthData,
        performanceData,
        statisticsData,
        activeTasksData,
        historyData
      ] = await Promise.all([
        agentService.getAgentStatus(),
        agentService.getAgentHealth(),
        agentService.getPerformanceMetrics(),
        agentService.getTaskStatistics(),
        agentService.getActiveTasks(),
        agentService.getTaskHistory(10)
      ]);

      setAgentStatus(statusData);
      setHealthStatus(healthData);
      setPerformanceMetrics(performanceData);
      setTaskStatistics(statisticsData);
      setActiveTasks(activeTasksData);
      setTaskHistory(historyData);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const refreshData = async () => {
    setRefreshing(true);
    await loadDashboardData();
    setRefreshing(false);
    toast.success('Dashboard refreshed');
  };

  const resetMetrics = async () => {
    if (window.confirm('Are you sure you want to reset all agent metrics? This action cannot be undone.')) {
      try {
        await agentService.resetAgentMetrics();
        toast.success('Agent metrics reset successfully');
        await loadDashboardData();
      } catch (error) {
        console.error('Error resetting metrics:', error);
        toast.error('Failed to reset metrics');
      }
    }
  };

  const clearHistory = async () => {
    if (window.confirm('Are you sure you want to clear old task history?')) {
      try {
        const result = await agentService.clearTaskHistory(30);
        toast.success(`Cleared ${result.cleared_count} old task records`);
        await loadDashboardData();
      } catch (error) {
        console.error('Error clearing history:', error);
        toast.error('Failed to clear history');
      }
    }
  };

  const exportData = async (type) => {
    try {
      let data;
      let filename;
      
      if (type === 'history') {
        data = await agentService.exportTaskHistory('json');
        filename = 'agent-task-history.json';
      } else if (type === 'metrics') {
        data = await agentService.exportMonitoringMetrics('json');
        filename = 'agent-metrics.json';
      }

      // Create and download file
      const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      toast.success(`${type} exported successfully`);
    } catch (error) {
      console.error('Error exporting data:', error);
      toast.error('Failed to export data');
    }
  };

  const getHealthColor = (status) => {
    switch (status) {
      case 'healthy': return 'text-green-600';
      case 'degraded': return 'text-yellow-600';
      case 'unhealthy': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getHealthBgColor = (status) => {
    switch (status) {
      case 'healthy': return 'bg-green-100';
      case 'degraded': return 'bg-yellow-100';
      case 'unhealthy': return 'bg-red-100';
      default: return 'bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="flex items-center space-x-2">
          <RefreshCw className="h-6 w-6 animate-spin" />
          <span>Loading agent dashboard...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Bot className="h-6 w-6 text-blue-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Agent Dashboard</h1>
            <p className="text-gray-600">Monitor and manage your AI scheduling assistant</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={refreshData}
            disabled={refreshing}
            className="btn-secondary"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <button
            onClick={() => exportData('history')}
            className="btn-secondary"
          >
            <Download className="h-4 w-4 mr-2" />
            Export History
          </button>
          <button
            onClick={() => exportData('metrics')}
            className="btn-secondary"
          >
            <Download className="h-4 w-4 mr-2" />
            Export Metrics
          </button>
        </div>
      </div>

      {/* Health Status */}
      {healthStatus && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="card">
            <div className="card-body">
              <div className="flex items-center">
                <div className={`p-3 rounded-lg ${getHealthBgColor(healthStatus.status)}`}>
                  <Bot className={`h-6 w-6 ${getHealthColor(healthStatus.status)}`} />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Agent Status</p>
                  <p className={`text-lg font-semibold ${getHealthColor(healthStatus.status)}`}>
                    {healthStatus.status}
                  </p>
                  <p className="text-xs text-gray-500">
                    Score: {healthStatus.health_score}/100
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-body">
              <div className="flex items-center">
                <div className="p-3 bg-blue-100 rounded-lg">
                  <Clock className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Uptime</p>
                  <p className="text-lg font-semibold text-blue-600">
                    {Math.floor(healthStatus.uptime.uptime_hours)}h {healthStatus.uptime.uptime_minutes}m
                  </p>
                  <p className="text-xs text-gray-500">
                    Started: {new Date(healthStatus.uptime.start_time).toLocaleDateString()}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-body">
              <div className="flex items-center">
                <div className="p-3 bg-green-100 rounded-lg">
                  <Activity className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Last Activity</p>
                  <p className="text-lg font-semibold text-green-600">
                    {Math.floor(healthStatus.last_activity.minutes_since_last)}m ago
                  </p>
                  <p className="text-xs text-gray-500">
                    {healthStatus.last_activity.is_active ? 'Active' : 'Inactive'}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="card-body">
              <div className="flex items-center">
                <div className="p-3 bg-purple-100 rounded-lg">
                  <BarChart3 className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Success Rate</p>
                  <p className="text-lg font-semibold text-purple-600">
                    {healthStatus.recent_performance.success_rate}%
                  </p>
                  <p className="text-xs text-gray-500">
                    {healthStatus.recent_performance.total_tasks} tasks
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Performance Metrics */}
      {performanceMetrics && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Performance Metrics (Last Hour)</h3>
          </div>
          <div className="card-body">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-600">{performanceMetrics.total_tasks}</p>
                <p className="text-sm text-gray-600">Total Tasks</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">{performanceMetrics.success_rate}%</p>
                <p className="text-sm text-gray-600">Success Rate</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-orange-600">{performanceMetrics.avg_processing_time}s</p>
                <p className="text-sm text-gray-600">Avg Processing Time</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-purple-600">{performanceMetrics.tasks_per_minute}</p>
                <p className="text-sm text-gray-600">Tasks/Minute</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Task Statistics */}
      {taskStatistics && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Task Statistics by Type</h3>
          </div>
          <div className="card-body">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Task Type
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Total
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Completed
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Failed
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Success Rate
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Avg Time
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {Object.entries(taskStatistics).map(([taskType, stats]) => (
                    <tr key={taskType}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {taskType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {stats.total}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600">
                        {stats.completed}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600">
                        {stats.failed}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {stats.success_rate}%
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {stats.avg_processing_time}s
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Active Tasks */}
      {activeTasks.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Active Tasks</h3>
          </div>
          <div className="card-body">
            <div className="space-y-3">
              {activeTasks.map((task) => (
                <div key={task.task_id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <Activity className="h-4 w-4 text-blue-600" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">{task.description}</p>
                      <p className="text-xs text-gray-500">
                        {task.task_type} • Started {new Date(task.created_at).toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded">
                      {task.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Recent Task History */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">Recent Task History</h3>
        </div>
        <div className="card-body">
          <div className="space-y-3">
            {taskHistory.map((task) => (
              <div key={task.task_id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${
                    task.status === 'completed' ? 'bg-green-100' : 
                    task.status === 'failed' ? 'bg-red-100' : 'bg-gray-100'
                  }`}>
                    {task.status === 'completed' ? (
                      <CheckCircle className="h-4 w-4 text-green-600" />
                    ) : task.status === 'failed' ? (
                      <XCircle className="h-4 w-4 text-red-600" />
                    ) : (
                      <AlertCircle className="h-4 w-4 text-gray-600" />
                    )}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{task.description}</p>
                    <p className="text-xs text-gray-500">
                      {task.task_type} • {task.processing_time}s • {new Date(task.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`text-xs px-2 py-1 rounded ${
                    task.status === 'completed' ? 'text-green-600 bg-green-100' : 
                    task.status === 'failed' ? 'text-red-600 bg-red-100' : 'text-gray-600 bg-gray-100'
                  }`}>
                    {task.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">Agent Actions</h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button
              onClick={resetMetrics}
              className="flex items-center justify-center space-x-2 p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <RefreshCw className="h-5 w-5 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">Reset Metrics</span>
            </button>
            <button
              onClick={clearHistory}
              className="flex items-center justify-center space-x-2 p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Trash2 className="h-5 w-5 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">Clear History</span>
            </button>
            <button
              onClick={() => window.location.reload()}
              className="flex items-center justify-center space-x-2 p-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <Play className="h-5 w-5 text-gray-600" />
              <span className="text-sm font-medium text-gray-700">Restart Agent</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentDashboard; 