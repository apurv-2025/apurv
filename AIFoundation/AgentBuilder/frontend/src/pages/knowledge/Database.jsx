import React, { useState, useEffect, useCallback } from 'react';
import { Upload, BookOpen } from 'lucide-react';
import { api } from '../../services/api';

const KnowledgeBase = () => {
  const [agents, setAgents] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [knowledgeItems, setKnowledgeItems] = useState([]);
  const [uploading, setUploading] = useState(false);

  const loadAgents = useCallback(async () => {
    try {
      const agentData = await api.getAgents();
      setAgents(agentData);
      if (agentData.length > 0 && !selectedAgent) {
        setSelectedAgent(agentData[0]);
      }
    } catch (error) {
      console.error('Error loading agents:', error);
    }
  }, [selectedAgent]);

  const loadKnowledgeBase = useCallback(async () => {
    if (!selectedAgent) return;
    
    try {
      const knowledge = await api.getKnowledgeBase(selectedAgent.id);
      setKnowledgeItems(knowledge);
    } catch (error) {
      console.error('Error loading knowledge base:', error);
    }
  }, [selectedAgent]);

  useEffect(() => {
    loadAgents();
  }, [loadAgents]);

  useEffect(() => {
    if (selectedAgent) {
      loadKnowledgeBase();
    }
  }, [selectedAgent, loadKnowledgeBase]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || !selectedAgent) return;

    setUploading(true);
    try {
      await api.uploadDocument(selectedAgent.id, file);
      await loadKnowledgeBase();
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Knowledge Base</h1>
        <p className="text-gray-600">Manage training documents and knowledge for your AI agents</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Agent Selection */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Select Agent</h2>
            <div className="space-y-2">
              {agents.map((agent) => (
                <button
                  key={agent.id}
                  onClick={() => setSelectedAgent(agent)}
                  className={`w-full text-left p-3 rounded-lg transition duration-200 ${
                    selectedAgent?.id === agent.id
                      ? 'bg-blue-100 text-blue-700 border border-blue-200'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <div className="font-medium">{agent.name}</div>
                  <div className="text-sm opacity-70">{agent.role}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Knowledge Management */}
        <div className="lg:col-span-3">
          {selectedAgent ? (
            <div className="bg-white rounded-xl shadow-sm border">
              <div className="p-6 border-b flex items-center justify-between">
                <h2 className="text-xl font-semibold text-gray-900">
                  Knowledge Base for {selectedAgent.name}
                </h2>
                <label className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 cursor-pointer flex items-center space-x-2 transition duration-200">
                  <Upload className="w-4 h-4" />
                  <span>{uploading ? 'Uploading...' : 'Upload Document'}</span>
                  <input
                    type="file"
                    onChange={handleFileUpload}
                    accept=".pdf,.txt,.doc,.docx"
                    className="hidden"
                    disabled={uploading}
                  />
                </label>
              </div>

              <div className="p-6">
                {knowledgeItems.length === 0 ? (
                  <div className="text-center py-12">
                    <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No knowledge items yet</h3>
                    <p className="text-gray-500 mb-6">Upload documents to train your agent</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {knowledgeItems.map((item) => (
                      <div key={item.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-medium text-gray-900">{item.title}</h3>
                          <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                            {item.source_type}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 line-clamp-3">
                          {item.content.substring(0, 200)}...
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-sm border p-12 text-center">
              <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Select an agent</h3>
              <p className="text-gray-500">Choose an agent to manage its knowledge base</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default KnowledgeBase;
