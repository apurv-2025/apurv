import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Eye, Search, Filter, RefreshCw } from 'lucide-react';

// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// API Service
const apiService = {
  // Claims
  getClaims: async (filters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });
    const response = await fetch(`${API_BASE_URL}/claims?${params}`);
    return response.json();
  },
  
  getClaim: async (id) => {
    const response = await fetch(`${API_BASE_URL}/claims/${id}`);
    return response.json();
  },
  
  createClaim: async (data) => {
    const response = await fetch(`${API_BASE_URL}/claims`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  updateClaim: async (id, data) => {
    const response = await fetch(`${API_BASE_URL}/claims/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  deleteClaim: async (id) => {
    const response = await fetch(`${API_BASE_URL}/claims/${id}`, {
      method: 'DELETE',
    });
    return response.json();
  },
  
  // Coverage
  getCoverages: async (filters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value);
    });
    const response = await fetch(`${API_BASE_URL}/coverages?${params}`);
    return response.json();
  },
  
  createCoverage: async (data) => {
    const response = await fetch(`${API_BASE_URL}/coverages`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
  
  // Stats
  getStats: async () => {
    const response = await fetch(`${API_BASE_URL}/stats/claims`);
    return response.json();
  }
};

// Status Badge Component
const StatusBadge = ({ status }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'draft': return 'bg-yellow-100 text-yellow-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      case 'entered-in-error': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(status)}`}>
      {status}
    </span>
  );
};

// Claim Form Component
const ClaimForm = ({ claim, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    status: claim?.status || 'draft',
    type: claim?.type || { text: 'Professional' },
    use: claim?.use || 'claim',
    patient_id: claim?.patient_id || '',
    insurer_id: claim?.insurer_id || '',
    provider_id: claim?.provider_id || '',
    insurance: claim?.insurance || [{ sequence: 1, focal: true, coverage: { reference: '' } }],
    total: claim?.total || { value: 0, currency: 'USD' },
    ...claim
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <h2 className="text-xl font-bold mb-4">
          {claim ? 'Edit Claim' : 'Create New Claim'}
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={formData.status}
                onChange={(e) => handleChange('status', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              >
                <option value="active">Active</option>
                <option value="draft">Draft</option>
                <option value="cancelled">Cancelled</option>
                <option value="entered-in-error">Entered in Error</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Use</label>
              <select
                value={formData.use}
                onChange={(e) => handleChange('use', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              >
                <option value="claim">Claim</option>
                <option value="preauthorization">Preauthorization</option>
                <option value="predetermination">Predetermination</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Patient ID</label>
            <input
              type="text"
              value={formData.patient_id}
              onChange={(e) => handleChange('patient_id', e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
              placeholder="Enter patient identifier"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Insurer ID</label>
            <input
              type="text"
              value={formData.insurer_id}
              onChange={(e) => handleChange('insurer_id', e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
              placeholder="Enter insurer identifier"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Provider ID</label>
            <input
              type="text"
              value={formData.provider_id}
              onChange={(e) => handleChange('provider_id', e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
              placeholder="Enter provider identifier"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Claim Type</label>
            <input
              type="text"
              value={formData.type?.text || ''}
              onChange={(e) => handleChange('type', { text: e.target.value })}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Professional, Institutional, Pharmacy"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Total Amount</label>
            <div className="flex gap-2">
              <input
                type="number"
                step="0.01"
                value={formData.total?.value || 0}
                onChange={(e) => handleChange('total', { 
                  ...formData.total, 
                  value: parseFloat(e.target.value) || 0 
                })}
                className="flex-1 p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="0.00"
              />
              <select
                value={formData.total?.currency || 'USD'}
                onChange={(e) => handleChange('total', { 
                  ...formData.total, 
                  currency: e.target.value 
                })}
                className="w-20 p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end space-x-2 pt-4">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              {claim ? 'Update' : 'Create'} Claim
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Coverage Form Component
const CoverageForm = ({ coverage, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    status: coverage?.status || 'active',
    kind: coverage?.kind || 'insurance',
    beneficiary_id: coverage?.beneficiary_id || '',
    insurer_id: coverage?.insurer_id || '',
    type: coverage?.type || { text: 'Medical' },
    ...coverage
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-2xl">
        <h2 className="text-xl font-bold mb-4">
          {coverage ? 'Edit Coverage' : 'Create New Coverage'}
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={formData.status}
                onChange={(e) => handleChange('status', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              >
                <option value="active">Active</option>
                <option value="cancelled">Cancelled</option>
                <option value="draft">Draft</option>
                <option value="entered-in-error">Entered in Error</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Kind</label>
              <select
                value={formData.kind}
                onChange={(e) => handleChange('kind', e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="insurance">Insurance</option>
                <option value="self-pay">Self Pay</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Beneficiary ID</label>
            <input
              type="text"
              value={formData.beneficiary_id}
              onChange={(e) => handleChange('beneficiary_id', e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
              placeholder="Enter beneficiary identifier"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Insurer ID</label>
            <input
              type="text"
              value={formData.insurer_id}
              onChange={(e) => handleChange('insurer_id', e.target.value)}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
              placeholder="Enter insurer identifier"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Coverage Type</label>
            <input
              type="text"
              value={formData.type?.text || ''}
              onChange={(e) => handleChange('type', { text: e.target.value })}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="e.g., Medical, Dental, Vision"
            />
          </div>

          <div className="flex justify-end space-x-2 pt-4">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              {coverage ? 'Update' : 'Create'} Coverage
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Main App Component
const FHIRClaimsApp = () => {
  const [activeTab, setActiveTab] = useState('claims');
  const [claims, setClaims] = useState([]);
  const [coverages, setCoverages] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(false);
  const [showClaimForm, setShowClaimForm] = useState(false);
  const [showCoverageForm, setShowCoverageForm] = useState(false);
  const [editingClaim, setEditingClaim] = useState(null);
  const [editingCoverage, setEditingCoverage] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  // Load data on mount and tab change
  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'claims') {
        const claimsData = await apiService.getClaims({ status: statusFilter });
        setClaims(claimsData);
      } else if (activeTab === 'coverage') {
        const coverageData = await apiService.getCoverages({ status: statusFilter });
        setCoverages(coverageData);
      } else if (activeTab === 'dashboard') {
        const statsData = await apiService.getStats();
        setStats(statsData);
        const claimsData = await apiService.getClaims({ limit: 5 });
        setClaims(claimsData);
      }
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateClaim = async (claimData) => {
    try {
      await apiService.createClaim(claimData);
      setShowClaimForm(false);
      loadData();
    } catch (error) {
      console.error('Error creating claim:', error);
    }
  };

  const handleUpdateClaim = async (claimData) => {
    try {
      await apiService.updateClaim(editingClaim.id, claimData);
      setEditingClaim(null);
      setShowClaimForm(false);
      loadData();
    } catch (error) {
      console.error('Error updating claim:', error);
    }
  };

  const handleDeleteClaim = async (claimId) => {
    if (window.confirm('Are you sure you want to delete this claim?')) {
      try {
        await apiService.deleteClaim(claimId);
        loadData();
      } catch (error) {
        console.error('Error deleting claim:', error);
      }
    }
  };

  const handleCreateCoverage = async (coverageData) => {
    try {
      await apiService.createCoverage(coverageData);
      setShowCoverageForm(false);
      loadData();
    } catch (error) {
      console.error('Error creating coverage:', error);
    }
  };

  const filteredClaims = claims.filter(claim =>
    claim.patient_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    claim.id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    claim.provider_id?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const filteredCoverages = coverages.filter(coverage =>
    coverage.beneficiary_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    coverage.id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    coverage.insurer_id?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">FHIR Claims Management</h1>
              <p className="text-gray-600">Manage healthcare claims and coverage</p>
            </div>
            <button
              onClick={loadData}
              className="flex items-center px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </button>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {['dashboard', 'claims', 'coverage'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`py-4 px-1 border-b-2 font-medium text-sm capitalize ${
                  activeTab === tab
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            {/* Dashboard Tab */}
            {activeTab === 'dashboard' && (
              <div className="space-y-6">
                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  {Object.entries(stats).map(([key, value]) => (
                    <div key={key} className="bg-white overflow-hidden shadow rounded-lg">
                      <div className="p-5">
                        <div className="flex items-center">
                          <div className="flex-shrink-0">
                            <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                              <span className="text-white font-bold text-sm">{value}</span>
                            </div>
                          </div>
                          <div className="ml-5 w-0 flex-1">
                            <dl>
                              <dt className="text-sm font-medium text-gray-500 truncate capitalize">
                                {key.replace('_', ' ')}
                              </dt>
                              <dd className="text-lg font-medium text-gray-900">{value}</dd>
                            </dl>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Recent Claims */}
                <div className="bg-white shadow rounded-lg">
                  <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                      Recent Claims
                    </h3>
                    <div className="overflow-hidden">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Claim ID
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Patient
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Status
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                              Total
                            </th>
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {claims.slice(0, 5).map((claim) => (
                            <tr key={claim.id}>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {claim.id.substring(0, 8)}...
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                {claim.patient_id}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap">
                                <StatusBadge status={claim.status} />
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                ${claim.total?.value || 0} {claim.total?.currency || 'USD'}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Claims Tab */}
            {activeTab === 'claims' && (
              <div className="space-y-4">
                {/* Actions Bar */}
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
                  <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                      <input
                        type="text"
                        placeholder="Search claims..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <select
                      value={statusFilter}
                      onChange={(e) => setStatusFilter(e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    >
                      <option value="">All Status</option>
                      <option value="active">Active</option>
                      <option value="draft">Draft</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </div>
                  <button
                    onClick={() => setShowClaimForm(true)}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    New Claim
                  </button>
                </div>

                {/* Claims Table */}
                <div className="bg-white shadow rounded-lg overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Claim ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Patient ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Provider
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Use
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Total
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {filteredClaims.map((claim) => (
                        <tr key={claim.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {claim.id.substring(0, 8)}...
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {claim.patient_id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {claim.provider_id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <StatusBadge status={claim.status} />
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 capitalize">
                            {claim.use}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            ${claim.total?.value || 0} {claim.total?.currency || 'USD'}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <div className="flex space-x-2">
                              <button
                                onClick={() => {
                                  setEditingClaim(claim);
                                  setShowClaimForm(true);
                                }}
                                className="text-blue-600 hover:text-blue-900"
                              >
                                <Edit className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDeleteClaim(claim.id)}
                                className="text-red-600 hover:text-red-900"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Coverage Tab */}
            {activeTab === 'coverage' && (
              <div className="space-y-4">
                {/* Actions Bar */}
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <input
                      type="text"
                      placeholder="Search coverage..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <button
                    onClick={() => setShowCoverageForm(true)}
                    className="flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    New Coverage
                  </button>
                </div>

                {/* Coverage Table */}
                <div className="bg-white shadow rounded-lg overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Coverage ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Beneficiary
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Insurer
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Type
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Kind
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {filteredCoverages.map((coverage) => (
                        <tr key={coverage.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {coverage.id.substring(0, 8)}...
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {coverage.beneficiary_id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {coverage.insurer_id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {coverage.type?.text || 'N/A'}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <StatusBadge status={coverage.status} />
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 capitalize">
                            {coverage.kind || 'N/A'}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <div className="flex space-x-2">
                              <button
                                onClick={() => {
                                  setEditingCoverage(coverage);
                                  setShowCoverageForm(true);
                                }}
                                className="text-blue-600 hover:text-blue-900"
                              >
                                <Edit className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => {
                                  if (window.confirm('Are you sure you want to delete this coverage?')) {
                                    // Handle delete coverage
                                    console.log('Delete coverage:', coverage.id);
                                  }
                                }}
                                className="text-red-600 hover:text-red-900"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  
                  {filteredCoverages.length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                      No coverage records found.
                    </div>
                  )}
                </div>
              </div>
            )}
          </>
        )}
      </main>

      {/* Modals */}
      {showClaimForm && (
        <ClaimForm
          claim={editingClaim}
          onSave={editingClaim ? handleUpdateClaim : handleCreateClaim}
          onCancel={() => {
            setShowClaimForm(false);
            setEditingClaim(null);
          }}
        />
      )}

      {showCoverageForm && (
        <CoverageForm
          coverage={editingCoverage}
          onSave={editingCoverage ? 
            async (data) => {
              // Handle update coverage
              console.log('Update coverage:', data);
              setShowCoverageForm(false);
              setEditingCoverage(null);
            } : 
            handleCreateCoverage
          }
          onCancel={() => {
            setShowCoverageForm(false);
            setEditingCoverage(null);
          }}
        />
      )}
    </div>
  );
};

export default FHIRClaimsApp;
