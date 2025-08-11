import React, { useState, useEffect } from 'react';
import { Shield, MessageSquare, FileText, CheckCircle, AlertCircle, Activity, Settings, Bot, User, Code } from 'lucide-react';
import AgentChat from '../components/agent/AgentChat';
import AgentDashboard from '../components/agent/AgentDashboard';
import AgentTools from '../components/agent/AgentTools';
import axios from 'axios';

const AIAssistantPage = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [agentStatus, setAgentStatus] = useState('loading');

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

  useEffect(() => {
    // Check agent health on component mount
    checkAgentHealth();
  }, []);

  const checkAgentHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/agent/health`);
      setAgentStatus(response.data.status);
    } catch (error) {
      setAgentStatus('unhealthy');
    }
  };

  const tabs = [
    { id: 'chat', label: 'AI Assistant', icon: MessageSquare },
    { id: 'tools', label: 'AI Tools', icon: Settings },
    { id: 'dashboard', label: 'Analytics', icon: Activity }
  ];

  const features = [
    {
      icon: Shield,
      title: 'Prior Authorization',
      description: 'AI-powered prior authorization request creation and management',
      color: 'text-blue-600'
    },
    {
      icon: FileText,
      title: 'EDI Generation',
      description: 'Generate EDI 278/275 documents for authorization requests',
      color: 'text-green-600'
    },
    {
      icon: CheckCircle,
      title: 'Status Tracking',
      description: 'Real-time authorization status monitoring and updates',
      color: 'text-purple-600'
    },
    {
      icon: User,
      title: 'Patient Lookup',
      description: 'Intelligent patient information retrieval and management',
      color: 'text-orange-600'
    },
    {
      icon: Code,
      title: 'Code Lookup',
      description: 'Find healthcare codes (CPT, ICD-10, service types)',
      color: 'text-indigo-600'
    }
  ];

  const quickActions = [
    {
      title: 'Create Auth',
      description: 'Create authorization request',
      action: () => setActiveTab('tools'),
      icon: Shield,
      color: 'bg-blue-500 hover:bg-blue-600'
    },
    {
      title: 'Check Status',
      description: 'Check authorization status',
      action: () => setActiveTab('tools'),
      icon: CheckCircle,
      color: 'bg-green-500 hover:bg-green-600'
    },
    {
      title: 'Generate EDI',
      description: 'Generate EDI documents',
      action: () => setActiveTab('tools'),
      icon: FileText,
      color: 'bg-purple-500 hover:bg-purple-600'
    },
    {
      title: 'Lookup Patient',
      description: 'Find patient information',
      action: () => setActiveTab('tools'),
      icon: User,
      color: 'bg-orange-500 hover:bg-orange-600'
    },
    {
      title: 'Find Codes',
      description: 'Search healthcare codes',
      action: () => setActiveTab('tools'),
      icon: Code,
      color: 'bg-indigo-500 hover:bg-indigo-600'
    }
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'chat':
        return <AgentChat />;
      case 'tools':
        return <AgentTools />;
      case 'dashboard':
        return <AgentDashboard />;
      default:
        return <AgentChat />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <Bot className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-xl font-semibold text-gray-900">AI Prior Authorization Assistant</h1>
                <p className="text-sm text-gray-500">Powered by Agentic Core</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
                agentStatus === 'healthy' 
                  ? 'bg-green-100 text-green-800' 
                  : agentStatus === 'degraded'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                <div className={`w-2 h-2 rounded-full ${
                  agentStatus === 'healthy' ? 'bg-green-500' : agentStatus === 'degraded' ? 'bg-yellow-500' : 'bg-red-500'
                }`} />
                <span>{agentStatus === 'healthy' ? 'Online' : agentStatus === 'degraded' ? 'Degraded' : 'Offline'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'chat' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Features Overview */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Features</h2>
                <div className="space-y-4">
                  {features.map((feature, index) => {
                    const Icon = feature.icon;
                    return (
                      <div key={index} className="flex items-start space-x-3">
                        <Icon className={`h-5 w-5 mt-0.5 ${feature.color}`} />
                        <div>
                          <h3 className="text-sm font-medium text-gray-900">{feature.title}</h3>
                          <p className="text-xs text-gray-500">{feature.description}</p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="bg-white rounded-lg shadow-sm border p-6 mt-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
                <div className="grid grid-cols-2 gap-3">
                  {quickActions.map((action, index) => {
                    const Icon = action.icon;
                    return (
                      <button
                        key={index}
                        onClick={action.action}
                        className={`${action.color} text-white p-3 rounded-lg text-center transition-colors`}
                      >
                        <Icon className="h-5 w-5 mx-auto mb-1" />
                        <div className="text-xs font-medium">{action.title}</div>
                        <div className="text-xs opacity-90">{action.description}</div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* AI Status */}
              <div className="bg-white rounded-lg shadow-sm border p-6 mt-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Status</h2>
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                  agentStatus === 'healthy' 
                    ? 'bg-green-100 text-green-800' 
                    : agentStatus === 'degraded'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  <div className={`w-2 h-2 rounded-full mr-2 ${
                    agentStatus === 'healthy' ? 'bg-green-500' : agentStatus === 'degraded' ? 'bg-yellow-500' : 'bg-red-500'
                  }`} />
                  <span>{agentStatus === 'healthy' ? 'AI Assistant Online' : agentStatus === 'degraded' ? 'AI Assistant Degraded' : 'AI Assistant Offline'}</span>
                </div>
                <p className="text-sm text-gray-500 mt-2">
                  {agentStatus === 'healthy' 
                    ? 'All AI features are available and working properly.'
                    : agentStatus === 'degraded'
                    ? 'Some AI features may be limited. Please try again later.'
                    : 'AI features are currently unavailable. Please check back later.'
                  }
                </p>
              </div>
            </div>

            {/* Chat Interface */}
            <div className="lg:col-span-2">
              {renderContent()}
            </div>
          </div>
        )}

        {activeTab !== 'chat' && (
          <div className="w-full">
            {renderContent()}
          </div>
        )}
      </div>
    </div>
  );
};

export default AIAssistantPage; 