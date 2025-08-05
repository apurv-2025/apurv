import React, { useState, useRef } from 'react';
import { 
  Bot, 
  Upload, 
  Link, 
  Database, 
  Play, 
  Pause,
  CheckCircle,
  AlertCircle,
  Loader,
  X,
  Plus,
  Download,
  Eye,
  RefreshCw,
  Globe,
  FileText,
  Settings,
  BarChart3,
  Clock,
  Users,
  CreditCard,
  Calendar,
  Mail,
  Phone,
  ShoppingCart,
  Trash2,
  Edit3,
  Save,
  Filter,
  Search
} from 'lucide-react';

const AgentTraining = () => {
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [isTraining, setIsTraining] = useState(false);
  const [trainingProgress, setTrainingProgress] = useState(0);
  const [urlInput, setUrlInput] = useState('');
  const [isScrapingUrl, setIsScrapingUrl] = useState(false);
  const [scrapedData, setScrapedData] = useState([]);
  const [selectedDataSources, setSelectedDataSources] = useState([]);
  const [selectedModel, setSelectedModel] = useState('apurv-ops-1');
  const fileInputRef = useRef(null);

  // Mock agents data
  const agents = [
    {
      id: 1,
      name: "Billing Support Bot",
      template: "billing",
      status: "active",
      trainingStatus: "trained",
      accuracy: 94,
      lastTrained: "2025-01-25",
      trainingData: 15420,
      conversations: 1247
    },
    {
      id: 2,
      name: "Front Desk Assistant",
      template: "reception",
      status: "active",
      trainingStatus: "training",
      accuracy: 89,
      lastTrained: "2025-01-28",
      trainingData: 8932,
      conversations: 892
    },
    {
      id: 3,
      name: "Sales Consultant",
      template: "sales",
      status: "paused",
      trainingStatus: "needs_training",
      accuracy: 72,
      lastTrained: "2025-01-15",
      trainingData: 3421,
      conversations: 543
    }
  ];

  // AI Models - simplified to just the 3 Apurv-Ops models
  const aiModels = [
    {
      id: 'apurv-ops-1',
      name: 'Apurv-Ops-1',
      description: 'General purpose operations model'
    },
    {
      id: 'apurv-ops-2',
      name: 'Apurv-Ops-2',
      description: 'Enhanced operations model'
    },
    {
      id: 'apurv-ops-3',
      name: 'Apurv-Ops-3',
      description: 'Advanced operations model'
    }
  ];

  // Data source options with EHR integrations
  const dataSourceOptions = [
    {
      category: "EHR Systems",
      sources: [
        { id: 'epic', name: 'Epic', type: 'ehr', icon: Database, status: 'connected' },
        { id: 'cerner', name: 'Cerner (Oracle Health)', type: 'ehr', icon: Database, status: 'available' },
        { id: 'allscripts', name: 'Allscripts', type: 'ehr', icon: Database, status: 'available' },
        { id: 'athenahealth', name: 'athenahealth', type: 'ehr', icon: Database, status: 'connected' },
        { id: 'eclinicalworks', name: 'eClinicalWorks', type: 'ehr', icon: Database, status: 'available' }
      ]
    },
    {
      category: "Practice Management",
      sources: [
        { id: 'change_healthcare', name: 'Change Healthcare', type: 'clearinghouse', icon: CreditCard, status: 'connected' },
        { id: 'availity', name: 'Availity', type: 'clearinghouse', icon: CreditCard, status: 'available' },
        { id: 'surescripts', name: 'Surescripts', type: 'prescription', icon: FileText, status: 'connected' }
      ]
    },
    {
      category: "Business Systems",
      sources: [
        { id: 'quickbooks', name: 'QuickBooks', type: 'accounting', icon: BarChart3, status: 'connected' },
        { id: 'salesforce', name: 'Salesforce CRM', type: 'crm', icon: Users, status: 'available' },
        { id: 'calendar', name: 'Google Calendar', type: 'scheduling', icon: Calendar, status: 'connected' }
      ]
    },
    {
      category: "Communication",
      sources: [
        { id: 'gmail', name: 'Gmail', type: 'email', icon: Mail, status: 'connected' },
        { id: 'slack', name: 'Slack', type: 'messaging', icon: Phone, status: 'available' },
        { id: 'zendesk', name: 'Zendesk', type: 'support', icon: Settings, status: 'available' }
      ]
    }
  ];

  const handleUrlScrape = async () => {
    if (!urlInput.trim()) return;
    
    setIsScrapingUrl(true);
    
    // Simulate URL scraping
    setTimeout(() => {
      const mockScrapedData = {
        id: Date.now(),
        url: urlInput,
        title: `Data from ${new URL(urlInput).hostname}`,
        pages: Math.floor(Math.random() * 50) + 10,
        dataPoints: Math.floor(Math.random() * 1000) + 500,
        status: 'completed',
        scrapedAt: new Date().toISOString(),
        content: [
          'FAQ sections',
          'Product descriptions',
          'Service information',
          'Contact details',
          'Policy documents'
        ]
      };
      
      setScrapedData([...scrapedData, mockScrapedData]);
      setUrlInput('');
      setIsScrapingUrl(false);
    }, 3000);
  };

  const handleDataSourceToggle = (sourceId) => {
    setSelectedDataSources(prev => 
      prev.includes(sourceId) 
        ? prev.filter(id => id !== sourceId)
        : [...prev, sourceId]
    );
  };

  const startTraining = () => {
    setIsTraining(true);
    setTrainingProgress(0);
    
    const interval = setInterval(() => {
      setTrainingProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsTraining(false);
          return 100;
        }
        return prev + Math.random() * 10;
      });
    }, 500);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'trained': return 'text-green-600 bg-green-100';
      case 'training': return 'text-blue-600 bg-blue-100';
      case 'needs_training': return 'text-orange-600 bg-orange-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getConnectionStatus = (status) => {
    switch (status) {
      case 'connected': return 'text-green-600 bg-green-100';
      case 'available': return 'text-gray-600 bg-gray-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Bot className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">Agent Training</h1>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={startTraining}
              disabled={!selectedAgent || isTraining}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              {isTraining ? <Loader className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              <span>{isTraining ? 'Training...' : 'Start Training'}</span>
            </button>
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
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(agent.trainingStatus)}`}>
                      {agent.trainingStatus.replace('_', ' ')}
                    </span>
                  </div>
                  
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between text-gray-600">
                      <span>Accuracy:</span>
                      <span className="font-medium">{agent.accuracy}%</span>
                    </div>
                    <div className="flex justify-between text-gray-600">
                      <span>Training Data:</span>
                      <span className="font-medium">{agent.trainingData.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between text-gray-600">
                      <span>Last Trained:</span>
                      <span className="font-medium">{agent.lastTrained}</span>
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
                <h3 className="text-lg font-medium text-gray-900 mb-2">Select an Agent to Train</h3>
                <p className="text-gray-600">Choose an agent from the sidebar to start training</p>
              </div>
            </div>
          ) : (
            <div>
              {/* Agent Header */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">{selectedAgent.name}</h2>
                    <p className="text-gray-600">Training and data management</p>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-blue-600">{selectedAgent.accuracy}%</div>
                      <div className="text-sm text-gray-600">Accuracy</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">{selectedAgent.trainingData.toLocaleString()}</div>
                      <div className="text-sm text-gray-600">Data Points</div>
                    </div>
                  </div>
                </div>

                {/* Training Progress */}
                {isTraining && (
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700">Training Progress</span>
                      <span className="text-sm text-gray-600">{Math.round(trainingProgress)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${trainingProgress}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                {/* Tabs */}
                <div className="border-b border-gray-200">
                  <nav className="-mb-px flex space-x-8">
                    {['overview', 'url-scraping', 'data-sources', 'training-history'].map((tab) => (
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
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Training Statistics</h3>
                    <div className="space-y-4">
                      <div className="flex justify-between">
                        <span className="text-gray-600">AI Model</span>
                        <div className="flex items-center space-x-2">
                          <select
                            value={selectedModel}
                            onChange={(e) => setSelectedModel(e.target.value)}
                            className="border border-gray-300 rounded px-3 py-1 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          >
                            {aiModels.map(model => (
                              <option key={model.id} value={model.id}>
                                {model.name}
                              </option>
                            ))}
                          </select>
                        </div>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Total Conversations</span>
                        <span className="font-medium">{selectedAgent.conversations}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Success Rate</span>
                        <span className="font-medium">{selectedAgent.accuracy}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Training Data Points</span>
                        <span className="font-medium">{selectedAgent.trainingData.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Last Updated</span>
                        <span className="font-medium">{selectedAgent.lastTrained}</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
                    <div className="space-y-3">
                      <button className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2">
                        <Play className="w-4 h-4" />
                        <span>Start Training Session</span>
                      </button>
                      <button className="w-full bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2">
                        <Download className="w-4 h-4" />
                        <span>Export Training Data</span>
                      </button>
                      <button className="w-full bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors flex items-center justify-center space-x-2">
                        <RefreshCw className="w-4 h-4" />
                        <span>Reset Training</span>
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'url-scraping' && (
                <div className="space-y-6">
                  {/* URL Input Section */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Website Data Scraping</h3>
                    <p className="text-gray-600 mb-4">Import training data from existing websites, documentation, or knowledge bases.</p>
                    
                    <div className="flex space-x-4">
                      <div className="flex-1">
                        <input
                          type="url"
                          value={urlInput}
                          onChange={(e) => setUrlInput(e.target.value)}
                          placeholder="https://example.com"
                          className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                      <button
                        onClick={handleUrlScrape}
                        disabled={!urlInput.trim() || isScrapingUrl}
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
                      >
                        {isScrapingUrl ? <Loader className="w-4 h-4 animate-spin" /> : <Globe className="w-4 h-4" />}
                        <span>{isScrapingUrl ? 'Scraping...' : 'Scrape URL'}</span>
                      </button>
                    </div>
                  </div>

                  {/* Scraped Data List */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                    <div className="p-6 border-b border-gray-200">
                      <h3 className="text-lg font-semibold text-gray-900">Scraped Data Sources</h3>
                    </div>
                    <div className="divide-y divide-gray-200">
                      {scrapedData.length === 0 ? (
                        <div className="p-6 text-center text-gray-500">
                          No scraped data yet. Add a URL above to get started.
                        </div>
                      ) : (
                        scrapedData.map((data) => (
                          <div key={data.id} className="p-6 hover:bg-gray-50">
                            <div className="flex items-center justify-between">
                              <div className="flex-1">
                                <h4 className="font-medium text-gray-900">{data.title}</h4>
                                <p className="text-sm text-gray-600 mt-1">{data.url}</p>
                                <div className="flex items-center space-x-4 mt-2">
                                  <span className="text-xs text-gray-500">{data.pages} pages</span>
                                  <span className="text-xs text-gray-500">{data.dataPoints} data points</span>
                                  <span className="text-xs text-gray-500">Scraped on {new Date(data.scrapedAt).toLocaleDateString()}</span>
                                </div>
                              </div>
                              <div className="flex items-center space-x-2">
                                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                                  {data.status}
                                </span>
                                <button className="p-2 text-gray-400 hover:text-gray-600">
                                  <Eye className="w-4 h-4" />
                                </button>
                                <button className="p-2 text-gray-400 hover:text-red-600">
                                  <Trash2 className="w-4 h-4" />
                                </button>
                              </div>
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'data-sources' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Data Sources</h3>
                    <p className="text-gray-600 mb-6">Select data sources to import training data from your connected systems.</p>
                    
                    {dataSourceOptions.map((category) => (
                      <div key={category.category} className="mb-8">
                        <h4 className="font-medium text-gray-900 mb-4">{category.category}</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {category.sources.map((source) => {
                            const IconComponent = source.icon;
                            const isSelected = selectedDataSources.includes(source.id);
                            const isConnected = source.status === 'connected';
                            
                            return (
                              <div
                                key={source.id}
                                onClick={() => isConnected && handleDataSourceToggle(source.id)}
                                className={`p-4 border rounded-lg transition-all cursor-pointer ${
                                  isSelected 
                                    ? 'border-blue-300 bg-blue-50' 
                                    : isConnected 
                                      ? 'border-gray-200 hover:border-blue-200' 
                                      : 'border-gray-200 opacity-50 cursor-not-allowed'
                                }`}
                              >
                                <div className="flex items-center space-x-3">
                                  <div className={`p-2 rounded-lg ${
                                    isConnected ? 'bg-green-100' : 'bg-gray-100'
                                  }`}>
                                    <IconComponent className={`w-5 h-5 ${
                                      isConnected ? 'text-green-600' : 'text-gray-400'
                                    }`} />
                                  </div>
                                  <div className="flex-1">
                                    <h5 className="font-medium text-gray-900">{source.name}</h5>
                                    <div className="flex items-center space-x-2 mt-1">
                                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getConnectionStatus(source.status)}`}>
                                        {source.status}
                                      </span>
                                      {isSelected && (
                                        <CheckCircle className="w-4 h-4 text-blue-600" />
                                      )}
                                    </div>
                                  </div>
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    ))}

                    {selectedDataSources.length > 0 && (
                      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                        <h4 className="font-medium text-blue-900 mb-2">Selected Data Sources ({selectedDataSources.length})</h4>
                        <div className="flex flex-wrap gap-2">
                          {selectedDataSources.map((sourceId) => {
                            const source = dataSourceOptions
                              .flatMap(cat => cat.sources)
                              .find(s => s.id === sourceId);
                            return (
                              <span key={sourceId} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                                {source?.name}
                              </span>
                            );
                          })}
                        </div>
                        <button className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                          Import Data from Selected Sources
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {activeTab === 'training-history' && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                  <div className="p-6 border-b border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-900">Training History</h3>
                  </div>
                  <div className="divide-y divide-gray-200">
                    {[
                      { date: '2025-01-28', type: 'Full Training', duration: '2h 34m', accuracy: 94, dataPoints: 15420 },
                      { date: '2025-01-25', type: 'Incremental', duration: '45m', accuracy: 92, dataPoints: 3200 },
                      { date: '2025-01-20', type: 'Full Training', duration: '3h 12m', accuracy: 89, dataPoints: 12100 },
                      { date: '2025-01-15', type: 'Data Import', duration: '1h 20m', accuracy: 85, dataPoints: 8900 }
                    ].map((session, index) => (
                      <div key={index} className="p-6 hover:bg-gray-50">
                        <div className="flex items-center justify-between">
                          <div>
                            <h4 className="font-medium text-gray-900">{session.type}</h4>
                            <p className="text-sm text-gray-600 mt-1">{session.date}</p>
                          </div>
                          <div className="text-right">
                            <div className="flex items-center space-x-4">
                              <div className="text-sm">
                                <div className="text-gray-600">Duration</div>
                                <div className="font-medium">{session.duration}</div>
                              </div>
                              <div className="text-sm">
                                <div className="text-gray-600">Accuracy</div>
                                <div className="font-medium">{session.accuracy}%</div>
                              </div>
                              <div className="text-sm">
                                <div className="text-gray-600">Data Points</div>
                                <div className="font-medium">{session.dataPoints.toLocaleString()}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
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

export default AgentTraining;