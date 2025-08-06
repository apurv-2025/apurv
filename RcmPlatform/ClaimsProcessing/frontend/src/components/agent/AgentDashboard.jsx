import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  TrendingUp, 
  Users, 
  Zap,
  Wrench, // Changed from Tool to Wrench
  BarChart3,
  Target,
  Loader2
} from 'lucide-react';
import { agentService } from '../../services/agentService';

const AgentDashboard = () => {
  const [health, setHealth] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [realtime, setRealtime] = useState(null);
  const [toolUsage, setToolUsage] = useState(null);
  const [activeTasks, setActiveTasks] = useState([]);
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          healthData,
          performanceData,
          realtimeData,
          toolUsageData,
          toolsData,
          activeTasksData
        ] = await Promise.all([
          agentService.getAgentHealth(),
          agentService.getPerformanceMetrics(),
          agentService.getRealtimeMetrics(),
          agentService.getToolUsageMetrics(),
          agentService.getAvailableTools(),
          agentService.getActiveTasks()
        ]);

        setHealth(healthData);
        setPerformance(performanceData);
        setRealtime(realtimeData);
        setToolUsage(toolUsageData);
        setTools(toolsData.tools || []);
        setActiveTasks(activeTasksData.active_tasks || []);
      } catch (error) {
        console.error('Error fetching agent data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
      case 'optimal':
        return 'text-green-600 bg-green-100';
      case 'warning':
        return 'text-yellow-600 bg-yellow-100';
      case 'error':
      case 'critical':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
      case 'optimal':
        return <CheckCircle className="w-4 h-4" />;
      case 'warning':
        return <AlertCircle className="w-4 h-4" />;
      case 'error':
      case 'critical':
        return <AlertCircle className="w-4 h-4" />;
      default:
        return <Activity className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Health Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Agent Status</p>
              <p className="text-2xl font-bold text-gray-900">
                {health?.agent_available ? 'Online' : 'Offline'}
              </p>
            </div>
            <div className={`p-2 rounded-lg ${getStatusColor(health?.status)}`}>
              {getStatusIcon(health?.status)}
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Model Status</p>
              <p className="text-2xl font-bold text-gray-900">
                {health?.model_status || 'Connected'}
              </p>
            </div>
            <div className="p-2 rounded-lg bg-blue-100 text-blue-600">
              <Zap className="w-4 h-4" />
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Tasks</p>
              <p className="text-2xl font-bold text-gray-900">
                {activeTasks.length}
              </p>
            </div>
            <div className="p-2 rounded-lg bg-purple-100 text-purple-600">
              <Activity className="w-4 h-4" />
            </div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Available Tools</p>
              <p className="text-2xl font-bold text-gray-900">
                {health?.tools_available || tools.length}
              </p>
            </div>
            <div className="p-2 rounded-lg bg-green-100 text-green-600">
              <Wrench className="w-4 h-4" />
            </div>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Overview</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Total Requests</span>
              <span className="font-semibold">{performance?.total_requests?.toLocaleString() || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Success Rate</span>
              <span className="font-semibold text-green-600">
                {performance?.success_rate || 0}%
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Avg Response Time</span>
              <span className="font-semibold">{performance?.average_response_time || 0}s</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Error Rate</span>
              <span className="font-semibold text-red-600">
                {performance?.error_rate || 0}%
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Real-time Metrics</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Current Load</span>
              <span className="font-semibold">{realtime?.current_load || 0}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Active Sessions</span>
              <span className="font-semibold">{realtime?.active_sessions || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Requests/min</span>
              <span className="font-semibold">{realtime?.requests_per_minute || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Queue Time</span>
              <span className="font-semibold">{realtime?.average_queue_time || 0}s</span>
            </div>
          </div>
        </div>
      </div>

      {/* Tool Usage */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Tool Usage Analytics</h3>
        <div className="space-y-3">
          {toolUsage?.tool_usage?.map((tool, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Wrench className="w-4 h-4 text-blue-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900 capitalize">
                    {tool.tool.replace(/_/g, ' ')}
                  </p>
                  <p className="text-sm text-gray-600">
                    {tool.usage_count} uses
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-semibold text-gray-900">
                  {tool.success_rate}%
                </p>
                <p className="text-sm text-gray-600">Success Rate</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Available Tools */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Tools</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {tools.map((tool, index) => (
            <div key={index} className="p-4 border border-gray-200 rounded-lg">
              <div className="flex items-start space-x-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Target className="w-4 h-4 text-green-600" />
                </div>
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900 capitalize">
                    {tool.name.replace(/_/g, ' ')}
                  </h4>
                  <p className="text-sm text-gray-600 mt-1">
                    {tool.description}
                  </p>
                  {tool.parameters && tool.parameters.length > 0 && (
                    <div className="mt-2">
                      <p className="text-xs text-gray-500">Parameters:</p>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {tool.parameters.map((param, paramIndex) => (
                          <span
                            key={paramIndex}
                            className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded"
                          >
                            {param}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Active Tasks */}
      {activeTasks.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Active Tasks</h3>
          <div className="space-y-3">
            {activeTasks.map((task, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <Clock className="w-4 h-4 text-blue-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 capitalize">
                      {task.task_type.replace(/_/g, ' ')}
                    </p>
                    <p className="text-sm text-gray-600">
                      Started {new Date(task.created_at).toLocaleTimeString()}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="flex items-center space-x-2">
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${task.progress || 0}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-medium text-gray-900">
                      {task.progress || 0}%
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">
                    {task.status}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AgentDashboard;