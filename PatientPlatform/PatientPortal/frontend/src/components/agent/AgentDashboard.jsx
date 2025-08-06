import React, { useState, useEffect } from 'react';
import { BarChart3, Heart, Calendar, Pill, FileText, User, Bell, TrendingUp, Activity, Clock, CheckCircle, AlertCircle, Zap } from 'lucide-react';

const AgentDashboard = () => {
  const [metrics, setMetrics] = useState({
    totalPatients: 1250,
    activePatients: 980,
    appointmentsToday: 15,
    engagementRate: 78.5,
    aiInteractions: 342,
    averageResponseTime: 1.2,
    successRate: 95.2
  });

  const [healthInsights, setHealthInsights] = useState([
    {
      id: 1,
      type: 'medication',
      title: 'Medication Reminders',
      description: '2 medications due today',
      status: 'warning',
      icon: Pill,
      color: 'purple'
    },
    {
      id: 2,
      type: 'appointment',
      title: 'Upcoming Appointments',
      description: 'Annual physical in 3 days',
      status: 'info',
      icon: Calendar,
      color: 'blue'
    },
    {
      id: 3,
      type: 'lab',
      title: 'Recent Lab Results',
      description: 'All values within normal range',
      status: 'success',
      icon: FileText,
      color: 'green'
    }
  ]);

  const [recentActivity, setRecentActivity] = useState([
    {
      id: 1,
      action: 'Appointment scheduled',
      details: 'Annual physical with Dr. Smith',
      timestamp: '2 hours ago',
      status: 'completed'
    },
    {
      id: 2,
      action: 'Medication refill requested',
      details: 'Lisinopril 10mg',
      timestamp: '4 hours ago',
      status: 'pending'
    },
    {
      id: 3,
      action: 'Lab results reviewed',
      details: 'Complete Blood Count analysis',
      timestamp: '1 day ago',
      status: 'completed'
    },
    {
      id: 4,
      action: 'Health summary generated',
      details: 'Comprehensive wellness report',
      timestamp: '2 days ago',
      status: 'completed'
    }
  ]);

  const [aiPerformance, setAiPerformance] = useState({
    totalConversations: 156,
    averageResponseTime: 1.2,
    successRate: 95.2,
    popularQueries: [
      'Schedule appointment',
      'Check medications',
      'View lab results',
      'Find doctor'
    ],
    toolUsage: [
      { name: 'Appointment Scheduling', usage: 45 },
      { name: 'Medication Check', usage: 30 },
      { name: 'Lab Results', usage: 15 },
      { name: 'Doctor Finder', usage: 10 }
    ]
  });

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setMetrics(prev => ({
        ...prev,
        aiInteractions: prev.aiInteractions + Math.floor(Math.random() * 3),
        appointmentsToday: prev.appointmentsToday + Math.floor(Math.random() * 2) - 1
      }));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status) => {
    const colors = {
      success: 'text-green-600 bg-green-100',
      warning: 'text-yellow-600 bg-yellow-100',
      error: 'text-red-600 bg-red-100',
      info: 'text-blue-600 bg-blue-100',
      pending: 'text-gray-600 bg-gray-100'
    };
    return colors[status] || colors.info;
  };

  const getStatusIcon = (status) => {
    const icons = {
      success: CheckCircle,
      warning: AlertCircle,
      error: AlertCircle,
      info: Clock,
      pending: Clock
    };
    return icons[status] || Clock;
  };

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-100 text-blue-600',
      purple: 'bg-purple-100 text-purple-600',
      green: 'bg-green-100 text-green-600',
      orange: 'bg-orange-100 text-orange-600',
      red: 'bg-red-100 text-red-600',
      yellow: 'bg-yellow-100 text-yellow-600'
    };
    return colors[color] || colors.blue;
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Health Dashboard</h2>
          <p className="text-gray-600">Your health metrics and AI insights</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-500">Live updates</span>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Patients</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.totalPatients.toLocaleString()}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <User className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
            <span className="text-green-600">+12% from last month</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Appointments Today</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.appointmentsToday}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <Calendar className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <Activity className="w-4 h-4 text-blue-500 mr-1" />
            <span className="text-blue-600">3 pending confirmations</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">AI Interactions</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.aiInteractions}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <Zap className="w-6 h-6 text-purple-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
            <span className="text-green-600">+8% this week</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Success Rate</p>
              <p className="text-2xl font-bold text-gray-900">{metrics.successRate}%</p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <Clock className="w-4 h-4 text-gray-500 mr-1" />
            <span className="text-gray-600">Avg response: {metrics.averageResponseTime}s</span>
          </div>
        </div>
      </div>

      {/* Health Insights */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Today's Health Insights</h3>
          <p className="text-sm text-gray-600">AI-powered recommendations and alerts</p>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {healthInsights.map((insight) => {
              const Icon = insight.icon;
              const StatusIcon = getStatusIcon(insight.status);
              return (
                <div key={insight.id} className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex items-center justify-between mb-3">
                    <div className={`p-2 rounded-lg ${getColorClasses(insight.color)}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(insight.status)}`}>
                      <StatusIcon className="w-3 h-3 inline mr-1" />
                      {insight.status}
                    </div>
                  </div>
                  <h4 className="font-medium text-gray-900 mb-1">{insight.title}</h4>
                  <p className="text-sm text-gray-600">{insight.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* AI Performance */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-sm border">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">AI Performance</h3>
            <p className="text-sm text-gray-600">Conversation and response metrics</p>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Total Conversations</span>
              <span className="font-medium">{aiPerformance.totalConversations}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Average Response Time</span>
              <span className="font-medium">{aiPerformance.averageResponseTime}s</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-600">Success Rate</span>
              <span className="font-medium">{aiPerformance.successRate}%</span>
            </div>
            <div className="pt-4 border-t border-gray-200">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Popular Queries</h4>
              <div className="space-y-1">
                {aiPerformance.popularQueries.map((query, index) => (
                  <div key={index} className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">{query}</span>
                    <span className="text-gray-400">#{index + 1}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm border">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Tool Usage</h3>
            <p className="text-sm text-gray-600">Most used AI features</p>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {aiPerformance.toolUsage.map((tool, index) => (
                <div key={index}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-gray-600">{tool.name}</span>
                    <span className="text-sm font-medium">{tool.usage}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-green-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${tool.usage}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
          <p className="text-sm text-gray-600">Latest actions and updates</p>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {recentActivity.map((activity) => {
              const StatusIcon = getStatusIcon(activity.status);
              return (
                <div key={activity.id} className="flex items-center space-x-4">
                  <div className={`p-2 rounded-lg ${getStatusColor(activity.status)}`}>
                    <StatusIcon className="w-4 h-4" />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{activity.action}</p>
                    <p className="text-sm text-gray-600">{activity.details}</p>
                  </div>
                  <span className="text-sm text-gray-500">{activity.timestamp}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AgentDashboard; 