import React, { useState } from 'react';
import { MessageSquare, BarChart3, Settings, Bot, Sparkles, Zap, Shield, Globe } from 'lucide-react';
import AgentChat from '../components/agent/AgentChat';
import EnhancedAgentChat from '../components/agent/EnhancedAgentChat';
import AgentDashboard from '../components/agent/AgentDashboard';

const Agent = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [useEnhancedChat, setUseEnhancedChat] = useState(true);

  const tabs = [
    {
      id: 'chat',
      label: 'AI Assistant',
      icon: MessageSquare,
      description: 'Chat with the AI agent'
    },
    {
      id: 'dashboard',
      label: 'Agent Dashboard',
      icon: BarChart3,
      description: 'View metrics and performance'
    }
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'chat':
        return useEnhancedChat ? <EnhancedAgentChat /> : <AgentChat />;
      case 'dashboard':
        return <AgentDashboard />;
      default:
        return useEnhancedChat ? <EnhancedAgentChat /> : <AgentChat />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">AI Claims Assistant</h1>
              <p className="text-gray-600">
                Intelligent automation for claims processing and analysis
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">AI Agent Online</span>
            </div>
            <div className="flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-blue-600" />
              <span className="text-sm text-gray-600">Enhanced Mode</span>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-4 h-4 mr-2" />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="h-[600px]">
          {renderContent()}
        </div>
      </div>

      {/* Features Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-blue-100 rounded-lg">
              <MessageSquare className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Natural Language</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Chat naturally with the AI assistant about claims, rejections, reports, and more.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-green-100 rounded-lg">
              <BarChart3 className="w-5 h-5 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Smart Analytics</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Get intelligent insights and automated analysis of your claims data.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Zap className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Automated Tasks</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Automate claim validation, rejection analysis, and report generation.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Shield className="w-5 h-5 text-orange-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Secure & Reliable</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Enterprise-grade security with real-time monitoring and backup systems.
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <button
            onClick={() => setActiveTab('chat')}
            className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left"
          >
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <MessageSquare className="w-4 h-4 text-blue-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">Start Chat</p>
                <p className="text-sm text-gray-600">Ask questions about claims</p>
              </div>
            </div>
          </button>

          <button
            onClick={() => {
              setActiveTab('chat');
              // This would trigger a specific action in the chat
            }}
            className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left"
          >
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <BarChart3 className="w-4 h-4 text-green-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">Generate Report</p>
                <p className="text-sm text-gray-600">Create financial summary</p>
              </div>
            </div>
          </button>

          <button
            onClick={() => {
              setActiveTab('chat');
              // This would trigger a specific action in the chat
            }}
            className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left"
          >
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <Settings className="w-4 h-4 text-yellow-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">Analyze Claims</p>
                <p className="text-sm text-gray-600">Check for issues</p>
              </div>
            </div>
          </button>

          <button
            onClick={() => {
              setActiveTab('chat');
              // This would trigger a specific action in the chat
            }}
            className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors text-left"
          >
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-red-100 rounded-lg">
                <MessageSquare className="w-4 h-4 text-red-600" />
              </div>
              <div>
                <p className="font-medium text-gray-900">Process Rejections</p>
                <p className="text-sm text-gray-600">Fix rejected claims</p>
              </div>
            </div>
          </button>
        </div>
      </div>

      {/* Help Section */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
        <div className="flex items-start space-x-4">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Bot className="w-5 h-5 text-blue-600" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 mb-2">How to use the AI Assistant</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
              <div>
                <p className="font-medium text-gray-900 mb-1">💬 Natural Conversations</p>
                <p>Ask questions in plain English about your claims, rejections, or reports.</p>
              </div>
              <div>
                <p className="font-medium text-gray-900 mb-1">📊 Smart Analysis</p>
                <p>Get automated insights and recommendations for claim processing.</p>
              </div>
              <div>
                <p className="font-medium text-gray-900 mb-1">⚡ Quick Actions</p>
                <p>Use the quick action buttons to perform common tasks instantly.</p>
              </div>
              <div>
                <p className="font-medium text-gray-900 mb-1">📈 Real-time Metrics</p>
                <p>Monitor agent performance and system health in the dashboard.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Features */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border border-purple-200">
        <div className="flex items-start space-x-4">
          <div className="p-2 bg-purple-100 rounded-lg">
            <Sparkles className="w-5 h-5 text-purple-600" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 mb-2">Enhanced Features</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
              <div>
                <p className="font-medium text-gray-900 mb-1">🔄 Conversation History</p>
                <p>Access and search through your previous conversations with the AI.</p>
              </div>
              <div>
                <p className="font-medium text-gray-900 mb-1">⚙️ Model Selection</p>
                <p>Choose between different AI models for optimal performance.</p>
              </div>
              <div>
                <p className="font-medium text-gray-900 mb-1">📤 Export & Share</p>
                <p>Export conversations and share insights with your team.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Agent; 