import React, { useState, useEffect } from 'react';
import { ChevronRight, FileText, FileCheck, Plus, Search, Trash2, Eye, Calendar, User } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

const FHIRDocumentManagement = () => {
  const [activeTab, setActiveTab] = useState('documents');
  const [documents, setDocuments] = useState([]);
  const [questionnaires, setQuestionnaires] = useState([]);
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchData();
  }, [activeTab]);

  const fetchData = async () => {
    setLoading(true);
    try {
      let endpoint = '';
      switch (activeTab) {
        case 'documents':
          endpoint = '/document-references/';
          break;
        case 'questionnaires':
          endpoint = '/questionnaires/';
          break;
        case 'responses':
          endpoint = '/questionnaire-responses/';
          break;
      }
      
      const response = await fetch(`${API_BASE_URL}${endpoint}`);
      const data = await response.json();
      
      switch (activeTab) {
        case 'documents':
          setDocuments(data);
          break;
        case 'questionnaires':
          setQuestionnaires(data);
          break;
        case 'responses':
          setResponses(data);
          break;
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, type) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;
    
    try {
      let endpoint = '';
      switch (type) {
        case 'document':
          endpoint = `/document-references/${id}`;
          break;
        case 'questionnaire':
          endpoint = `/questionnaires/${id}`;
          break;
        case 'response':
          endpoint = `/questionnaire-responses/${id}`;
          break;
      }
      
      await fetch(`${API_BASE_URL}${endpoint}`, { method: 'DELETE' });
      fetchData();
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  const CreateDocumentForm = () => {
    const [formData, setFormData] = useState({
      fhir_id: '',
      status: 'current',
      subject_patient_id: '00000000-0000-0000-0000-000000000001',
      description: '',
      content: [{ attachment: { contentType: 'application/pdf', title: 'Document' } }]
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        await fetch(`${API_BASE_URL}/document-references/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
        setShowCreateModal(false);
        fetchData();
      } catch (error) {
        console.error('Error creating document:', error);
      }
    };

    return (
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">FHIR ID</label>
          <input
            type="text"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={formData.fhir_id}
            onChange={(e) => setFormData({...formData, fhir_id: e.target.value})}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            value={formData.status}
            onChange={(e) => setFormData({...formData, status: e.target.value})}
          >
            <option value="current">Current</option>
            <option value="superseded">Superseded</option>
            <option value="entered-in-error">Entered in Error</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Patient</label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            value={formData.subject_patient_id}
            onChange={(e) => setFormData({...formData, subject_patient_id: e.target.value})}
            required
          >
            <option value="00000000-0000-0000-0000-000000000001">John Doe</option>
            <option value="00000000-0000-0000-0000-000000000002">Jane Smith</option>
            <option value="11111111-1111-1111-1111-111111111111">Alice Johnson</option>
            <option value="22222222-2222-2222-2222-222222222222">Bob Wilson</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows="3"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
          />
        </div>
        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Create Document
          </button>
          <button
            type="button"
            onClick={() => setShowCreateModal(false)}
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>
    );
  };

  const CreateQuestionnaireForm = () => {
    const [formData, setFormData] = useState({
      fhir_id: '',
      title: '',
      status: 'draft',
      description: '',
      items: [{ linkId: '1', text: 'Sample Question', type: 'string' }]
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        await fetch(`${API_BASE_URL}/questionnaires/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
        setShowCreateModal(false);
        fetchData();
      } catch (error) {
        console.error('Error creating questionnaire:', error);
      }
    };

    return (
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">FHIR ID</label>
          <input
            type="text"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={formData.fhir_id}
            onChange={(e) => setFormData({...formData, fhir_id: e.target.value})}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
          <input
            type="text"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={formData.title}
            onChange={(e) => setFormData({...formData, title: e.target.value})}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            value={formData.status}
            onChange={(e) => setFormData({...formData, status: e.target.value})}
          >
            <option value="draft">Draft</option>
            <option value="active">Active</option>
            <option value="retired">Retired</option>
            <option value="unknown">Unknown</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows="3"
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}
          />
        </div>
        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Create Questionnaire
          </button>
          <button
            type="button"
            onClick={() => setShowCreateModal(false)}
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>
    );
  };

  const CreateResponseForm = () => {
    const [formData, setFormData] = useState({
      fhir_id: '',
      status: 'completed',
      subject_patient_id: '00000000-0000-0000-0000-000000000001',
      authored: new Date().toISOString(),
      items: [{ linkId: '1', text: 'Sample Answer', answer: [{ valueString: 'Sample Response' }] }]
    });

    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        await fetch(`${API_BASE_URL}/questionnaire-responses/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(formData)
        });
        setShowCreateModal(false);
        fetchData();
      } catch (error) {
        console.error('Error creating response:', error);
      }
    };

    return (
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">FHIR ID</label>
          <input
            type="text"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            value={formData.fhir_id}
            onChange={(e) => setFormData({...formData, fhir_id: e.target.value})}
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            value={formData.status}
            onChange={(e) => setFormData({...formData, status: e.target.value})}
          >
            <option value="in-progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="amended">Amended</option>
            <option value="entered-in-error">Entered in Error</option>
            <option value="stopped">Stopped</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Patient</label>
          <select
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            value={formData.subject_patient_id}
            onChange={(e) => setFormData({...formData, subject_patient_id: e.target.value})}
            required
          >
            <option value="00000000-0000-0000-0000-000000000001">John Doe</option>
            <option value="00000000-0000-0000-0000-000000000002">Jane Smith</option>
            <option value="11111111-1111-1111-1111-111111111111">Alice Johnson</option>
            <option value="22222222-2222-2222-2222-222222222222">Bob Wilson</option>
          </select>
        </div>
        <div className="flex gap-3 pt-4">
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Create Response
          </button>
          <button
            type="button"
            onClick={() => setShowCreateModal(false)}
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
          >
            Cancel
          </button>
        </div>
      </form>
    );
  };

  const filteredData = () => {
    let data = [];
    switch (activeTab) {
      case 'documents':
        data = documents;
        break;
      case 'questionnaires':
        data = questionnaires;
        break;
      case 'responses':
        data = responses;
        break;
      default:
        data = [];
    }
    
    if (!searchTerm) return data;
    
    return data.filter(item => 
      item.fhir_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.title?.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const getStatusColor = (status) => {
    const statusColors = {
      'current': 'bg-green-100 text-green-800',
      'active': 'bg-green-100 text-green-800',
      'completed': 'bg-blue-100 text-blue-800',
      'draft': 'bg-yellow-100 text-yellow-800',
      'in-progress': 'bg-orange-100 text-orange-800',
      'superseded': 'bg-gray-100 text-gray-800',
      'retired': 'bg-red-100 text-red-800',
      'entered-in-error': 'bg-red-100 text-red-800'
    };
    return statusColors[status] || 'bg-gray-100 text-gray-800';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">FHIR Document Management</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Search..."
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <button
                onClick={() => setShowCreateModal(true)}
                className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="h-5 w-5 mr-2" />
                Create New
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8">
            {[
              { id: 'documents', name: 'Document References', icon: FileText },
              { id: 'questionnaires', name: 'Questionnaires', icon: FileCheck },
              { id: 'responses', name: 'Responses', icon: User }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-5 w-5 mr-2" />
                  {tab.name}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">
                {activeTab === 'documents' && 'Document References'}
                {activeTab === 'questionnaires' && 'Questionnaires'}
                {activeTab === 'responses' && 'Questionnaire Responses'}
              </h2>
            </div>

            <div className="divide-y divide-gray-200">
              {filteredData().length === 0 ? (
                <div className="text-center py-12">
                  <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No items found</h3>
                  <p className="text-gray-500">Get started by creating a new item.</p>
                </div>
              ) : (
                filteredData().map((item) => (
                  <div key={item.id} className="px-6 py-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center">
                          <h3 className="text-sm font-medium text-gray-900">
                            {item.fhir_id}
                          </h3>
                          <span className={`ml-3 px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(item.status)}`}>
                            {item.status}
                          </span>
                        </div>
                        <div className="mt-1 text-sm text-gray-600">
                          {item.description || item.title || 'No description'}
                        </div>
                        <div className="mt-1 flex items-center text-xs text-gray-500">
                          <Calendar className="h-4 w-4 mr-1" />
                          Created: {formatDate(item.created_at)}
                          {item.authored && (
                            <>
                              <span className="mx-2">•</span>
                              Authored: {formatDate(item.authored)}
                            </>
                          )}
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => setSelectedItem(item)}
                          className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                          title="View details"
                        >
                          <Eye className="h-5 w-5" />
                        </button>
                        <button
                          onClick={() => handleDelete(item.id, activeTab.slice(0, -1))}
                          className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                          title="Delete"
                        >
                          <Trash2 className="h-5 w-5" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </main>

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-md w-full mx-4 max-h-96 overflow-y-auto">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">
                Create New {activeTab === 'documents' ? 'Document Reference' : activeTab === 'questionnaires' ? 'Questionnaire' : 'Response'}
              </h3>
            </div>
            <div className="p-6">
              {activeTab === 'documents' && <CreateDocumentForm />}
              {activeTab === 'questionnaires' && <CreateQuestionnaireForm />}
              {activeTab === 'responses' && <CreateResponseForm />}
            </div>
          </div>
        </div>
      )}

      {/* Details Modal */}
      {selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full mx-4 max-h-96 overflow-y-auto">
            <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-lg font-medium text-gray-900">Item Details</h3>
              <button
                onClick={() => setSelectedItem(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            </div>
            <div className="p-6">
              <pre className="text-sm text-gray-600 whitespace-pre-wrap">
                {JSON.stringify(selectedItem, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FHIRDocumentManagement;
