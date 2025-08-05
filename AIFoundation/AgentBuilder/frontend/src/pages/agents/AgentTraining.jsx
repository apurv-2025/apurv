import React, { useState, useEffect } from 'react';
import { Bot, Play, Download, RefreshCw, Brain, Globe, Database } from 'lucide-react';
import AgentTrainingCard from '../../components/agent/AgentTrainingCard';
import TrainingProgress from '../../components/agent/TrainingProgress';
import UrlScrapingForm from '../../components/agent/UrlScrapingForm';
import DataSourceSelector from '../../components/agent/DataSourceSelector';
import agentTrainingService from '../../services/agentTrainingService';

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
  const [agents, setAgents] = useState([]);
  const [aiModels, setAiModels] = useState([]);
  const [dataSourceOptions, setDataSourceOptions] = useState([]);

  useEffect(() => {
    // Load data from service
    setAgents(agentTrainingService.getAgents());
    setAiModels(agentTrainingService.getAIModels());
    setDataSourceOptions(agentTrainingService.getDataSourceOptions());
  }, []);

  const handleUrlScrape = async () => {
    if (!urlInput.trim()) return;
    
    setIsScrapingUrl(true);
    
    try {
      const scrapedDataItem = await agentTrainingService.scrapeUrl(urlInput);
      setScrapedData([...scrapedData, scrapedDataItem]);
      setUrlInput('');
    } catch (error) {
      console.error('Error scraping URL:', error);
    } finally {
      setIsScrapingUrl(false);
    }
  };

  const handleDataSourceToggle = (sourceId) => {
    setSelectedDataSources(prev => 
      prev.includes(sourceId) 
        ? prev.filter(id => id !== sourceId)
        : [...prev, sourceId]
    );
  };

  const startTraining = async () => {
    if (!selectedAgent) return;
    
    setIsTraining(true);
    setTrainingProgress(0);
    
    try {
      const result = await agentTrainingService.startTraining(selectedAgent.id, {
        model: selectedModel,
        dataSources: selectedDataSources
      });
      
      if (result.success) {
        // Update agent training status
        setSelectedAgent(prev => ({
          ...prev,
          trainingStatus: 'trained',
          accuracy: result.accuracy,
          lastTrained: new Date().toISOString().split('T')[0]
        }));
      }
    } catch (error) {
      console.error('Training failed:', error);
    } finally {
      setIsTraining(false);
      setTrainingProgress(100);
    }
  };

  const getStatusColor = (status) => {
    const colors = agentTrainingService.getTrainingStatusColors();
    return colors[status] || 'text-gray-600 bg-gray-100';
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
              <Play className="w-4 h-4" />
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
                <AgentTrainingCard
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

                <TrainingProgress isTraining={isTraining} progress={trainingProgress} />

                {/* Tabs */}
                <div className="border-b border-gray-200">
                  <nav className="-mb-px flex space-x-8">
                    {[
                      { id: 'overview', label: 'Overview', icon: Brain },
                      { id: 'url-scraping', label: 'URL Scraping', icon: Globe },
                      { id: 'data-sources', label: 'Data Sources', icon: Database },
                      { id: 'training-history', label: 'Training History', icon: RefreshCw }
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
                      <button 
                        onClick={startTraining}
                        disabled={isTraining}
                        className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
                      >
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
                  <UrlScrapingForm
                    urlInput={urlInput}
                    setUrlInput={setUrlInput}
                    isScrapingUrl={isScrapingUrl}
                    handleUrlScrape={handleUrlScrape}
                  />

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
                                  View
                                </button>
                                <button className="p-2 text-gray-400 hover:text-red-600">
                                  Delete
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
                <DataSourceSelector
                  dataSourceOptions={dataSourceOptions}
                  selectedDataSources={selectedDataSources}
                  handleDataSourceToggle={handleDataSourceToggle}
                />
              )}

              {activeTab === 'training-history' && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200">
                  <div className="p-6 border-b border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-900">Training History</h3>
                  </div>
                  <div className="divide-y divide-gray-200">
                    {agentTrainingService.getTrainingHistory(selectedAgent.id).map((session, index) => (
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