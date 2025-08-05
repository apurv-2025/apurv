import React, { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Search, Filter, Calendar, User, FileText, Activity } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

// Utility functions
const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString();
};

const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString();
};

// Navigation Component
const Navigation = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'encounters', label: 'Encounters', icon: Calendar },
    { id: 'observations', label: 'Observations', icon: Activity },
    { id: 'conditions', label: 'Conditions', icon: FileText }
  ];

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <User className="h-8 w-8" />
            <h1 className="text-xl font-bold">FHIR Management System</h1>
          </div>
          <div className="flex space-x-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-800 text-white'
                      : 'hover:bg-blue-500'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

// Generic Modal Component
const Modal = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">{title}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>
        {children}
      </div>
    </div>
  );
};

// Encounters Component
const Encounters = () => {
  const [encounters, setEncounters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingEncounter, setEditingEncounter] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const [formData, setFormData] = useState({
    fhir_id: '',
    status: '',
    subject_patient_id: '',
    period_start: '',
    period_end: ''
  });

  const statusOptions = ['planned', 'arrived', 'triaged', 'in-progress', 'onleave', 'finished', 'cancelled'];

  const fetchEncounters = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/encounters/`);
      const data = await response.json();
      setEncounters(data);
    } catch (error) {
      console.error('Error fetching encounters:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEncounters();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const method = editingEncounter ? 'PUT' : 'POST';
    const url = editingEncounter 
      ? `${API_BASE_URL}/encounters/${editingEncounter.id}`
      : `${API_BASE_URL}/encounters/`;

    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        fetchEncounters();
        setIsModalOpen(false);
        resetForm();
      }
    } catch (error) {
      console.error('Error saving encounter:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this encounter?')) {
      try {
        await fetch(`${API_BASE_URL}/encounters/${id}`, { method: 'DELETE' });
        fetchEncounters();
      } catch (error) {
        console.error('Error deleting encounter:', error);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      fhir_id: '',
      status: '',
      subject_patient_id: '',
      period_start: '',
      period_end: ''
    });
    setEditingEncounter(null);
  };

  const openEditModal = (encounter) => {
    setEditingEncounter(encounter);
    setFormData({
      fhir_id: encounter.fhir_id,
      status: encounter.status,
      subject_patient_id: encounter.subject_patient_id,
      period_start: encounter.period_start ? encounter.period_start.split('T')[0] : '',
      period_end: encounter.period_end ? encounter.period_end.split('T')[0] : ''
    });
    setIsModalOpen(true);
  };

  const filteredEncounters = encounters.filter(encounter =>
    encounter.fhir_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    encounter.status.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Encounters</h2>
        <button
          onClick={() => {
            resetForm();
            setIsModalOpen(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700"
        >
          <Plus className="h-4 w-4" />
          <span>Add Encounter</span>
        </button>
      </div>

      <div className="mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Search encounters..."
            className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg w-full"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">FHIR ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Patient ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Period Start</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredEncounters.map((encounter) => (
              <tr key={encounter.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {encounter.fhir_id}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    encounter.status === 'finished' ? 'bg-green-100 text-green-800' :
                    encounter.status === 'in-progress' ? 'bg-blue-100 text-blue-800' :
                    encounter.status === 'planned' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {encounter.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {encounter.subject_patient_id}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {formatDate(encounter.period_start)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    onClick={() => openEditModal(encounter)}
                    className="text-blue-600 hover:text-blue-900 mr-3"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(encounter.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingEncounter ? 'Edit Encounter' : 'Add Encounter'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">FHIR ID</label>
            <input
              type="text"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.fhir_id}
              onChange={(e) => setFormData({...formData, fhir_id: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.status}
              onChange={(e) => setFormData({...formData, status: e.target.value})}
            >
              <option value="">Select Status</option>
              {statusOptions.map(status => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Patient ID</label>
            <input
              type="text"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.subject_patient_id}
              onChange={(e) => setFormData({...formData, subject_patient_id: e.target.value})}
              placeholder="e.g., 123e4567-e89b-12d3-a456-426614174000"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Period Start</label>
            <input
              type="date"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.period_start}
              onChange={(e) => setFormData({...formData, period_start: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Period End</label>
            <input
              type="date"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.period_end}
              onChange={(e) => setFormData({...formData, period_end: e.target.value})}
            />
          </div>
          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={() => setIsModalOpen(false)}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {editingEncounter ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

// Observations Component
const Observations = () => {
  const [observations, setObservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingObservation, setEditingObservation] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const [formData, setFormData] = useState({
    fhir_id: '',
    status: '',
    code: { coding: [{ code: '', display: '' }] },
    subject_patient_id: '',
    encounter_id: '',
    effective_date_time: '',
    value_quantity_value: '',
    value_quantity_unit: '',
    value_string: ''
  });

  const statusOptions = ['registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled'];

  const fetchObservations = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/observations/`);
      const data = await response.json();
      setObservations(data);
    } catch (error) {
      console.error('Error fetching observations:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchObservations();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const method = editingObservation ? 'PUT' : 'POST';
    const url = editingObservation 
      ? `${API_BASE_URL}/observations/${editingObservation.id}`
      : `${API_BASE_URL}/observations/`;

    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        fetchObservations();
        setIsModalOpen(false);
        resetForm();
      }
    } catch (error) {
      console.error('Error saving observation:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this observation?')) {
      try {
        await fetch(`${API_BASE_URL}/observations/${id}`, { method: 'DELETE' });
        fetchObservations();
      } catch (error) {
        console.error('Error deleting observation:', error);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      fhir_id: '',
      status: '',
      code: { coding: [{ code: '', display: '' }] },
      subject_patient_id: '',
      encounter_id: '',
      effective_date_time: '',
      value_quantity_value: '',
      value_quantity_unit: '',
      value_string: ''
    });
    setEditingObservation(null);
  };

  const openEditModal = (observation) => {
    setEditingObservation(observation);
    setFormData({
      fhir_id: observation.fhir_id,
      status: observation.status,
      code: observation.code || { coding: [{ code: '', display: '' }] },
      subject_patient_id: observation.subject_patient_id,
      encounter_id: observation.encounter_id || '',
      effective_date_time: observation.effective_date_time ? observation.effective_date_time.split('T')[0] : '',
      value_quantity_value: observation.value_quantity_value || '',
      value_quantity_unit: observation.value_quantity_unit || '',
      value_string: observation.value_string || ''
    });
    setIsModalOpen(true);
  };

  const filteredObservations = observations.filter(observation =>
    observation.fhir_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    observation.status.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Observations</h2>
        <button
          onClick={() => {
            resetForm();
            setIsModalOpen(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700"
        >
          <Plus className="h-4 w-4" />
          <span>Add Observation</span>
        </button>
      </div>

      <div className="mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Search observations..."
            className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg w-full"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">FHIR ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Value</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredObservations.map((observation) => (
              <tr key={observation.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {observation.fhir_id}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    observation.status === 'final' ? 'bg-green-100 text-green-800' :
                    observation.status === 'preliminary' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {observation.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {observation.code?.coding?.[0]?.display || observation.code?.coding?.[0]?.code || 'N/A'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {observation.value_quantity_value ? 
                    `${observation.value_quantity_value} ${observation.value_quantity_unit || ''}` :
                    observation.value_string || 'N/A'
                  }
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {formatDate(observation.effective_date_time)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    onClick={() => openEditModal(observation)}
                    className="text-blue-600 hover:text-blue-900 mr-3"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(observation.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingObservation ? 'Edit Observation' : 'Add Observation'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">FHIR ID</label>
            <input
              type="text"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.fhir_id}
              onChange={(e) => setFormData({...formData, fhir_id: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.status}
              onChange={(e) => setFormData({...formData, status: e.target.value})}
            >
              <option value="">Select Status</option>
              {statusOptions.map(status => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Code</label>
            <input
              type="text"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.code.coding[0].code}
              onChange={(e) => setFormData({
                ...formData, 
                code: { coding: [{ ...formData.code.coding[0], code: e.target.value }] }
              })}
              placeholder="e.g., 8480-6"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Code Display</label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.code.coding[0].display}
              onChange={(e) => setFormData({
                ...formData, 
                code: { coding: [{ ...formData.code.coding[0], display: e.target.value }] }
              })}
              placeholder="e.g., Systolic blood pressure"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Patient ID</label>
            <input
              type="text"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.subject_patient_id}
              onChange={(e) => setFormData({...formData, subject_patient_id: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Encounter ID (Optional)</label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.encounter_id}
              onChange={(e) => setFormData({...formData, encounter_id: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Effective Date</label>
            <input
              type="date"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.effective_date_time}
              onChange={(e) => setFormData({...formData, effective_date_time: e.target.value})}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Quantity Value</label>
              <input
                type="number"
                step="any"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                value={formData.value_quantity_value}
                onChange={(e) => setFormData({...formData, value_quantity_value: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Unit</label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                value={formData.value_quantity_unit}
                onChange={(e) => setFormData({...formData, value_quantity_unit: e.target.value})}
                placeholder="e.g., mmHg"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">String Value</label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.value_string}
              onChange={(e) => setFormData({...formData, value_string: e.target.value})}
              placeholder="Alternative to quantity value"
            />
          </div>
          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={() => setIsModalOpen(false)}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {editingObservation ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

// Conditions Component
const Conditions = () => {
  const [conditions, setConditions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingCondition, setEditingCondition] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const [formData, setFormData] = useState({
    fhir_id: '',
    clinical_status: '',
    verification_status: '',
    code: { coding: [{ code: '', display: '' }] },
    subject_patient_id: '',
    encounter_id: '',
    onset_date_time: '',
    recorded_date: ''
  });

  const clinicalStatusOptions = ['active', 'recurrence', 'relapse', 'inactive', 'remission', 'resolved', 'unknown'];
  const verificationStatusOptions = ['unconfirmed', 'provisional', 'differential', 'confirmed', 'refuted', 'entered-in-error'];

  const fetchConditions = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/conditions/`);
      const data = await response.json();
      setConditions(data);
    } catch (error) {
      console.error('Error fetching conditions:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConditions();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const method = editingCondition ? 'PUT' : 'POST';
    const url = editingCondition 
      ? `${API_BASE_URL}/conditions/${editingCondition.id}`
      : `${API_BASE_URL}/conditions/`;

    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        fetchConditions();
        setIsModalOpen(false);
        resetForm();
      }
    } catch (error) {
      console.error('Error saving condition:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this condition?')) {
      try {
        await fetch(`${API_BASE_URL}/conditions/${id}`, { method: 'DELETE' });
        fetchConditions();
      } catch (error) {
        console.error('Error deleting condition:', error);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      fhir_id: '',
      clinical_status: '',
      verification_status: '',
      code: { coding: [{ code: '', display: '' }] },
      subject_patient_id: '',
      encounter_id: '',
      onset_date_time: '',
      recorded_date: ''
    });
    setEditingCondition(null);
  };

  const openEditModal = (condition) => {
    setEditingCondition(condition);
    setFormData({
      fhir_id: condition.fhir_id,
      clinical_status: condition.clinical_status || '',
      verification_status: condition.verification_status || '',
      code: condition.code || { coding: [{ code: '', display: '' }] },
      subject_patient_id: condition.subject_patient_id,
      encounter_id: condition.encounter_id || '',
      onset_date_time: condition.onset_date_time ? condition.onset_date_time.split('T')[0] : '',
      recorded_date: condition.recorded_date || ''
    });
    setIsModalOpen(true);
  };

  const filteredConditions = conditions.filter(condition =>
    condition.fhir_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (condition.clinical_status && condition.clinical_status.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Conditions</h2>
        <button
          onClick={() => {
            resetForm();
            setIsModalOpen(true);
          }}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:bg-blue-700"
        >
          <Plus className="h-4 w-4" />
          <span>Add Condition</span>
        </button>
      </div>

      <div className="mb-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <input
            type="text"
            placeholder="Search conditions..."
            className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg w-full"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">FHIR ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Clinical Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Verification Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Onset Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredConditions.map((condition) => (
              <tr key={condition.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {condition.fhir_id}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    condition.clinical_status === 'active' ? 'bg-red-100 text-red-800' :
                    condition.clinical_status === 'resolved' ? 'bg-green-100 text-green-800' :
                    condition.clinical_status === 'inactive' ? 'bg-gray-100 text-gray-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {condition.clinical_status || 'N/A'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    condition.verification_status === 'confirmed' ? 'bg-green-100 text-green-800' :
                    condition.verification_status === 'provisional' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {condition.verification_status || 'N/A'}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {condition.code?.coding?.[0]?.display || condition.code?.coding?.[0]?.code || 'N/A'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {formatDate(condition.onset_date_time)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    onClick={() => openEditModal(condition)}
                    className="text-blue-600 hover:text-blue-900 mr-3"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(condition.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingCondition ? 'Edit Condition' : 'Add Condition'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">FHIR ID</label>
            <input
              type="text"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.fhir_id}
              onChange={(e) => setFormData({...formData, fhir_id: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Clinical Status</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.clinical_status}
              onChange={(e) => setFormData({...formData, clinical_status: e.target.value})}
            >
              <option value="">Select Clinical Status</option>
              {clinicalStatusOptions.map(status => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Verification Status</label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.verification_status}
              onChange={(e) => setFormData({...formData, verification_status: e.target.value})}
            >
              <option value="">Select Verification Status</option>
              {verificationStatusOptions.map(status => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Condition Code</label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.code.coding[0].code}
              onChange={(e) => setFormData({
                ...formData, 
                code: { coding: [{ ...formData.code.coding[0], code: e.target.value }] }
              })}
              placeholder="e.g., E11.9"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Condition Display</label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.code.coding[0].display}
              onChange={(e) => setFormData({
                ...formData, 
                code: { coding: [{ ...formData.code.coding[0], display: e.target.value }] }
              })}
              placeholder="e.g., Type 2 diabetes mellitus without complications"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Patient ID</label>
            <input
              type="text"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.subject_patient_id}
              onChange={(e) => setFormData({...formData, subject_patient_id: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Encounter ID (Optional)</label>
            <input
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.encounter_id}
              onChange={(e) => setFormData({...formData, encounter_id: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Onset Date</label>
            <input
              type="date"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.onset_date_time}
              onChange={(e) => setFormData({...formData, onset_date_time: e.target.value})}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Recorded Date</label>
            <input
              type="date"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              value={formData.recorded_date}
              onChange={(e) => setFormData({...formData, recorded_date: e.target.value})}
            />
          </div>
          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={() => setIsModalOpen(false)}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {editingCondition ? 'Update' : 'Create'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

// Main App Component
const App = () => {
  const [activeTab, setActiveTab] = useState('encounters');

  const renderContent = () => {
    switch (activeTab) {
      case 'encounters':
        return <Encounters />;
      case 'observations':
        return <Observations />;
      case 'conditions':
        return <Conditions />;
      default:
        return <Encounters />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="max-w-7xl mx-auto">
        {renderContent()}
      </main>
    </div>
  );
};

export default App;
