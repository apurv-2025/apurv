import React, { useState, useEffect } from 'react';
import { Shield, MessageSquare, FileText, CheckCircle, AlertCircle, Activity, Settings, Bot } from 'lucide-react';
import AgentChat from '../components/agent/AgentChat';
import AgentDashboard from '../components/agent/AgentDashboard';
import AgentTools from '../components/agent/AgentTools';

const AgentPage = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [agentStatus, setAgentStatus] = useState('loading');

  useEffect(() => {
    // Check agent health on component mount
    checkAgentHealth();
  }, []);

  const checkAgentHealth = async () => {
    try {
      const response = await fetch('/api/v1/agent/health');
      const data = await response.json();
      setAgentStatus(data.status);
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
      title: 'Insurance Verification',
      description: 'AI-powered insurance coverage verification with real-time eligibility checks',
      color: 'text-blue-600'
    },
    {
      icon: FileText,
      title: 'Document Analysis',
      description: 'Extract insurance information from uploaded cards and documents',
      color: 'text-green-600'
    },
    {
      icon: CheckCircle,
      title: 'Eligibility Checks',
      description: 'Comprehensive eligibility verification for multiple service types',
      color: 'text-purple-600'
    },
    {
      icon: AlertCircle,
      title: 'EDI Analysis',
      description: 'Advanced EDI 270/271 transaction analysis and validation',
      color: 'text-orange-600'
    }
  ];

  const quickActions = [
    {
      title: 'Verify Insurance',
      description: 'Check coverage and eligibility',
      action: () => setActiveTab('tools'),
      icon: Shield,
      color: 'bg-blue-500 hover:bg-blue-600'
    },
    {
      title: 'Extract Info',
      description: 'Extract from documents',
      action: () => setActiveTab('tools'),
      icon: FileText,
      color: 'bg-green-500 hover:bg-green-600'
    },
    {
      title: 'Check Eligibility',
      description: 'Verify patient eligibility',
      action: () => setActiveTab('tools'),
      icon: CheckCircle,
      color: 'bg-purple-500 hover:bg-purple-600'
    },
    {
      title: 'Analyze EDI',
      description: 'Process EDI transactions',
      action: () => setActiveTab('tools'),
      icon: AlertCircle,
      color: 'bg-orange-500 hover:bg-orange-600'
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
                <h1 className="text-xl font-semibold text-gray-900">AI Insurance Assistant</h1>
                <p className="text-sm text-gray-500">Powered by Agentic Core</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
                agentStatus === 'healthy' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                <div className={`w-2 h-2 rounded-full ${
                  agentStatus === 'healthy' ? 'bg-green-500' : 'bg-red-500'
                }`} />
                <span>{agentStatus === 'healthy' ? 'Online' : 'Offline'}</span>
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

export default AgentPage; 