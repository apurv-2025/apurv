import React, { useState } from 'react';
import { MessageSquare, BarChart3, Settings, Bot, Sparkles, Zap, Shield, Globe, Heart, Calendar, Pill, FileText, User, Bell } from 'lucide-react';
import AgentChat from './agent/AgentChat';
import EnhancedAgentChat from './agent/EnhancedAgentChat';
import AgentDashboard from './agent/AgentDashboard';

const Agent = () => {
  const [activeTab, setActiveTab] = useState('chat');
  const [useEnhancedChat, setUseEnhancedChat] = useState(true);

  const tabs = [
    {
      id: 'chat',
      label: 'AI Health Assistant',
      icon: MessageSquare,
      description: 'Chat with your AI health assistant'
    },
    {
      id: 'dashboard',
      label: 'Health Dashboard',
      icon: BarChart3,
      description: 'View your health metrics and insights'
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
            <div className="p-3 bg-gradient-to-r from-green-500 to-blue-600 rounded-lg">
              <Heart className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">AI Health Assistant</h1>
              <p className="text-gray-600">
                Your intelligent health companion for appointments, medications, and more
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">AI Assistant Online</span>
            </div>
            <div className="flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-green-600" />
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
                      ? 'border-green-500 text-green-600'
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
              <Calendar className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Appointment Scheduling</h3>
          </div>
          <p className="text-gray-600 text-sm">
            AI-powered appointment booking with smart recommendations and availability checking.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Pill className="w-5 h-5 text-purple-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Medication Management</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Track medications, check refills, and set up smart reminders for your health routine.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-green-100 rounded-lg">
              <FileText className="w-5 h-5 text-green-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Lab Results Analysis</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Get AI-powered explanations of your lab results with personalized insights and recommendations.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center space-x-3 mb-4">
            <div className="p-2 bg-orange-100 rounded-lg">
              <User className="w-5 h-5 text-orange-600" />
            </div>
            <h3 className="font-semibold text-gray-900">Doctor Finder</h3>
          </div>
          <p className="text-gray-600 text-sm">
            Find and book appointments with specialists based on your needs and preferences.
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <Calendar className="w-5 h-5 text-blue-600 mr-2" />
            <span className="text-sm font-medium">Schedule Visit</span>
          </button>
          <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <Pill className="w-5 h-5 text-purple-600 mr-2" />
            <span className="text-sm font-medium">Check Meds</span>
          </button>
          <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <FileText className="w-5 h-5 text-green-600 mr-2" />
            <span className="text-sm font-medium">View Results</span>
          </button>
          <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <Bell className="w-5 h-5 text-orange-600 mr-2" />
            <span className="text-sm font-medium">Set Reminders</span>
          </button>
        </div>
      </div>

      {/* Health Insights */}
      <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border border-green-200">
        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2 bg-green-100 rounded-lg">
            <Heart className="w-5 h-5 text-green-600" />
          </div>
          <h2 className="text-lg font-semibold text-gray-900">Today's Health Insights</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <h3 className="font-medium text-gray-900 mb-2">Medication Reminders</h3>
            <p className="text-sm text-gray-600">2 medications due today</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <h3 className="font-medium text-gray-900 mb-2">Upcoming Appointments</h3>
            <p className="text-sm text-gray-600">Annual physical in 3 days</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm">
            <h3 className="font-medium text-gray-900 mb-2">Recent Lab Results</h3>
            <p className="text-sm text-gray-600">All values within normal range</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Agent; 