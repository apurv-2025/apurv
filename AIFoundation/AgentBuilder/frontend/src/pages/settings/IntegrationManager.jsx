import React, { useState, useEffect } from 'react';
import { 
  Settings, 
  Plus, 
  Search, 
  Filter,
  CheckCircle,
  AlertTriangle,
  X,
  Edit3,
  Trash2,
  Play,
  Pause,
  RefreshCw,
  Database,
  Cloud,
  Key,
  Shield,
  Activity,
  Clock,
  Users,
  CreditCard,
  Mail,
  Phone,
  Calendar,
  FileText,
  Globe,
  Server,
  Zap,
  AlertCircle,
  Save,
  Eye,
  EyeOff,
  Copy,
  Download,
  Upload,
  Link
} from 'lucide-react';

const SystemIntegrationsManager = () => {
  const [selectedIntegration, setSelectedIntegration] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showConfigModal, setShowConfigModal] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [showApiKey, setShowApiKey] = useState({});

  // Integration categories and systems
  const integrationCategories = {
    ehr: {
      name: 'Electronic Health Records',
      icon: Database,
      color: 'blue',
      systems: [
        { id: 'epic', name: 'Epic', description: 'Epic EHR System Integration', popularity: 95 },
        { id: 'cerner', name: 'Cerner (Oracle Health)', description: 'Cerner EHR Platform', popularity: 88 },
        { id: 'allscripts', name: 'Allscripts', description: 'Allscripts EHR Solution', popularity: 72 },
        { id: 'athenahealth', name: 'athenahealth', description: 'athenahealth EHR Platform', popularity: 85 },
        { id: 'eclinicalworks', name: 'eClinicalWorks', description: 'eClinicalWorks EHR', popularity: 68 },
        { id: 'nextgen', name: 'NextGen Healthcare', description: 'NextGen EHR System', popularity: 65 }
      ]
    },
    billing: {
      name: 'Billing & Payment Systems',
      icon: CreditCard,
      color: 'green',
      systems: [
        { id: 'change_healthcare', name: 'Change Healthcare', description: 'Revenue Cycle Management', popularity: 92 },
        { id: 'availity', name: 'Availity', description: 'Healthcare Administrative Solutions', popularity: 89 },
        { id: 'relay_health', name: 'Relay Health', description: 'Claims Processing Platform', popularity: 78 },
        { id: 'waystar', name: 'Waystar', description: 'Revenue Cycle Technology', popularity: 82 },
        { id: 'navicure', name: 'Navicure', description: 'Practice Management Solutions', popularity: 71 }
      ]
    },
    communication: {
      name: 'Communication Systems',
      icon: Mail,
      color: 'purple',
      systems: [
        { id: 'twilio', name: 'Twilio', description: 'SMS and Voice Communications', popularity: 94 },
        { id: 'sendgrid', name: 'SendGrid', description: 'Email Delivery Service', popularity: 87 },
        { id: 'mailchimp', name: 'Mailchimp', description: 'Email Marketing Platform', popularity: 83 },
        { id: 'slack', name: 'Slack', description: 'Team Communication', popularity: 91 },
        { id: 'microsoft_teams', name: 'Microsoft Teams', description: 'Collaboration Platform', popularity: 89 }
      ]
    },
    scheduling: {
      name: 'Scheduling & Calendar',
      icon: Calendar,
      color: 'orange',
      systems: [
        { id: 'google_calendar', name: 'Google Calendar', description: 'Calendar Integration', popularity: 96 },
        { id: 'outlook_calendar', name: 'Outlook Calendar', description: 'Microsoft Calendar', popularity: 94 },
        { id: 'calendly', name: 'Calendly', description: 'Appointment Scheduling', popularity: 88 },
        { id: 'acuity_scheduling', name: 'Acuity Scheduling', description: 'Online Scheduling', popularity: 79 },
        { id: 'square_appointments', name: 'Square Appointments', description: 'Appointment Management', popularity: 75 }
      ]
    },
    analytics: {
      name: 'Analytics & Reporting',
      icon: Activity,
      color: 'indigo',
      systems: [
        { id: 'tableau', name: 'Tableau', description: 'Data Visualization Platform', popularity: 91 },
        { id: 'power_bi', name: 'Power BI', description: 'Microsoft Business Intelligence', popularity: 88 },
        { id: 'google_analytics', name: 'Google Analytics', description: 'Web Analytics', popularity: 95 },
        { id: 'mixpanel', name: 'Mixpanel', description: 'Product Analytics', popularity: 82 },
        { id: 'amplitude', name: 'Amplitude', description: 'Digital Analytics', popularity: 79 }
      ]
    }
  };

  // Mock configured integrations
  const [integrations, setIntegrations] = useState([
    {
      id: 1,
      systemId: 'epic',
      name: 'Epic EHR - Main Campus',
      category: 'ehr',
      status: 'active',
      lastSync: '2025-01-28 11:15 AM',
      health: 'healthy',
      apiCalls: 15420,
      errorRate: 0.2,
      config: {
        endpoint: 'https://api.epic.myhealth.org',
        apiKey: 'epk_test_5Fo02kCJNDsjfksdj',
        environment: 'production',
        version: 'R4',
        timeout: 30000,
        retries: 3,
        dataSync: {
          patients: true,
          appointments: true,
          medications: true,
          allergies: true,
          vitals: false
        }
      },
      authentication: {
        type: 'oauth2',
        clientId: 'epic_client_123',
        scope: 'patient/*.read patient/*.write'
      }
    },
    {
      id: 2,
      systemId: 'change_healthcare',
      name: 'Change Healthcare - Claims',
      category: 'billing',
      status: 'active',
      lastSync: '2025-01-28 11:10 AM',
      health: 'healthy',
      apiCalls: 8934,
      errorRate: 1.8,
      config: {
        endpoint: 'https://api.changehealthcare.com',
        apiKey: 'chc_prod_kj3h4k5j6l7m8n9o',
        environment: 'production',
        timeout: 45000,
        retries: 5,
        features: {
          eligibility: true,
          claims: true,
          prior_auth: true,
          remittance: true
        }
      },
      authentication: {
        type: 'api_key',
        keyLocation: 'header'
      }
    },
    {
      id: 3,
      systemId: 'twilio',
      name: 'Twilio Communications',
      category: 'communication',
      status: 'warning',
      lastSync: '2025-01-28 10:45 AM',
      health: 'degraded',
      apiCalls: 3421,
      errorRate: 5.2,
      config: {
        endpoint: 'https://api.twilio.com',
        accountSid: 'AC1234567890abcdef',
        authToken: 'your_auth_token_here',
        phoneNumber: '+15551234567',
        features: {
          sms: true,
          voice: true,
          whatsapp: false,
          email: false
        }
      },
      authentication: {
        type: 'basic_auth',
        username: 'account_sid',
        password: 'auth_token'
      }
    }
  ]);

  const [newIntegration, setNewIntegration] = useState({
    systemId: '',
    name: '',
    category: '',
    environment: 'sandbox',
    config: {}
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'inactive': return 'text-gray-600 bg-gray-100';
      case 'warning': return 'text-yellow-600 bg-yellow-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getHealthColor = (health) => {
    switch (health) {
      case 'healthy': return 'text-green-600';
      case 'degraded': return 'text-yellow-600';
      case 'unhealthy': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getCategoryIcon = (category) => {
    return integrationCategories[category]?.icon || Settings;
  };

  const filteredIntegrations = integrations.filter(integration => {
    const matchesSearch = integration.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || integration.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const testConnection = async (integrationId) => {
    // Mock API call to test connection
    const integration = integrations.find(i => i.id === integrationId);
    console.log('Testing connection for:', integration.name);
    
    // Simulate API call delay
    setTimeout(() => {
      alert(`Connection test ${Math.random() > 0.2 ? 'successful' : 'failed'} for ${integration.name}`);
    }, 2000);
  };

  const toggleIntegration = (integrationId) => {
    setIntegrations(integrations.map(integration => 
      integration.id === integrationId 
        ? { ...integration, status: integration.status === 'active' ? 'inactive' : 'active' }
        : integration
    ));
  };

  const deleteIntegration = (integrationId) => {
    setShowDeleteConfirm(integrationId);
  };

  const confirmDelete = () => {
    if (showDeleteConfirm) {
      setIntegrations(integrations.filter(integration => integration.id !== showDeleteConfirm));
      setShowDeleteConfirm(null);
    }
  };

  const addIntegration = () => {
    const selectedSystem = Object.values(integrationCategories)
      .flatMap(cat => cat.systems)
      .find(sys => sys.id === newIntegration.systemId);

    if (selectedSystem) {
      const integration = {
        id: integrations.length + 1,
        ...newIntegration,
        name: newIntegration.name || selectedSystem.name,
        status: 'inactive',
        lastSync: 'Never',
        health: 'unknown',
        apiCalls: 0,
        errorRate: 0,
        config: {
          ...newIntegration.config,
          environment: newIntegration.environment
        }
      };
      
      setIntegrations([...integrations, integration]);
      setNewIntegration({ systemId: '', name: '', category: '', environment: 'sandbox', config: {} });
      setShowAddModal(false);
    }
  };

  const toggleApiKeyVisibility = (integrationId) => {
    setShowApiKey(prev => ({
      ...prev,
      [integrationId]: !prev[integrationId]
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Settings className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">System Integrations</h1>
              <p className="text-gray-600">Configure and manage all system integrations</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setShowAddModal(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              <span>Add Integration</span>
            </button>
            <button className="bg-gray-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-gray-700 transition-colors">
              <RefreshCw className="w-4 h-4" />
              <span>Sync All</span>
            </button>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center space-x-4">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Search integrations..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg w-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="warning">Warning</option>
            <option value="error">Error</option>
          </select>
        </div>
      </div>

      <div className="p-6">
        {/* Integration Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Integrations</p>
                <p className="text-2xl font-bold text-gray-900">{integrations.length}</p>
              </div>
              <Settings className="w-8 h-8 text-blue-600" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Active</p>
                <p className="text-2xl font-bold text-green-600">
                  {integrations.filter(i => i.status === 'active').length}
                </p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Warnings</p>
                <p className="text-2xl font-bold text-yellow-600">
                  {integrations.filter(i => i.status === 'warning').length}
                </p>
              </div>
              <AlertTriangle className="w-8 h-8 text-yellow-600" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total API Calls</p>
                <p className="text-2xl font-bold text-purple-600">
                  {integrations.reduce((sum, i) => sum + i.apiCalls, 0).toLocaleString()}
                </p>
              </div>
              <Activity className="w-8 h-8 text-purple-600" />
            </div>
          </div>
        </div>

        {/* Integrations List */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Configured Integrations</h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Integration</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Health</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Last Sync</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">API Calls</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredIntegrations.map((integration) => {
                  const IconComponent = getCategoryIcon(integration.category);
                  return (
                    <tr key={integration.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className={`p-2 rounded-lg bg-${integrationCategories[integration.category]?.color}-100 mr-3`}>
                            <IconComponent className={`w-5 h-5 text-${integrationCategories[integration.category]?.color}-600`} />
                          </div>
                          <div>
                            <div className="text-sm font-medium text-gray-900">{integration.name}</div>
                            <div className="text-sm text-gray-500">{integration.config?.endpoint}</div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm text-gray-900 capitalize">
                          {integrationCategories[integration.category]?.name}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(integration.status)}`}>
                          {integration.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className={`w-2 h-2 rounded-full mr-2 ${
                            integration.health === 'healthy' ? 'bg-green-400' :
                            integration.health === 'degraded' ? 'bg-yellow-400' : 'bg-red-400'
                          }`}></div>
                          <span className={`text-sm ${getHealthColor(integration.health)}`}>
                            {integration.health}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {integration.lastSync}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{integration.apiCalls.toLocaleString()}</div>
                        <div className="text-sm text-gray-500">{integration.errorRate}% error rate</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => setSelectedIntegration(integration)}
                            className="text-blue-600 hover:text-blue-900"
                            title="Configure"
                          >
                            <Edit3 className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => toggleIntegration(integration.id)}
                            className={`${integration.status === 'active' ? 'text-yellow-600 hover:text-yellow-900' : 'text-green-600 hover:text-green-900'}`}
                            title={integration.status === 'active' ? 'Pause' : 'Activate'}
                          >
                            {integration.status === 'active' ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                          </button>
                          <button
                            onClick={() => testConnection(integration.id)}
                            className="text-purple-600 hover:text-purple-900"
                            title="Test Connection"
                          >
                            <Zap className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => deleteIntegration(integration.id)}
                            className="text-red-600 hover:text-red-900"
                            title="Delete"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Add Integration Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Add New Integration</h2>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="space-y-6">
              {Object.entries(integrationCategories).map(([categoryKey, category]) => {
                const IconComponent = category.icon;
                return (
                  <div key={categoryKey} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center space-x-3 mb-4">
                      <div className={`p-2 rounded-lg bg-${category.color}-100`}>
                        <IconComponent className={`w-5 h-5 text-${category.color}-600`} />
                      </div>
                      <h3 className="text-lg font-medium text-gray-900">{category.name}</h3>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                      {category.systems.map((system) => (
                        <div
                          key={system.id}
                          onClick={() => setNewIntegration({
                            ...newIntegration,
                            systemId: system.id,
                            category: categoryKey,
                            name: system.name
                          })}
                          className={`p-3 border rounded-lg cursor-pointer transition-all ${
                            newIntegration.systemId === system.id
                              ? 'border-blue-300 bg-blue-50'
                              : 'border-gray-200 hover:border-blue-200 hover:bg-gray-50'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div>
                              <h4 className="font-medium text-gray-900">{system.name}</h4>
                              <p className="text-sm text-gray-600">{system.description}</p>
                              <div className="flex items-center space-x-2 mt-1">
                                <div className="w-16 bg-gray-200 rounded-full h-1">
                                  <div 
                                    className="bg-blue-600 h-1 rounded-full" 
                                    style={{ width: `${system.popularity}%` }}
                                  ></div>
                                </div>
                                <span className="text-xs text-gray-500">{system.popularity}%</span>
                              </div>
                            </div>
                            {newIntegration.systemId === system.id && (
                              <CheckCircle className="w-5 h-5 text-blue-600" />
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>

            {newIntegration.systemId && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-4">Configuration</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Integration Name</label>
                    <input
                      type="text"
                      value={newIntegration.name}
                      onChange={(e) => setNewIntegration({...newIntegration, name: e.target.value})}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Enter custom name..."
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Environment</label>
                    <select
                      value={newIntegration.environment}
                      onChange={(e) => setNewIntegration({...newIntegration, environment: e.target.value})}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="sandbox">Sandbox</option>
                      <option value="staging">Staging</option>
                      <option value="production">Production</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            <div className="flex items-center justify-end space-x-4 mt-8">
              <button
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={addIntegration}
                disabled={!newIntegration.systemId}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
              >
                Add Integration
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Configuration Modal */}
      {selectedIntegration && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Configure {selectedIntegration.name}</h2>
              <button
                onClick={() => setSelectedIntegration(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="space-y-6">
              {/* Basic Settings */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Basic Settings</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Integration Name</label>
                    <input
                      type="text"
                      value={selectedIntegration.name}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Environment</label>
                    <select
                      value={selectedIntegration.config?.environment || 'production'}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="sandbox">Sandbox</option>
                      <option value="staging">Staging</option>
                      <option value="production">Production</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Connection Settings */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Connection Settings</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">API Endpoint</label>
                    <input
                      type="url"
                      value={selectedIntegration.config?.endpoint || ''}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="https://api.example.com"
                    />
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Timeout (ms)</label>
                      <input
                        type="number"
                        value={selectedIntegration.config?.timeout || 30000}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Retry Attempts</label>
                      <input
                        type="number"
                        value={selectedIntegration.config?.retries || 3}
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Authentication */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Authentication</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Authentication Type</label>
                    <select
                      value={selectedIntegration.authentication?.type || 'api_key'}
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="api_key">API Key</option>
                      <option value="oauth2">OAuth 2.0</option>
                      <option value="basic_auth">Basic Authentication</option>
                      <option value="bearer_token">Bearer Token</option>
                    </select>
                  </div>

                  {selectedIntegration.authentication?.type === 'api_key' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">API Key</label>
                      <div className="relative">
                        <input
                          type={showApiKey[selectedIntegration.id] ? 'text' : 'password'}
                          value={selectedIntegration.config?.apiKey || ''}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 pr-20 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Enter API key..."
                        />
                        <div className="absolute inset-y-0 right-0 flex items-center space-x-2 pr-3">
                          <button
                            onClick={() => toggleApiKeyVisibility(selectedIntegration.id)}
                            className="text-gray-400 hover:text-gray-600"
                          >
                            {showApiKey[selectedIntegration.id] ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                          </button>
                          <button
                            onClick={() => navigator.clipboard.writeText(selectedIntegration.config?.apiKey || '')}
                            className="text-gray-400 hover:text-gray-600"
                          >
                            <Copy className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  )}

                  {selectedIntegration.authentication?.type === 'oauth2' && (
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Client ID</label>
                        <input
                          type="text"
                          value={selectedIntegration.authentication?.clientId || ''}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Scope</label>
                        <input
                          type="text"
                          value={selectedIntegration.authentication?.scope || ''}
                          className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="read write"
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Data Sync Settings */}
              {selectedIntegration.category === 'ehr' && selectedIntegration.config?.dataSync && (
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Data Synchronization</h3>
                  <div className="grid grid-cols-2 gap-4">
                    {Object.entries(selectedIntegration.config.dataSync).map(([key, enabled]) => (
                      <label key={key} className="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          checked={enabled}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="text-sm text-gray-700 capitalize">{key.replace('_', ' ')}</span>
                      </label>
                    ))}
                  </div>
                </div>
              )}

              {/* Feature Settings */}
              {selectedIntegration.config?.features && (
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Features</h3>
                  <div className="grid grid-cols-2 gap-4">
                    {Object.entries(selectedIntegration.config.features).map(([key, enabled]) => (
                      <label key={key} className="flex items-center space-x-3">
                        <input
                          type="checkbox"
                          checked={enabled}
                          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        />
                        <span className="text-sm text-gray-700 capitalize">{key.replace('_', ' ')}</span>
                      </label>
                    ))}
                  </div>
                </div>
              )}

              {/* Health Check */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Health & Monitoring</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Current Status</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(selectedIntegration.status)}`}>
                        {selectedIntegration.status}
                      </span>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Health</span>
                      <span className={`text-sm font-medium ${getHealthColor(selectedIntegration.health)}`}>
                        {selectedIntegration.health}
                      </span>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Error Rate</span>
                      <span className="text-sm font-medium text-gray-900">{selectedIntegration.errorRate}%</span>
                    </div>
                  </div>
                </div>
                
                <div className="mt-4 flex space-x-4">
                  <button
                    onClick={() => testConnection(selectedIntegration.id)}
                    className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors flex items-center space-x-2"
                  >
                    <Zap className="w-4 h-4" />
                    <span>Test Connection</span>
                  </button>
                  <button className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors flex items-center space-x-2">
                    <RefreshCw className="w-4 h-4" />
                    <span>Force Sync</span>
                  </button>
                </div>
              </div>

              {/* Webhook Configuration */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Webhook Configuration</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Webhook URL</label>
                    <input
                      type="url"
                      placeholder="https://your-app.com/webhooks/integration"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Secret Key</label>
                      <input
                        type="password"
                        placeholder="webhook_secret_key"
                        className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Events</label>
                      <select className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option>All Events</option>
                        <option>Data Changes</option>
                        <option>Status Updates</option>
                        <option>Errors Only</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              {/* Rate Limiting */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-4">Rate Limiting</h3>
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Requests per Minute</label>
                    <input
                      type="number"
                      defaultValue="100"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Requests per Hour</label>
                    <input
                      type="number"
                      defaultValue="5000"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Daily Limit</label>
                    <input
                      type="number"
                      defaultValue="100000"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between mt-8 pt-6 border-t border-gray-200">
              <div className="flex space-x-4">
                <button className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors flex items-center space-x-2">
                  <Trash2 className="w-4 h-4" />
                  <span>Delete Integration</span>
                </button>
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => setSelectedIntegration(null)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                >
                  Cancel
                </button>
                <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2">
                  <Save className="w-4 h-4" />
                  <span>Save Configuration</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Confirm Deletion</h2>
              <button
                onClick={() => setShowDeleteConfirm(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="mb-6">
              <p className="text-gray-700">
                Are you sure you want to delete this integration? This action cannot be undone and will immediately stop all data synchronization.
              </p>
            </div>
            
            <div className="flex items-center justify-end space-x-4">
              <button
                onClick={() => setShowDeleteConfirm(null)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-colors flex items-center space-x-2"
              >
                <Trash2 className="w-4 h-4" />
                <span>Delete Integration</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SystemIntegrationsManager;