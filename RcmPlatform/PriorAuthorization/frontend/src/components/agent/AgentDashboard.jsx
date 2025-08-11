import React, { useState, useEffect } from 'react';
import { BarChart3, Shield, FileText, CheckCircle, AlertTriangle, TrendingUp, Activity, Clock, CheckCircle2, Zap, User, Code } from 'lucide-react';
import axios from 'axios';

const AgentDashboard = () => {
  const [metrics, setMetrics] = useState({
    total_requests: 0,
    successful_requests: 0,
    failed_requests: 0,
    average_response_time: 0
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [toolUsage, setToolUsage] = useState([]);
  const [aiHealth, setAiHealth] = useState(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

  useEffect(() => {
    fetchMetrics();
    fetchRecentActivity();
    fetchToolUsage();
    checkAIHealth();
  }, []);

  const fetchMetrics = async () => {
    try {
      // Mock metrics for now - in real implementation, this would come from the API
      setMetrics({
        total_requests: 156,
        successful_requests: 142,
        failed_requests: 14,
        average_response_time: 2.3
      });
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    }
  };

  const fetchRecentActivity = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/agent/conversations/test_user?limit=5`);
      setRecentActivity(response.data.conversations || []);
    } catch (error) {
      console.error('Failed to fetch recent activity:', error);
      // Mock data for demonstration
      setRecentActivity([
        {
          id: 'conv_1',
          user_id: 'test_user',
          messages: [
            { role: 'user', content: 'Create a prior authorization request', timestamp: '2024-01-15T10:30:00Z' },
            { role: 'assistant', content: 'I\'ll help you create a prior authorization request...', timestamp: '2024-01-15T10:30:05Z' }
          ],
          created_at: '2024-01-15T10:30:00Z',
          updated_at: '2024-01-15T10:30:05Z'
        },
        {
          id: 'conv_2',
          user_id: 'test_user',
          messages: [
            { role: 'user', content: 'Check authorization status', timestamp: '2024-01-15T09:15:00Z' },
            { role: 'assistant', content: 'Let me check the status of your authorization request...', timestamp: '2024-01-15T09:15:03Z' }
          ],
          created_at: '2024-01-15T09:15:00Z',
          updated_at: '2024-01-15T09:15:03Z'
        }
      ]);
    }
  };

  const fetchToolUsage = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/agent/tools`);
      setToolUsage(response.data.tools || []);
    } catch (error) {
      console.error('Failed to fetch tool usage:', error);
      // Mock data for demonstration
      setToolUsage([
        { name: 'create_prior_authorization', usage_count: 45 },
        { name: 'check_authorization_status', usage_count: 38 },
        { name: 'generate_edi', usage_count: 32 },
        { name: 'lookup_patient', usage_count: 28 },
        { name: 'lookup_codes', usage_count: 13 }
      ]);
    }
  };

  const checkAIHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/agent/health`);
      setAiHealth(response.data);
    } catch (error) {
      console.error('Failed to check AI health:', error);
      setAiHealth({ status: 'unhealthy', error: error.message });
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'success': return 'text-green-600';
      case 'error': return 'text-red-600';
      case 'pending': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success': return CheckCircle2;
      case 'error': return AlertTriangle;
      case 'pending': return Clock;
      default: return Activity;
    }
  };

  const getColorClasses = (index) => {
    const colors = [
      'bg-blue-500',
      'bg-green-500',
      'bg-purple-500',
      'bg-orange-500',
      'bg-red-500',
      'bg-indigo-500'
    ];
    return colors[index % colors.length];
  };

  const getToolIcon = (toolName) => {
    if (toolName.includes('create')) return Shield;
    if (toolName.includes('status')) return CheckCircle;
    if (toolName.includes('edi')) return FileText;
    if (toolName.includes('patient')) return User;
    if (toolName.includes('codes')) return Code;
    return Activity;
  };

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Requests</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.total_requests}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <Activity className="h-6 w-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-center text-sm text-gray-600">
              <TrendingUp className="h-4 w-4 mr-1" />
              <span>+12% from last week</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Successful</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.successful_requests}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <CheckCircle2 className="h-6 w-6 text-green-600" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-center text-sm text-gray-600">
              <div className="w-full bg-gray-200 rounded-full h-2 mr-2">
                <div 
                  className="bg-green-600 h-2 rounded-full" 
                  style={{ width: `${(metrics.successful_requests / metrics.total_requests) * 100}%` }}
                ></div>
              </div>
              <span>{Math.round((metrics.successful_requests / metrics.total_requests) * 100)}%</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Failed</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.failed_requests}</p>
            </div>
            <div className="p-3 bg-red-100 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-red-600" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-center text-sm text-gray-600">
              <div className="w-full bg-gray-200 rounded-full h-2 mr-2">
                <div 
                  className="bg-red-600 h-2 rounded-full" 
                  style={{ width: `${(metrics.failed_requests / metrics.total_requests) * 100}%` }}
                ></div>
              </div>
              <span>{Math.round((metrics.failed_requests / metrics.total_requests) * 100)}%</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg Response Time</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.average_response_time}s</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <Zap className="h-6 w-6 text-purple-600" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-center text-sm text-gray-600">
              <TrendingUp className="h-4 w-4 mr-1" />
              <span>-8% from last week</span>
            </div>
          </div>
        </div>
      </div>

      {/* AI Health Status */}
      {aiHealth && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Assistant Status</h2>
          <div className={`inline-flex items-center px-4 py-2 rounded-full text-sm font-medium ${
            aiHealth.status === 'healthy' 
              ? 'bg-green-100 text-green-800' 
              : aiHealth.status === 'degraded'
              ? 'bg-yellow-100 text-yellow-800'
              : 'bg-red-100 text-red-800'
          }`}>
            <div className={`w-2 h-2 rounded-full mr-2 ${
              aiHealth.status === 'healthy' ? 'bg-green-500' : aiHealth.status === 'degraded' ? 'bg-yellow-500' : 'bg-red-500'
            }`} />
            <span>Status: {aiHealth.status}</span>
            {aiHealth.error && <span className="ml-2">- {aiHealth.error}</span>}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Tool Usage */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Tool Usage</h2>
          <div className="space-y-4">
            {toolUsage.map((tool, index) => {
              const Icon = getToolIcon(tool.name);
              return (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${getColorClasses(index)}`}>
                      <Icon className="h-4 w-4 text-white" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {tool.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </p>
                      <p className="text-xs text-gray-500">{tool.usage_count} uses</p>
                    </div>
                  </div>
                  <div className="w-24 bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full ${getColorClasses(index)}`}
                      style={{ width: `${(tool.usage_count / Math.max(...toolUsage.map(t => t.usage_count))) * 100}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            {recentActivity.map((conversation, index) => (
              <div key={index} className="border-l-4 border-blue-500 pl-4">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-medium text-gray-900">
                    Conversation {conversation.id}
                  </p>
                  <span className="text-xs text-gray-500">
                    {new Date(conversation.updated_at).toLocaleTimeString()}
                  </span>
                </div>
                <p className="text-sm text-gray-600">
                  {conversation.messages?.[0]?.content || 'No messages'}
                </p>
                <div className="mt-2 flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-xs text-gray-500">Completed</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Performance Chart */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Performance Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600 mb-2">91%</div>
            <div className="text-sm text-gray-600">Success Rate</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600 mb-2">2.3s</div>
            <div className="text-sm text-gray-600">Average Response</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600 mb-2">156</div>
            <div className="text-sm text-gray-600">Total Requests</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentDashboard; 