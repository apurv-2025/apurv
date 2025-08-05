import React, { useState, useEffect } from 'react';
import { Plus, Bot } from 'lucide-react';
import { api } from '../services/api';
import AgentCard from '../components/agent/AgentCard';
import AgentModal from '../components/agent/AgentModal';
import ChatModal from '../components/agent/ChatModal';

const AgentManagement = () => {
  const [agents, setAgents] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [showChatModal, setShowChatModal] = useState(false);
  const [chatAgent, setChatAgent] = useState(null);
  const [activeTab, setActiveTab] = useState('build'); 

  useEffect(() => {
    loadAgents();
  }, []);
  
  const loadAgents = async () => {
    try {
      const agentData = await api.getAgents();
      setAgents(agentData);
    } catch (error) {
      console.error('Error loading agents:', error);
    }
  };

  const handleCreateAgent = () => {
    setSelectedAgent(null);
    setShowModal(true);
  };
  const handleBuildAgent = () => {
    setSelectedAgent(null);
    setShowModal(true);
  };
  const handleConfigureAgent = () => {
    setSelectedAgent(null);
    setShowModal(true);
  };
  const handleDeployAgent = () => {
    setSelectedAgent(null);
    setShowModal(true);
  };
  const handleMonitorAgent = () => {
    setSelectedAgent(null);
    setShowModal(true);
  };
  const handleEditAgent = (agent) => {
    setSelectedAgent(agent);
    setShowModal(true);
  };

  const handleDeleteAgent = async (agentId) => {
    if (window.confirm('Are you sure you want to delete this agent?')) {
      try {
        await api.deleteAgent(agentId);
        await loadAgents();
      } catch (error) {
        console.error('Error deleting agent:', error);
      }
    }
  };

  const handleTestAgent = (agent) => {
    setChatAgent(agent);
    setShowChatModal(true);
  };

  // Function to render content based on active tab
  const renderTabContent = () => {
    switch (activeTab) {
      case 'build':
        return (
          <div className="p-8">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Agents</h1>
                <p className="text-gray-600">Create and manage your AI agents</p>
              </div>
              <button
                onClick={handleCreateAgent}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2 transition duration-200"
              >
                <Plus className="w-5 h-5" />
                <span>Create Agent</span>
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {agents.map((agent) => (
                <AgentCard
                  key={agent.id}
                  agent={agent}
                  onBuild={handleBuildAgent}
                  onConfigure={handleConfigureAgent}
                  onTest={handleTestAgent}
                  onDeploy={handleDeployAgent}
                  onMonitor={handleMonitorAgent}
                  onDelete={handleDeleteAgent}
                />
              ))}

              {agents.length === 0 && (
                <div className="col-span-full text-center py-12">
                  <Bot className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No agents yet</h3>
                  <p className="text-gray-500 mb-6">Create your first AI agent to get started</p>
                  <button
                    onClick={handleCreateAgent}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 flex items-center space-x-2 mx-auto transition duration-200"
                  >
                    <Plus className="w-5 h-5" />
                    <span>Create Your First Agent</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        );
      
      case 'dashboard':
        return (
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600">Overview of your AI agents and performance metrics</p>
            {/* Add dashboard content here */}
            <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Agents</h3>
                <p className="text-3xl font-bold text-blue-600">{agents.length}</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Active Agents</h3>
                <p className="text-3xl font-bold text-green-600">{agents.filter(a => a.status === 'active').length}</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Total Conversations</h3>
                <p className="text-3xl font-bold text-purple-600">-</p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Success Rate</h3>
                <p className="text-3xl font-bold text-orange-600">-</p>
              </div>
            </div>
          </div>
        );
      
      case 'knowledge':
        return (
          <div className="p-8">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Knowledge Base</h1>
                <p className="text-gray-600">Manage knowledge sources for your AI agents</p>
              </div>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2 transition duration-200">
                <Plus className="w-5 h-5" />
                <span>Add Knowledge Source</span>
              </button>
            </div>
            {/* Add knowledge base content here */}
          </div>
        );
      
      case 'templates':
        return (
          <div className="p-8">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Templates</h1>
                <p className="text-gray-600">Pre-built agent templates to get started quickly</p>
              </div>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center space-x-2 transition duration-200">
                <Plus className="w-5 h-5" />
                <span>Create Template</span>
              </button>
            </div>
            {/* Add templates content here */}
          </div>
        );
      
      case 'test':
        return (
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Test</h1>
            <p className="text-gray-600">Test your AI agents before deployment</p>
            {/* Add testing content here */}
          </div>
        );
      
      case 'deploy':
        return (
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Deploy</h1>
            <p className="text-gray-600">Deploy your AI agents to production</p>
            {/* Add deployment content here */}
          </div>
        );
      
      case 'monitor':
        return (
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Monitor</h1>
            <p className="text-gray-600">Monitor performance and usage of deployed agents</p>
            {/* Add monitoring content here */}
          </div>
        );
      
      case 'decommision':
        return (
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Decommission</h1>
            <p className="text-gray-600">Safely decommission agents that are no longer needed</p>
            {/* Add decommission content here */}
          </div>
        );
      
      case 'settings':
        return (
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Settings</h1>
            <p className="text-gray-600">Configure your AI agent studio settings</p>
            {/* Add settings content here */}
          </div>
        );
      
      default:
        return (
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Page Not Found</h1>
            <p className="text-gray-600">The requested page could not be found.</p>
          </div>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      
      {/* Main Content */}
      <main className="flex-1">
        {renderTabContent()}
      </main>

      {/* Modals */}
      {showModal && (
        <AgentModal
          agent={selectedAgent}
          onClose={() => setShowModal(false)}
          onSave={loadAgents}
        />
      )}

      {showChatModal && chatAgent && (
        <ChatModal
          agent={chatAgent}
          onClose={() => setShowChatModal(false)}
        />
      )}
    </div>
  );
};

export default AgentManagement;
