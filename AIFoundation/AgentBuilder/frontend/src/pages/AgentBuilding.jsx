import React, { useState, useRef } from 'react';
import { 
  Bot, 
  Plus, 
  Search, 
  Filter,
  Copy,
  Archive,
  GitBranch,
  Settings,
  Trash2,
  Play,
  Pause,
  Edit3,
  Save,
  X,
  ChevronDown,
  Move,
  MessageSquare,
  Users,
  CreditCard,
  Calendar,
  Mail,
  Phone,
  ShoppingCart,
  FileText,
  Heart,
  Zap
} from 'lucide-react';
import templateService from '../services/templateService';

const AgentBuilder = () => {
  const [agents, setAgents] = useState([
    {
      id: 1,
      name: "Billing Specialist",
      template: "billing-specialist",
      status: "active",
      persona: "Professional & Detail-oriented",
      tone: "Formal",
      version: "v1.2",
      created: "2025-01-15",
      conversations: 1247,
      successRate: 94
    },
    {
      id: 2,
      name: "Appointment Scheduler",
      template: "appointment-scheduler",
      status: "paused",
      persona: "Friendly & Efficient",
      tone: "Casual",
      version: "v2.0",
      created: "2025-01-10",
      conversations: 892,
      successRate: 98
    },
    {
      id: 3,
      name: "Insurance Verification",
      template: "insurance-verifier",
      status: "active",
      persona: "Thorough & Knowledgeable",
      tone: "Professional",
      version: "v1.0",
      created: "2025-01-20",
      conversations: 543,
      successRate: 87
    }
  ]);

  const [selectedAgent, setSelectedAgent] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [draggedTemplate, setDraggedTemplate] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  // Get templates from centralized service
  const agentTemplates = templateService.getAgentTemplates();

  // Get persona and tone options from centralized service
  const personaOptions = templateService.getPersonaOptions();
  const toneOptions = templateService.getToneOptions();

  // Get integration options from centralized service
  const integrationOptions = templateService.getIntegrationOptions();

  const [newAgent, setNewAgent] = useState({
    name: '',
    template: '',
    persona: '',
    tone: '',
    scope: '',
    customInstructions: '',
    ehrIntegration: 'none',
    clearingHouse: 'none',
    ePrescription: 'none',
    accountingSystem: 'none',
    mobileIntegration: 'none'
  });

  const filteredAgents = agents.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || agent.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const handleDragStart = (e, template) => {
    setDraggedTemplate(template);
    e.dataTransfer.effectAllowed = 'copy';
    e.dataTransfer.setData('text/plain', template.id);
    
    // Create drag image
    const dragImage = e.target.cloneNode(true);
    dragImage.style.transform = 'rotate(5deg)';
    dragImage.style.opacity = '0.8';
    document.body.appendChild(dragImage);
    e.dataTransfer.setDragImage(dragImage, 50, 50);
    setTimeout(() => document.body.removeChild(dragImage), 0);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    // Only set dragOver to false if we're actually leaving the drop zone
    if (!e.currentTarget.contains(e.relatedTarget)) {
      setIsDragOver(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    if (draggedTemplate) {
      setNewAgent({
        ...newAgent,
        name: draggedTemplate.name,
        template: draggedTemplate.id,
        persona: draggedTemplate.defaultPersona,
        tone: draggedTemplate.defaultTone
      });
      setShowCreateModal(true);
      setDraggedTemplate(null);
    }
  };

  const createAgent = () => {
    if (newAgent.name && newAgent.template) {
      const template = agentTemplates.find(t => t.id === newAgent.template);
      const agent = {
        id: agents.length + 1,
        name: newAgent.name,
        template: newAgent.template,
        status: 'active',
        persona: newAgent.persona || template.defaultPersona,
        tone: newAgent.tone || template.defaultTone,
        version: 'v1.0',
        created: new Date().toISOString().split('T')[0],
        conversations: 0,
        successRate: 0,
        scope: newAgent.scope,
        customInstructions: newAgent.customInstructions
      };
      setAgents([...agents, agent]);
      setNewAgent({ name: '', template: '', persona: '', tone: '', scope: '', customInstructions: '', ehrIntegration: 'none', clearingHouse: 'none', ePrescription: 'none', accountingSystem: 'none', mobileIntegration: 'none' });
      setShowCreateModal(false);
    }
  };

  const cloneAgent = (agent) => {
    const cloned = {
      ...agent,
      id: agents.length + 1,
      name: `${agent.name} (Copy)`,
      version: 'v1.0',
      created: new Date().toISOString().split('T')[0],
      conversations: 0,
      successRate: 0
    };
    setAgents([...agents, cloned]);
  };

  const toggleAgentStatus = (id) => {
    setAgents(agents.map(agent => 
      agent.id === id 
        ? { ...agent, status: agent.status === 'active' ? 'paused' : 'active' }
        : agent
    ));
  };

  const archiveAgent = (id) => {
    setAgents(agents.map(agent => 
      agent.id === id 
        ? { ...agent, status: 'archived' }
        : agent
    ));
  };

  const deleteAgent = (id) => {
    setAgents(agents.filter(agent => agent.id !== id));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Bot className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">AI Agent Builder</h1>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Create Agent</span>
          </button>
        </div>
      </div>

      <div className="flex">
        {/* Sidebar - Templates */}
        <div className="w-80 bg-white border-r border-gray-200 h-screen overflow-y-auto">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Agent Templates</h2>
            <p className="text-sm text-gray-600 mb-6">Drag templates to create new agents</p>
            
            <div className="space-y-4">
              {agentTemplates.map((template) => (
                <div
                  key={template.id}
                  draggable
                  onDragStart={(e) => handleDragStart(e, template)}
                  className="p-4 border border-gray-200 rounded-lg cursor-move hover:border-blue-300 hover:shadow-md transition-all bg-white select-none active:scale-105"
                >
                  <div className="flex items-start space-x-3">
                    <div className="bg-blue-100 p-2 rounded-lg">
                      <span className="text-2xl">{template.icon}</span>
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900">{template.name}</h3>
                      <p className="text-sm text-gray-600 mt-1">{template.description}</p>
                      <div className="flex items-center space-x-2 mt-2">
                        <span className="text-xs bg-gray-100 px-2 py-1 rounded capitalize">{template.category.replace('_', ' ')}</span>
                        <span className={`text-xs px-2 py-1 rounded ${
                          template.complexity === 'beginner' ? 'bg-green-100 text-green-800' :
                          template.complexity === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {template.complexity}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 p-6">
          {/* Search and Filters */}
          <div className="mb-6 flex items-center space-x-4">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search agents..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div className="relative">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="paused">Paused</option>
                <option value="archived">Archived</option>
              </select>
              <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            </div>
          </div>

          {/* Drop Zone */}
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`mb-6 border-2 border-dashed rounded-lg p-12 text-center transition-all duration-200 ${
              isDragOver 
                ? 'border-blue-400 bg-blue-50 scale-105' 
                : 'border-gray-300 hover:border-blue-400'
            }`}
          >
            <Bot className={`w-16 h-16 mx-auto mb-4 transition-all duration-200 ${
              isDragOver ? 'text-blue-500 scale-110' : 'text-gray-400'
            }`} />
            <p className={`transition-colors duration-200 ${
              isDragOver ? 'text-blue-600 font-medium' : 'text-gray-600'
            }`}>
              {isDragOver ? 'Release to create agent' : 'Drop a template here to create a new agent'}
            </p>
            {isDragOver && (
              <div className="mt-4">
                <div className="inline-flex items-center px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium">
                  <Plus className="w-4 h-4 mr-2" />
                  Creating {draggedTemplate?.name}
                </div>
              </div>
            )}
          </div>

          {/* Agents Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredAgents.map((agent) => {
              const template = agentTemplates.find(t => t.id === agent.template);
              
              return (
                <div key={agent.id} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                  <div className="p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <div className={`p-2 rounded-lg ${
                          agent.status === 'active' ? 'bg-green-100' : 
                          agent.status === 'paused' ? 'bg-yellow-100' : 'bg-gray-100'
                        }`}>
                          <span className={`text-2xl ${
                            agent.status === 'active' ? 'text-green-600' : 
                            agent.status === 'paused' ? 'text-yellow-600' : 'text-gray-600'
                          }`}>
                            {template?.icon || '🤖'}
                          </span>
                        </div>
                        <div>
                          <h3 className="font-semibold text-gray-900">{agent.name}</h3>
                          <p className="text-sm text-gray-600">{agent.version}</p>
                        </div>
                      </div>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        agent.status === 'active' ? 'bg-green-100 text-green-800' :
                        agent.status === 'paused' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {agent.status}
                      </span>
                    </div>

                    <div className="space-y-2 mb-4">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Persona:</span>
                        <span className="text-gray-900">{agent.persona}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Tone:</span>
                        <span className="text-gray-900">{agent.tone}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Conversations:</span>
                        <span className="text-gray-900">{agent.conversations.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">Success Rate:</span>
                        <span className="text-gray-900">{agent.successRate}%</span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => toggleAgentStatus(agent.id)}
                        className={`p-2 rounded-lg transition-colors ${
                          agent.status === 'active' 
                            ? 'bg-yellow-100 text-yellow-600 hover:bg-yellow-200' 
                            : 'bg-green-100 text-green-600 hover:bg-green-200'
                        }`}
                        title={agent.status === 'active' ? 'Pause Agent' : 'Activate Agent'}
                      >
                        {agent.status === 'active' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                      </button>
                      
                      <button
                        onClick={() => setSelectedAgent(agent)}
                        className="p-2 bg-blue-100 text-blue-600 rounded-lg hover:bg-blue-200 transition-colors"
                        title="Edit Agent"
                      >
                        <Edit3 className="w-4 h-4" />
                      </button>
                      
                      <button
                        onClick={() => cloneAgent(agent)}
                        className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
                        title="Clone Agent"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                      
                      <button
                        onClick={() => archiveAgent(agent.id)}
                        className="p-2 bg-orange-100 text-orange-600 rounded-lg hover:bg-orange-200 transition-colors"
                        title="Archive Agent"
                      >
                        <Archive className="w-4 h-4" />
                      </button>
                      
                      <button
                        className="p-2 bg-purple-100 text-purple-600 rounded-lg hover:bg-purple-200 transition-colors"
                        title="Version Control"
                      >
                        <GitBranch className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Create Agent Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Create New Agent</h2>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Agent Name</label>
                <input
                  type="text"
                  value={newAgent.name}
                  onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter agent name..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Template</label>
                <select
                  value={newAgent.template}
                  onChange={(e) => {
                    const template = agentTemplates.find(t => t.id === e.target.value);
                    setNewAgent({
                      ...newAgent,
                      template: e.target.value,
                      persona: template?.defaultPersona || '',
                      tone: template?.defaultTone || ''
                    });
                  }}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Select a template...</option>
                  {agentTemplates.map(template => (
                    <option key={template.id} value={template.id}>{template.name}</option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Persona</label>
                  <select
                    value={newAgent.persona}
                    onChange={(e) => setNewAgent({ ...newAgent, persona: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select persona...</option>
                    {personaOptions.map(persona => (
                      <option key={persona} value={persona}>{persona}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Tone</label>
                  <select
                    value={newAgent.tone}
                    onChange={(e) => setNewAgent({ ...newAgent, tone: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select tone...</option>
                    {toneOptions.map(tone => (
                      <option key={tone} value={tone}>{tone}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Scope of Interaction</label>
                <textarea
                  value={newAgent.scope}
                  onChange={(e) => setNewAgent({ ...newAgent, scope: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows="3"
                  placeholder="Define what this agent should and shouldn't handle..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Custom Instructions</label>
                <textarea
                  value={newAgent.customInstructions}
                  onChange={(e) => setNewAgent({ ...newAgent, customInstructions: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows="4"
                  placeholder="Add any specific instructions or behaviors..."
                />
              </div>

              {/* Integration Settings */}
              <div className="border-t border-gray-200 pt-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">System Integrations</h3>
                <p className="text-sm text-gray-600 mb-4">Configure which systems this agent can integrate with</p>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">EHR Integration</label>
                    <select
                      value={newAgent.ehrIntegration}
                      onChange={(e) => setNewAgent({ ...newAgent, ehrIntegration: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      {integrationOptions.ehrIntegration.map(option => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Clearing House</label>
                    <select
                      value={newAgent.clearingHouse}
                      onChange={(e) => setNewAgent({ ...newAgent, clearingHouse: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      {integrationOptions.clearingHouse.map(option => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">E-Prescription</label>
                    <select
                      value={newAgent.ePrescription}
                      onChange={(e) => setNewAgent({ ...newAgent, ePrescription: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      {integrationOptions.ePrescription.map(option => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Accounting System</label>
                    <select
                      value={newAgent.accountingSystem}
                      onChange={(e) => setNewAgent({ ...newAgent, accountingSystem: e.target.value })}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      {integrationOptions.accountingSystem.map(option => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                  </div>

                  {/* Mobile Integration - Only show for non-billing agents */}
                  {newAgent.template && !newAgent.template.includes('billing') && (
                    <div className="col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">Mobile Integration</label>
                      <select
                        value={newAgent.mobileIntegration}
                        onChange={(e) => setNewAgent({ ...newAgent, mobileIntegration: e.target.value })}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        {integrationOptions.mobileIntegration.map(option => (
                          <option key={option.value} value={option.value}>{option.label}</option>
                        ))}
                      </select>
                      {newAgent.mobileIntegration !== 'none' && (
                        <p className="text-xs text-gray-500 mt-1">
                          Access fitness data including steps, heart rate, sleep, workouts, and health metrics from mobile devices
                        </p>
                      )}
                    </div>
                  )}
                </div>

                {/* Integration Summary */}
                {(newAgent.ehrIntegration !== 'none' || newAgent.clearingHouse !== 'none' || newAgent.ePrescription !== 'none' || newAgent.accountingSystem !== 'none' || (newAgent.mobileIntegration !== 'none' && newAgent.template !== 'billing')) && (
                  <div className="mt-4 p-4 bg-green-50 rounded-lg">
                    <h4 className="font-medium text-green-900 mb-2">Active Integrations</h4>
                    <div className="flex flex-wrap gap-2">
                      {newAgent.ehrIntegration !== 'none' && (
                        <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                          EHR: {integrationOptions.ehrIntegration.find(opt => opt.value === newAgent.ehrIntegration)?.label}
                        </span>
                      )}
                      {newAgent.clearingHouse !== 'none' && (
                        <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                          Clearing House: {integrationOptions.clearingHouse.find(opt => opt.value === newAgent.clearingHouse)?.label}
                        </span>
                      )}
                      {newAgent.ePrescription !== 'none' && (
                        <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                          E-Prescription: {integrationOptions.ePrescription.find(opt => opt.value === newAgent.ePrescription)?.label}
                        </span>
                      )}
                      {newAgent.accountingSystem !== 'none' && (
                        <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                          Accounting: {integrationOptions.accountingSystem.find(opt => opt.value === newAgent.accountingSystem)?.label}
                        </span>
                      )}
                      {newAgent.mobileIntegration !== 'none' && !newAgent.template.includes('billing') && (
                        <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                          📱 Mobile: {integrationOptions.mobileIntegration.find(opt => opt.value === newAgent.mobileIntegration)?.label}
                        </span>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {newAgent.template && (
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="font-medium text-blue-900 mb-2">Template Features</h3>
                  <div className="flex flex-wrap gap-2">
                    {agentTemplates.find(t => t.id === newAgent.template)?.features.map(feature => (
                      <span key={feature} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="flex items-center justify-end space-x-4 mt-8">
              <button
                onClick={() => setShowCreateModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={createAgent}
                disabled={!newAgent.name || !newAgent.template}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
              >
                <Save className="w-4 h-4" />
                <span>Create Agent</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit Agent Modal (simplified for this prototype) */}
      {selectedAgent && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Edit Agent</h2>
              <button
                onClick={() => setSelectedAgent(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <p className="text-gray-600 mb-4">Editing: {selectedAgent.name}</p>
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => setSelectedAgent(null)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Close
              </button>
              <button
                onClick={() => {
                  // Save changes logic would go here
                  setSelectedAgent(null);
                }}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AgentBuilder;