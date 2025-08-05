import React, { useState, useEffect } from 'react';
import { Bot, Cloud, Play, MessageSquare, Monitor, Settings } from 'lucide-react';
import AgentDeploymentCard from '../../components/agent/AgentDeploymentCard';
import DeploymentProgress from '../../components/agent/DeploymentProgress';
import AgentTestChat from '../../components/agent/AgentTestChat';
import CloudVendorSelector from '../../components/agent/CloudVendorSelector';
import DeploymentConfig from '../../components/agent/DeploymentConfig';
import agentDeploymentService from '../../services/agentDeploymentService';

const AgentDeployment = () => {
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [testMessage, setTestMessage] = useState('');
  const [testConversation, setTestConversation] = useState([]);
  const [isTestingAgent, setIsTestingAgent] = useState(false);
  const [selectedCloudVendor, setSelectedCloudVendor] = useState('');
  const [deploymentConfig, setDeploymentConfig] = useState({
    region: '',
    instanceType: '',
    scaling: 'auto',
    environment: 'staging'
  });
  const [isDeploying, setIsDeploying] = useState(false);
  const [deploymentProgress, setDeploymentProgress] = useState(0);
  const [agents, setAgents] = useState([]);
  const [cloudVendors, setCloudVendors] = useState([]);

  useEffect(() => {
    // Load data from service
    setAgents(agentDeploymentService.getAgents());
    setCloudVendors(agentDeploymentService.getCloudVendors());
  }, []);

  const sendTestMessage = async () => {
    if (!testMessage.trim() || isTestingAgent || !selectedAgent) return;

    const userMessage = { type: 'user', content: testMessage, timestamp: new Date() };
    setTestConversation(prev => [...prev, userMessage]);
    setTestMessage('');
    setIsTestingAgent(true);

    try {
      const agentResponse = await agentDeploymentService.testAgent(selectedAgent.id, testMessage);
      setTestConversation(prev => [...prev, agentResponse]);
    } catch (error) {
      console.error('Error testing agent:', error);
    } finally {
      setIsTestingAgent(false);
    }
  };

  const startDeployment = async () => {
    if (!selectedAgent || !selectedCloudVendor) return;
    
    setIsDeploying(true);
    setDeploymentProgress(0);
    
    try {
      const result = await agentDeploymentService.deployAgent(selectedAgent.id, deploymentConfig);
      if (result.success) {
        // Update agent deployment status
        setSelectedAgent(prev => ({
          ...prev,
          deploymentStatus: 'deployed',
          endpoint: result.endpoint,
          cloudVendor: selectedCloudVendor,
          region: deploymentConfig.region
        }));
      }
    } catch (error) {
      console.error('Deployment failed:', error);
    } finally {
      setIsDeploying(false);
      setDeploymentProgress(100);
    }
  };

  const getStatusColor = (status) => {
    const statuses = agentDeploymentService.getDeploymentStatuses();
    return statuses[status]?.color || 'text-gray-600 bg-gray-100';
  };

  const selectedVendor = cloudVendors.find(v => v.id === selectedCloudVendor);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Bot className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">Agent Deployment</h1>
          </div>
          <div className="flex items-center space-x-4">
            {selectedAgent && (
              <div className="flex items-center space-x-2">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(selectedAgent.deploymentStatus)}`}>
                  {agentDeploymentService.getDeploymentStatuses()[selectedAgent.deploymentStatus]?.label}
                </span>
                <button
                  onClick={startDeployment}
                  disabled={!selectedCloudVendor || isDeploying || selectedAgent.deploymentStatus === 'deployed'}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  <Cloud className="w-4 h-4" />
                  <span>{isDeploying ? 'Deploying...' : 'Deploy Agent'}</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="flex">
        {/* Sidebar - Agent Selection */}
        <div className="w-80 bg-white border-r border-gray-200 h-screen overflow-y-auto">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Select Agent</h2>
            
            <div className="space-y-4">
              {agents.map((agent) => (
                <AgentDeploymentCard
                  key={agent.id}
                  agent={agent}
                  isSelected={selectedAgent?.id === agent.id}
                  onClick={setSelectedAgent}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6">
          {!selectedAgent ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <Bot className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select an Agent to Deploy</h3>
                <p className="text-gray-600">Choose an agent from the sidebar to start deployment</p>
              </div>
            </div>
          ) : (
            <div>
              {/* Agent Header */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">{selectedAgent.name}</h2>
                    <p className="text-gray-600">Version {selectedAgent.version} • Ready for deployment</p>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-center">
                      <div className={`text-2xl font-bold ${selectedAgent.deploymentStatus === 'deployed' ? 'text-green-600' : 'text-gray-400'}`}>
                        {selectedAgent.deploymentStatus === 'deployed' ? '✓' : '○'}
                      </div>
                      <div className="text-sm text-gray-600">Status</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">{selectedAgent.accuracy}%</div>
                      <div className="text-sm text-gray-600">Accuracy</div>
                    </div>
                  </div>
                </div>

                <DeploymentProgress isDeploying={isDeploying} progress={deploymentProgress} />

                {/* Tabs */}
                <div className="border-b border-gray-200">
                  <nav className="-mb-px flex space-x-8">
                    {[
                      { id: 'overview', label: 'Overview', icon: Settings },
                      { id: 'test-preview', label: 'Test Preview', icon: MessageSquare },
                      { id: 'cloud-config', label: 'Cloud Config', icon: Cloud },
                      { id: 'deployment-status', label: 'Deployment Status', icon: Monitor }
                    ].map((tab) => {
                      const Icon = tab.icon;
                      return (
                        <button
                          key={tab.id}
                          onClick={() => setActiveTab(tab.id)}
                          className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors flex items-center space-x-2 ${
                            activeTab === tab.id
                              ? 'border-blue-500 text-blue-600'
                              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                          }`}
                        >
                          <Icon className="w-4 h-4" />
                          <span>{tab.label}</span>
                        </button>
                      );
                    })}
                  </nav>
                </div>
              </div>

              {/* Tab Content */}
              {activeTab === 'overview' && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Deployment Overview</h3>
                    <div className="space-y-4">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Current Status</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedAgent.deploymentStatus)}`}>
                          {agentDeploymentService.getDeploymentStatuses()[selectedAgent.deploymentStatus]?.label}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Version</span>
                        <span className="font-medium">{selectedAgent.version}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Test Accuracy</span>
                        <span className="font-medium">{selectedAgent.accuracy}%</span>
                      </div>
                      {selectedAgent.endpoint && (
                        <div className="flex justify-between">
                          <span className="text-gray-600">Endpoint</span>
                          <a href={selectedAgent.endpoint} className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                            API
                          </a>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                    <div className="space-y-3">
                      <button 
                        onClick={() => setActiveTab('test-preview')}
                        className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2"
                      >
                        <MessageSquare className="w-4 h-4" />
                        <span>Test Agent</span>
                      </button>
                      <button 
                        onClick={() => setActiveTab('cloud-config')}
                        className="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
                      >
                        <Cloud className="w-4 h-4" />
                        <span>Configure Deployment</span>
                      </button>
                      <button 
                        onClick={() => setActiveTab('deployment-status')}
                        className="w-full bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center space-x-2"
                      >
                        <Monitor className="w-4 h-4" />
                        <span>View Status</span>
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'test-preview' && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <AgentTestChat
                    testMessage={testMessage}
                    setTestMessage={setTestMessage}
                    testConversation={testConversation}
                    isTestingAgent={isTestingAgent}
                    sendTestMessage={sendTestMessage}
                  />

                  {/* Test Results */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Results</h3>
                    
                    {testConversation.length === 0 ? (
                      <div className="text-center text-gray-500 py-8">
                        <Bot className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                        <p>No test data yet</p>
                        <p className="text-sm">Start a conversation to see analytics</p>
                      </div>
                    ) : (
                      <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                          <div className="text-center p-3 bg-blue-50 rounded-lg">
                            <div className="text-2xl font-bold text-blue-600">
                              {testConversation.filter(m => m.type === 'agent').length}
                            </div>
                            <div className="text-sm text-gray-600">Responses</div>
                          </div>
                          <div className="text-center p-3 bg-green-50 rounded-lg">
                            <div className="text-2xl font-bold text-green-600">
                              {testConversation.filter(m => m.type === 'agent' && m.confidence > 0.8).length}
                            </div>
                            <div className="text-sm text-gray-600">High Confidence</div>
                          </div>
                        </div>
                        
                        <div>
                          <h4 className="font-medium text-gray-900 mb-2">Average Metrics</h4>
                          <div className="space-y-2">
                            <div className="flex justify-between">
                              <span className="text-gray-600">Confidence</span>
                              <span className="font-medium">
                                {(testConversation
                                  .filter(m => m.type === 'agent')
                                  .reduce((acc, m) => acc + m.confidence, 0) / 
                                  testConversation.filter(m => m.type === 'agent').length * 100
                                ).toFixed(1)}%
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-600">Response Time</span>
                              <span className="font-medium">
                                {(testConversation
                                  .filter(m => m.type === 'agent')
                                  .reduce((acc, m) => acc + m.processingTime, 0) / 
                                  testConversation.filter(m => m.type === 'agent').length
                                ).toFixed(0)}ms
                              </span>
                            </div>
                          </div>
                        </div>
                        
                        <button 
                          onClick={() => setTestConversation([])}
                          className="w-full bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors flex items-center justify-center space-x-2"
                        >
                          <span>Clear Chat</span>
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {activeTab === 'cloud-config' && (
                <div className="space-y-6">
                  <CloudVendorSelector
                    cloudVendors={cloudVendors}
                    selectedVendor={selectedCloudVendor}
                    onVendorSelect={setSelectedCloudVendor}
                  />

                  <DeploymentConfig
                    selectedVendor={selectedVendor}
                    deploymentConfig={deploymentConfig}
                    setDeploymentConfig={setDeploymentConfig}
                  />
                </div>
              )}

              {activeTab === 'deployment-status' && (
                <div className="space-y-6">
                  {/* Current Status */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Deployment Status</h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className={`text-3xl mb-2 ${
                          selectedAgent.deploymentStatus === 'deployed' ? 'text-green-600' : 
                          selectedAgent.deploymentStatus === 'staging' ? 'text-yellow-600' : 
                          selectedAgent.deploymentStatus === 'deploying' ? 'text-blue-600' : 'text-gray-400'
                        }`}>
                          {selectedAgent.deploymentStatus === 'deployed' ? '✓' :
                           selectedAgent.deploymentStatus === 'staging' ? '⏳' :
                           selectedAgent.deploymentStatus === 'deploying' ? '🔄' : '○'}
                        </div>
                        <div className="font-medium text-gray-900">
                          {agentDeploymentService.getDeploymentStatuses()[selectedAgent.deploymentStatus]?.label}
                        </div>
                      </div>
                      
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-600 mb-2">
                          {selectedAgent.cloudVendor ? selectedAgent.cloudVendor.toUpperCase() : 'N/A'}
                        </div>
                        <div className="font-medium text-gray-900">Cloud Provider</div>
                      </div>
                      
                      <div className="text-center p-4 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-600 mb-2">
                          {selectedAgent.region || 'N/A'}
                        </div>
                        <div className="font-medium text-gray-900">Region</div>
                      </div>
                    </div>

                    {selectedAgent.endpoint && (
                      <div className="mt-6 p-4 bg-green-50 rounded-lg">
                        <h4 className="font-medium text-green-900 mb-2">Agent Endpoint</h4>
                        <div className="flex items-center justify-between">
                          <code className="text-sm bg-white px-3 py-2 rounded border">
                            {selectedAgent.endpoint}
                          </code>
                          <button
                            onClick={() => navigator.clipboard.writeText(selectedAgent.endpoint)}
                            className="ml-2 p-2 text-green-600 hover:text-green-800"
                          >
                            Copy
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AgentDeployment; 