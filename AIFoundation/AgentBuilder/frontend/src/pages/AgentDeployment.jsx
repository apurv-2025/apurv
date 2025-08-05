import React, { useState, useRef, useEffect } from 'react';
import { 
  Bot, 
  Play, 
  Pause,
  Send,
  MessageSquare,
  Cloud,
  Server,
  CheckCircle,
  AlertCircle,
  Loader,
  X,
  Settings,
  Monitor,
  Globe,
  Shield,
  Zap,
  Database,
  Activity,
  Download,
  Upload,
  RefreshCw,
  ExternalLink,
  Copy,
  Eye,
  AlertTriangle,
  Clock,
  Target,
  BarChart3,
  Users,
  DollarSign
} from 'lucide-react';

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
  const chatEndRef = useRef(null);

  // Mock agents data
  const agents = [
    {
      id: 1,
      name: "Billing Support Bot",
      template: "billing",
      status: "ready",
      deploymentStatus: "deployed",
      version: "v1.2",
      lastTested: "2025-01-28",
      accuracy: 94,
      cloudVendor: "aws",
      endpoint: "https://api.billing-bot.com",
      region: "us-east-1"
    },
    {
      id: 2,
      name: "Front Desk Assistant",
      template: "reception",
      status: "ready",
      deploymentStatus: "staging",
      version: "v2.0",
      lastTested: "2025-01-27",
      accuracy: 98,
      cloudVendor: "azure",
      endpoint: "https://staging.frontdesk-bot.com",
      region: "east-us"
    },
    {
      id: 3,
      name: "Sales Consultant",
      template: "sales",
      status: "testing",
      deploymentStatus: "not_deployed",
      version: "v1.0",
      lastTested: "2025-01-26",
      accuracy: 87,
      cloudVendor: "",
      endpoint: "",
      region: ""
    }
  ];

  // Cloud vendor options
  const cloudVendors = [
    {
      id: 'aws',
      name: 'Amazon Web Services',
      logo: '🔶',
      regions: [
        { id: 'us-east-1', name: 'US East (N. Virginia)', latency: '12ms' },
        { id: 'us-west-2', name: 'US West (Oregon)', latency: '45ms' },
        { id: 'eu-west-1', name: 'Europe (Ireland)', latency: '89ms' },
        { id: 'ap-southeast-1', name: 'Asia Pacific (Singapore)', latency: '156ms' }
      ],
      instanceTypes: [
        { id: 't3.micro', name: 't3.micro', cpu: '2 vCPUs', memory: '1GB', cost: '$8.76/month' },
        { id: 't3.small', name: 't3.small', cpu: '2 vCPUs', memory: '2GB', cost: '$17.52/month' },
        { id: 't3.medium', name: 't3.medium', cpu: '2 vCPUs', memory: '4GB', cost: '$35.04/month' },
        { id: 'c5.large', name: 'c5.large', cpu: '2 vCPUs', memory: '4GB', cost: '$62.56/month' }
      ],
      features: ['Auto Scaling', 'Load Balancing', 'CloudWatch Monitoring', 'S3 Storage']
    },
    {
      id: 'azure',
      name: 'Microsoft Azure',
      logo: '🔷',
      regions: [
        { id: 'east-us', name: 'East US', latency: '15ms' },
        { id: 'west-us-2', name: 'West US 2', latency: '42ms' },
        { id: 'west-europe', name: 'West Europe', latency: '92ms' },
        { id: 'southeast-asia', name: 'Southeast Asia', latency: '162ms' }
      ],
      instanceTypes: [
        { id: 'B1s', name: 'B1s', cpu: '1 vCPU', memory: '1GB', cost: '$7.59/month' },
        { id: 'B2s', name: 'B2s', cpu: '2 vCPUs', memory: '4GB', cost: '$30.37/month' },
        { id: 'D2s_v3', name: 'D2s v3', cpu: '2 vCPUs', memory: '8GB', cost: '$70.08/month' },
        { id: 'F2s_v2', name: 'F2s v2', cpu: '2 vCPUs', memory: '4GB', cost: '$60.74/month' }
      ],
      features: ['Auto Scaling', 'Application Gateway', 'Azure Monitor', 'Blob Storage']
    },
    {
      id: 'gcp',
      name: 'Google Cloud Platform',
      logo: '🟡',
      regions: [
        { id: 'us-central1', name: 'US Central (Iowa)', latency: '18ms' },
        { id: 'us-west1', name: 'US West (Oregon)', latency: '48ms' },
        { id: 'europe-west1', name: 'Europe West (Belgium)', latency: '95ms' },
        { id: 'asia-southeast1', name: 'Asia Southeast (Singapore)', latency: '168ms' }
      ],
      instanceTypes: [
        { id: 'e2-micro', name: 'e2-micro', cpu: '2 vCPUs', memory: '1GB', cost: '$6.11/month' },
        { id: 'e2-small', name: 'e2-small', cpu: '2 vCPUs', memory: '2GB', cost: '$12.23/month' },
        { id: 'e2-medium', name: 'e2-medium', cpu: '2 vCPUs', memory: '4GB', cost: '$24.46/month' },
        { id: 'n2-standard-2', name: 'n2-standard-2', cpu: '2 vCPUs', memory: '8GB', cost: '$63.74/month' }
      ],
      features: ['Auto Scaling', 'Load Balancing', 'Cloud Monitoring', 'Cloud Storage']
    }
  ];

  const deploymentStatuses = {
    'not_deployed': { color: 'text-gray-600 bg-gray-100', label: 'Not Deployed' },
    'deploying': { color: 'text-blue-600 bg-blue-100', label: 'Deploying' },
    'staging': { color: 'text-yellow-600 bg-yellow-100', label: 'Staging' },
    'deployed': { color: 'text-green-600 bg-green-100', label: 'Production' },
    'failed': { color: 'text-red-600 bg-red-100', label: 'Failed' }
  };

  const sendTestMessage = async () => {
    if (!testMessage.trim() || isTestingAgent) return;

    const userMessage = { type: 'user', content: testMessage, timestamp: new Date() };
    setTestConversation(prev => [...prev, userMessage]);
    setTestMessage('');
    setIsTestingAgent(true);

    // Simulate agent response
    setTimeout(() => {
      const agentResponse = {
        type: 'agent',
        content: `Hello! I'm ${selectedAgent.name}. I understand you said: "${userMessage.content}". How can I help you with that?`,
        timestamp: new Date(),
        confidence: Math.random() * 0.3 + 0.7, // 70-100% confidence
        processingTime: Math.random() * 2000 + 500 // 500-2500ms
      };
      setTestConversation(prev => [...prev, agentResponse]);
      setIsTestingAgent(false);
    }, Math.random() * 2000 + 1000);
  };

  const startDeployment = () => {
    setIsDeploying(true);
    setDeploymentProgress(0);
    
    const stages = [
      'Validating configuration...',
      'Creating cloud resources...',
      'Deploying agent container...',
      'Setting up load balancer...',
      'Configuring auto-scaling...',
      'Running health checks...',
      'Deployment complete!'
    ];

    let currentStage = 0;
    const interval = setInterval(() => {
      setDeploymentProgress(prev => {
        const newProgress = prev + Math.random() * 20;
        if (newProgress >= 100) {
          clearInterval(interval);
          setIsDeploying(false);
          // Update agent deployment status
          if (selectedAgent) {
            setSelectedAgent(prev => ({
              ...prev,
              deploymentStatus: 'deployed',
              endpoint: `https://api.${prev.name.toLowerCase().replace(/\s+/g, '-')}.com`,
              cloudVendor: selectedCloudVendor,
              region: deploymentConfig.region
            }));
          }
          return 100;
        }
        return newProgress;
      });
      
      if (currentStage < stages.length - 1) {
        currentStage++;
      }
    }, 1500);
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [testConversation]);

  const getStatusColor = (status) => {
    return deploymentStatuses[status]?.color || 'text-gray-600 bg-gray-100';
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
                  {deploymentStatuses[selectedAgent.deploymentStatus]?.label}
                </span>
                <button
                  onClick={startDeployment}
                  disabled={!selectedCloudVendor || isDeploying || selectedAgent.deploymentStatus === 'deployed'}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  {isDeploying ? <Loader className="w-4 h-4 animate-spin" /> : <Cloud className="w-4 h-4" />}
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
                <div
                  key={agent.id}
                  onClick={() => setSelectedAgent(agent)}
                  className={`p-4 border rounded-lg cursor-pointer transition-all ${
                    selectedAgent?.id === agent.id 
                      ? 'border-blue-300 bg-blue-50' 
                      : 'border-gray-200 hover:border-blue-200 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="font-medium text-gray-900">{agent.name}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(agent.deploymentStatus)}`}>
                      {deploymentStatuses[agent.deploymentStatus]?.label}
                    </span>
                  </div>
                  
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between text-gray-600">
                      <span>Version:</span>
                      <span className="font-medium">{agent.version}</span>
                    </div>
                    <div className="flex justify-between text-gray-600">
                      <span>Accuracy:</span>
                      <span className="font-medium">{agent.accuracy}%</span>
                    </div>
                    {agent.cloudVendor && (
                      <div className="flex justify-between text-gray-600">
                        <span>Cloud:</span>
                        <span className="font-medium capitalize">{agent.cloudVendor}</span>
                      </div>
                    )}
                    <div className="flex justify-between text-gray-600">
                      <span>Last Tested:</span>
                      <span className="font-medium">{agent.lastTested}</span>
                    </div>
                  </div>
                </div>
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

                {/* Deployment Progress */}
                {isDeploying && (
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">Deployment Progress</span>
                      <span className="text-sm text-gray-600">{Math.round(deploymentProgress)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${deploymentProgress}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                {/* Tabs */}
                <div className="border-b border-gray-200">
                  <nav className="-mb-px flex space-x-8">
                    {['overview', 'test-preview', 'cloud-config', 'deployment-status'].map((tab) => (
                      <button
                        key={tab}
                        onClick={() => setActiveTab(tab)}
                        className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                          activeTab === tab
                            ? 'border-blue-500 text-blue-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                        }`}
                      >
                        {tab.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </button>
                    ))}
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
                          {deploymentStatuses[selectedAgent.deploymentStatus]?.label}
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
                          <a href={selectedAgent.endpoint} className="text-blue-600 hover:text-blue-800 text-sm font-medium flex items-center">
                            <ExternalLink className="w-3 h-3 mr-1" />
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
                  {/* Chat Interface */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col h-96">
                    <div className="p-4 border-b border-gray-200">
                      <h3 className="text-lg font-semibold text-gray-900">Test Conversation</h3>
                      <p className="text-sm text-gray-600">Test your agent's responses in real-time</p>
                    </div>
                    
                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                      {testConversation.length === 0 ? (
                        <div className="text-center text-gray-500 mt-8">
                          <Bot className="w-12 h-12 mx-auto mb-4 text-gray-300" />
                          <p>Start a conversation to test your agent</p>
                        </div>
                      ) : (
                        testConversation.map((message, index) => (
                          <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                            <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                              message.type === 'user' 
                                ? 'bg-blue-600 text-white' 
                                : 'bg-gray-100 text-gray-900'
                            }`}>
                              <p className="text-sm">{message.content}</p>
                              {message.type === 'agent' && (
                                <div className="mt-2 text-xs opacity-75">
                                  <div>Confidence: {(message.confidence * 100).toFixed(1)}%</div>
                                  <div>Response time: {message.processingTime.toFixed(0)}ms</div>
                                </div>
                              )}
                            </div>
                          </div>
                        ))
                      )}
                      {isTestingAgent && (
                        <div className="flex justify-start">
                          <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                            <div className="flex items-center space-x-2">
                              <Loader className="w-4 h-4 animate-spin" />
                              <span className="text-sm">Agent is thinking...</span>
                            </div>
                          </div>
                        </div>
                      )}
                      <div ref={chatEndRef} />
                    </div>
                    
                    <div className="p-4 border-t border-gray-200">
                      <div className="flex space-x-2">
                        <input
                          type="text"
                          value={testMessage}
                          onChange={(e) => setTestMessage(e.target.value)}
                          onKeyPress={(e) => e.key === 'Enter' && sendTestMessage()}
                          placeholder="Type your message..."
                          className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          disabled={isTestingAgent}
                        />
                        <button
                          onClick={sendTestMessage}
                          disabled={!testMessage.trim() || isTestingAgent}
                          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                        >
                          <Send className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Test Results */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Test Results</h3>
                    
                    {testConversation.length === 0 ? (
                      <div className="text-center text-gray-500 py-8">
                        <Target className="w-12 h-12 mx-auto mb-4 text-gray-300" />
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
                          <RefreshCw className="w-4 h-4" />
                          <span>Clear Chat</span>
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {activeTab === 'cloud-config' && (
                <div className="space-y-6">
                  {/* Cloud Vendor Selection */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Cloud Vendor</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {cloudVendors.map((vendor) => (
                        <div
                          key={vendor.id}
                          onClick={() => setSelectedCloudVendor(vendor.id)}
                          className={`p-4 border rounded-lg cursor-pointer transition-all ${
                            selectedCloudVendor === vendor.id 
                              ? 'border-blue-300 bg-blue-50' 
                              : 'border-gray-200 hover:border-blue-200'
                          }`}
                        >
                          <div className="text-center">
                            <div className="text-4xl mb-2">{vendor.logo}</div>
                            <h4 className="font-medium text-gray-900">{vendor.name}</h4>
                            <div className="mt-2 flex flex-wrap gap-1 justify-center">
                              {vendor.features.slice(0, 2).map(feature => (
                                <span key={feature} className="text-xs bg-gray-100 px-2 py-1 rounded">
                                  {feature}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Configuration Options */}
                  {selectedVendor && (
                    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                      <h3 className="text-lg font-semibold text-gray-900 mb-4">Deployment Configuration</h3>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Region Selection */}
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Region</label>
                          <select
                            value={deploymentConfig.region}
                            onChange={(e) => setDeploymentConfig({ ...deploymentConfig, region: e.target.value })}
                            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          >
                            <option value="">Select region...</option>
                            {selectedVendor.regions.map(region => (
                              <option key={region.id} value={region.id}>
                                {region.name} ({region.latency})
                              </option>
                            ))}
                          </select>
                        </div>

                        {/* Instance Type */}
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Instance Type</label>
                          <select
                            value={deploymentConfig.instanceType}
                            onChange={(e) => setDeploymentConfig({ ...deploymentConfig, instanceType: e.target.value })}
                            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          >
                            <option value="">Select instance...</option>
                            {selectedVendor.instanceTypes.map(instance => (
                              <option key={instance.id} value={instance.id}>
                                {instance.name} - {instance.cpu}, {instance.memory} ({instance.cost})
                              </option>
                            ))}
                          </select>
                        </div>

                        {/* Scaling */}
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Scaling</label>
                          <select
                            value={deploymentConfig.scaling}
                            onChange={(e) => setDeploymentConfig({ ...deploymentConfig, scaling: e.target.value })}
                            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          >
                            <option value="auto">Auto Scaling</option>
                            <option value="manual">Manual Scaling</option>
                            <option value="fixed">Fixed Instances</option>
                          </select>
                        </div>

                        {/* Environment */}
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">Environment</label>
                          <select
                            value={deploymentConfig.environment}
                            onChange={(e) => setDeploymentConfig({ ...deploymentConfig, environment: e.target.value })}
                            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          >
                            <option value="staging">Staging</option>
                            <option value="production">Production</option>
                          </select>
                        </div>
                      </div>

                      {/* Cost Estimate */}
                      {deploymentConfig.instanceType && (
                        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                          <h4 className="font-medium text-blue-900 mb-2">Estimated Monthly Cost</h4>
                          <div className="text-2xl font-bold text-blue-600">
                            {selectedVendor.instanceTypes.find(i => i.id === deploymentConfig.instanceType)?.cost || 'N/A'}
                          </div>
                          <p className="text-sm text-blue-700 mt-1">
                            Includes compute, storage, and basic monitoring
                          </p>
                        </div>
                      )}
                    </div>
                  )}
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
                          {selectedAgent.deploymentStatus === 'deployed' ? <CheckCircle className="w-8 h-8 mx-auto" /> :
                           selectedAgent.deploymentStatus === 'staging' ? <Clock className="w-8 h-8 mx-auto" /> :
                           selectedAgent.deploymentStatus === 'deploying' ? <Loader className="w-8 h-8 mx-auto animate-spin" /> :
                           <AlertCircle className="w-8 h-8 mx-auto" />}
                        </div>
                        <div className="font-medium text-gray-900">
                          {deploymentStatuses[selectedAgent.deploymentStatus]?.label}
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
                            <Copy className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Deployment History */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="p-6 border-b border-gray-200">
                      <h3 className="text-lg font-semibold text-gray-900">Deployment History</h3>
                    </div>
                    <div className="divide-y divide-gray-200">
                      {[
                        { 
                          date: '2025-01-28', 
                          version: 'v1.2', 
                          status: 'deployed', 
                          environment: 'production',
                          duration: '4m 32s'
                        },
                        { 
                          date: '2025-01-25', 
                          version: 'v1.1', 
                          status: 'deployed', 
                          environment: 'staging',
                          duration: '3m 45s'
                        },
                        { 
                          date: '2025-01-20', 
                          version: 'v1.0', 
                          status: 'failed', 
                          environment: 'production',
                          duration: '1m 15s'
                        }
                      ].map((deployment, index) => (
                        <div key={index} className="p-6 hover:bg-gray-50">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4">
                              <div className={`w-3 h-3 rounded-full ${
                                deployment.status === 'deployed' ? 'bg-green-500' :
                                deployment.status === 'failed' ? 'bg-red-500' : 'bg-yellow-500'
                              }`}></div>
                              <div>
                                <h4 className="font-medium text-gray-900">{deployment.version}</h4>
                                <p className="text-sm text-gray-600">{deployment.date}</p>
                              </div>
                            </div>
                            <div className="text-right">
                              <div className="flex items-center space-x-4">
                                <div className="text-sm">
                                  <div className="text-gray-600">Environment</div>
                                  <div className="font-medium capitalize">{deployment.environment}</div>
                                </div>
                                <div className="text-sm">
                                  <div className="text-gray-600">Duration</div>
                                  <div className="font-medium">{deployment.duration}</div>
                                </div>
                                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(deployment.status)}`}>
                                  {deployment.status}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Performance Metrics */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <div className="text-center p-4 bg-blue-50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-600">99.9%</div>
                        <div className="text-sm text-gray-600">Uptime</div>
                      </div>
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-600">245ms</div>
                        <div className="text-sm text-gray-600">Avg Response</div>
                      </div>
                      <div className="text-center p-4 bg-purple-50 rounded-lg">
                        <div className="text-2xl font-bold text-purple-600">1.2K</div>
                        <div className="text-sm text-gray-600">Daily Requests</div>
                      </div>
                      <div className="text-center p-4 bg-orange-50 rounded-lg">
                        <div className="text-2xl font-bold text-orange-600">$45</div>
                        <div className="text-sm text-gray-600">Monthly Cost</div>
                      </div>
                    </div>
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