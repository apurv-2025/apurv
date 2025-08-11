import React, { useState, useEffect } from 'react';
import { BarChart3, Shield, FileText, CheckCircle, AlertTriangle, TrendingUp, Activity, Clock, CheckCircle2, Zap } from 'lucide-react';

const AgentDashboard = () => {
  const [metrics, setMetrics] = useState({
    total_requests: 0,
    successful_requests: 0,
    failed_requests: 0,
    average_response_time: 0
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [toolUsage, setToolUsage] = useState([]);

  useEffect(() => {
    fetchMetrics();
    fetchRecentActivity();
    fetchToolUsage();
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await fetch('/api/v1/agent/metrics');
      const data = await response.json();
      setMetrics(data);
    } catch (error) {
      console.error('Failed to fetch metrics:', error);
    }
  };

  const fetchRecentActivity = async () => {
    try {
      const response = await fetch('/api/v1/agent/conversations/user-123?limit=5');
      const data = await response.json();
      setRecentActivity(data.conversations || []);
    } catch (error) {
      console.error('Failed to fetch recent activity:', error);
    }
  };

  const fetchToolUsage = async () => {
    try {
      const response = await fetch('/api/v1/agent/tools');
      const data = await response.json();
      setToolUsage(data);
    } catch (error) {
      console.error('Failed to fetch tool usage:', error);
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
              <p className="text-2xl font-bold text-green-600">{metrics.successful_requests}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <CheckCircle2 className="h-6 w-6 text-green-600" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-center text-sm text-gray-600">
              <TrendingUp className="h-4 w-4 mr-1" />
              <span>95% success rate</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Failed</p>
              <p className="text-2xl font-bold text-red-600">{metrics.failed_requests}</p>
            </div>
            <div className="p-3 bg-red-100 rounded-lg">
              <AlertTriangle className="h-6 w-6 text-red-600" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-center text-sm text-gray-600">
              <TrendingUp className="h-4 w-4 mr-1" />
              <span>5% failure rate</span>
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

      {/* Tool Usage Chart */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Tool Usage</h3>
        <div className="space-y-4">
          {metrics.most_used_tools?.map((tool, index) => (
            <div key={tool.name} className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className={`w-4 h-4 rounded-full ${getColorClasses(index)}`}></div>
                <span className="text-sm font-medium text-gray-700 capitalize">
                  {tool.name.replace('_', ' ')}
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full ${getColorClasses(index)}`}
                    style={{ width: `${(tool.count / Math.max(...metrics.most_used_tools.map(t => t.count))) * 100}%` }}
                  ></div>
                </div>
                <span className="text-sm text-gray-600 w-8">{tool.count}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-4">
          {recentActivity.map((conversation, index) => (
            <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <Activity className="h-4 w-4 text-blue-600" />
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">
                  Conversation {conversation.conversation_id}
                </p>
                <p className="text-sm text-gray-500">
                  {conversation.messages?.length || 0} messages
                </p>
                <p className="text-xs text-gray-400">
                  {new Date(conversation.created_at).toLocaleString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Available Tools */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Tools</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {toolUsage.map((tool, index) => (
            <div key={tool.name} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg">
              <div className={`p-2 rounded-lg ${getColorClasses(index).replace('bg-', 'bg-').replace('-500', '-100')}`}>
                {tool.name === 'verify_insurance' && <Shield className="h-5 w-5 text-blue-600" />}
                {tool.name === 'extract_insurance_info' && <FileText className="h-5 w-5 text-green-600" />}
                {tool.name === 'check_eligibility' && <CheckCircle className="h-5 w-5 text-purple-600" />}
                {tool.name === 'analyze_edi' && <AlertTriangle className="h-5 w-5 text-orange-600" />}
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-900 capitalize">
                  {tool.name.replace('_', ' ')}
                </h4>
                <p className="text-xs text-gray-500">{tool.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Performance Chart */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Overview</h3>
        <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
          <div className="text-center">
            <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-2" />
            <p className="text-sm text-gray-500">Performance chart will be displayed here</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentDashboard; 