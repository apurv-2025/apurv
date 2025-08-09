import React, { useState, useEffect } from 'react';
import { 
  Pill, RefreshCw, Clock, AlertCircle, CheckCircle, 
  Calendar, User, FileText, Search, X, Send
} from 'lucide-react';
import { useAPI } from '../hooks/useAPI';
import { medicationsAPI } from '../services/api';

const Prescriptions = () => {
  const [activeTab, setActiveTab] = useState('current');
  const [medications, setMedications] = useState([]);
  const [filteredMedications, setFilteredMedications] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterDoctor, setFilterDoctor] = useState('all');
  const [showRefillModal, setShowRefillModal] = useState(false);
  const [selectedMedication, setSelectedMedication] = useState(null);
  const [loading, setLoading] = useState(true);

  const { data: medicationData, error } = useAPI(() => medicationsAPI.getMedications(), []);

  useEffect(() => {
    // Mock comprehensive medications data
    const mockMedications = [
      {
        id: 1,
        name: 'Lisinopril',
        genericName: 'Lisinopril',
        strength: '10mg',
        form: 'Tablet',
        prescriber: 'Dr. Sarah Johnson',
        prescribedDate: '2024-01-15',
        quantity: 90,
        daysSupply: 90,
        refillsRemaining: 2,
        totalRefills: 5,
        lastFilled: '2024-01-15',
        nextRefillDate: '2024-04-15',
        instructions: 'Take once daily in the morning with or without food',
        indication: 'High Blood Pressure',
        status: 'active',
        pharmacy: 'CVS Pharmacy - Main St',
        ndc: '0071-0222-23',
        isControlled: false,
        sideEffects: ['Dizziness', 'Dry cough', 'Headache'],
        interactions: ['NSAIDs', 'Potassium supplements']
      },
      {
        id: 2,
        name: 'Metformin',
        genericName: 'Metformin Hydrochloride',
        strength: '500mg',
        form: 'Extended Release Tablet',
        prescriber: 'Dr. Michael Chen',
        prescribedDate: '2024-01-20',
        quantity: 60,
        daysSupply: 30,
        refillsRemaining: 0,
        totalRefills: 5,
        lastFilled: '2024-02-01',
        nextRefillDate: '2024-02-18',
        instructions: 'Take twice daily with meals',
        indication: 'Type 2 Diabetes',
        status: 'refill_needed',
        pharmacy: 'Walgreens - Oak Ave',
        ndc: '0781-5526-01',
        isControlled: false,
        sideEffects: ['Nausea', 'Diarrhea', 'Stomach upset'],
        interactions: ['Alcohol', 'Contrast dye']
      },
      {
        id: 3,
        name: 'Atorvastatin',
        genericName: 'Atorvastatin Calcium',
        strength: '20mg',
        form: 'Tablet',
        prescriber: 'Dr. Sarah Johnson',
        prescribedDate: '2024-02-01',
        quantity: 30,
        daysSupply: 30,
        refillsRemaining: 5,
        totalRefills: 5,
        lastFilled: '2024-02-01',
        nextRefillDate: '2024-03-01',
        instructions: 'Take once daily in the evening',
        indication: 'High Cholesterol',
        status: 'active',
        pharmacy: 'CVS Pharmacy - Main St',
        ndc: '0071-0156-23',
        isControlled: false,
        sideEffects: ['Muscle pain', 'Liver problems', 'Memory issues'],
        interactions: ['Grapefruit juice', 'Cyclosporine']
      },
      {
        id: 4,
        name: 'Tramadol',
        genericName: 'Tramadol Hydrochloride',
        strength: '50mg',
        form: 'Tablet',
        prescriber: 'Dr. Robert Wilson',
        prescribedDate: '2024-01-10',
        quantity: 30,
        daysSupply: 15,
        refillsRemaining: 0,
        totalRefills: 0,
        lastFilled: '2024-01-10',
        nextRefillDate: null,
        instructions: 'Take every 6 hours as needed for pain. Do not exceed 8 tablets per day.',
        indication: 'Post-surgical pain',
        status: 'expired',
        pharmacy: 'CVS Pharmacy - Main St',
        ndc: '0093-0058-01',
        isControlled: true,
        controlledSchedule: 'Schedule IV',
        sideEffects: ['Drowsiness', 'Nausea', 'Constipation'],
        interactions: ['Alcohol', 'Sedatives', 'MAOIs']
      }
    ];

    setMedications(mockMedications);
    setFilteredMedications(mockMedications);
    setLoading(false);
  }, [medicationData]);

  useEffect(() => {
    let filtered = medications;

    // Filter by tab
    if (activeTab === 'active') {
      filtered = filtered.filter(med => med.status === 'active');
    } else if (activeTab === 'refill_needed') {
      filtered = filtered.filter(med => med.status === 'refill_needed');
    } else if (activeTab === 'expired') {
      filtered = filtered.filter(med => med.status === 'expired');
    } else if (activeTab === 'controlled') {
      filtered = filtered.filter(med => med.isControlled);
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(med =>
        med.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        med.genericName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        med.indication.toLowerCase().includes(searchTerm.toLowerCase()) ||
        med.prescriber.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by doctor
    if (filterDoctor !== 'all') {
      filtered = filtered.filter(med => med.prescriber === filterDoctor);
    }

    setFilteredMedications(filtered);
  }, [medications, activeTab, searchTerm, filterDoctor]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'refill_needed': return 'bg-orange-100 text-orange-800';
      case 'expired': return 'bg-gray-100 text-gray-800';
      case 'discontinued': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'active': return CheckCircle;
      case 'refill_needed': return AlertCircle;
      case 'expired': return Clock;
      default: return Pill;
    }
  };

  const requestRefill = async (medicationId) => {
    try {
      // API call would go here
      console.log('Requesting refill for medication:', medicationId);
      setMedications(prev =>
        prev.map(med =>
          med.id === medicationId
            ? { ...med, status: 'refill_requested' }
            : med
        )
      );
    } catch (error) {
      console.error('Error requesting refill:', error);
    }
  };

  const MedicationCard = ({ medication }) => {
    const isRefillTime = medication.refillsRemaining > 0 && 
      new Date(medication.nextRefillDate) <= new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);

    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-3 mb-2">
              <h3 className="text-lg font-semibold text-gray-900">{medication.name}</h3>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(medication.status)}`}>
                {medication.status.replace('_', ' ')}
              </span>
              {medication.isControlled && (
                <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium">
                  {medication.controlledSchedule}
                </span>
              )}
            </div>
            
            <p className="text-sm text-gray-600 mb-1">{medication.strength} {medication.form}</p>
            <p className="text-sm text-gray-600 mb-3">Generic: {medication.genericName}</p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4 text-sm text-gray-600">
              <div className="flex items-center space-x-2">
                <User className="w-4 h-4" />
                <span>{medication.prescriber}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Calendar className="w-4 h-4" />
                <span>Prescribed: {medication.prescribedDate}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Pill className="w-4 h-4" />
                <span>{medication.refillsRemaining} of {medication.totalRefills} refills left</span>
              </div>
            </div>

            <div className="mb-4">
              <h4 className="font-medium text-gray-900 mb-1">Instructions:</h4>
              <p className="text-sm text-gray-600">{medication.instructions}</p>
            </div>

            <div className="mb-4">
              <h4 className="font-medium text-gray-900 mb-1">Indication:</h4>
              <p className="text-sm text-gray-600">{medication.indication}</p>
            </div>

            {medication.nextRefillDate && (
              <div className={`p-3 rounded-lg border ${
                isRefillTime ? 'bg-orange-50 border-orange-200' : 'bg-blue-50 border-blue-200'
              }`}>
                <div className="flex items-center space-x-2">
                  <Clock className={`w-4 h-4 ${isRefillTime ? 'text-orange-600' : 'text-blue-600'}`} />
                  <span className={`text-sm font-medium ${isRefillTime ? 'text-orange-800' : 'text-blue-800'}`}>
                    Next refill: {medication.nextRefillDate}
                  </span>
                </div>
                {isRefillTime && (
                  <p className="text-xs text-orange-700 mt-1">Refill available now</p>
                )}
              </div>
            )}
          </div>

          <div className="flex flex-col space-y-2 ml-4">
            {(medication.status === 'active' || medication.status === 'refill_needed') && medication.refillsRemaining > 0 && (
              <button
                onClick={() => {
                  setSelectedMedication(medication);
                  setShowRefillModal(true);
                }}
                className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm flex items-center"
              >
                <RefreshCw className="w-4 h-4 mr-1" />
                Request Refill
              </button>
            )}
            
            <button className="px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors text-sm flex items-center">
              <FileText className="w-4 h-4 mr-1" />
              Details
            </button>
          </div>
        </div>
      </div>
    );
  };

  const RefillModal = () => {
    const [refillData, setRefillData] = useState({
      pharmacy: '',
      deliveryMethod: 'pickup',
      notes: '',
      urgency: 'standard'
    });

    const pharmacies = [
      'CVS Pharmacy - Main St',
      'Walgreens - Oak Ave',
      'Rite Aid - Downtown',
      'Local Community Pharmacy'
    ];

    const handleSubmit = (e) => {
      e.preventDefault();
      requestRefill(selectedMedication.id);
      setShowRefillModal(false);
      setSelectedMedication(null);
    };

    if (!showRefillModal || !selectedMedication) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Request Refill</h2>
              <button 
                onClick={() => setShowRefillModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
          </div>

          <div className="p-6">
            {/* Medication Info */}
            <div className="bg-gray-50 p-4 rounded-lg mb-6">
              <h3 className="font-medium text-gray-900 mb-2">{selectedMedication.name}</h3>
              <p className="text-sm text-gray-600">{selectedMedication.strength} {selectedMedication.form}</p>
              <p className="text-sm text-gray-600">Refills remaining: {selectedMedication.refillsRemaining}</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Pharmacy
                </label>
                <select
                  value={refillData.pharmacy}
                  onChange={(e) => setRefillData({...refillData, pharmacy: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="">Select pharmacy</option>
                  {pharmacies.map((pharmacy, index) => (
                    <option key={index} value={pharmacy}>{pharmacy}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Delivery Method
                </label>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      value="pickup"
                      checked={refillData.deliveryMethod === 'pickup'}
                      onChange={(e) => setRefillData({...refillData, deliveryMethod: e.target.value})}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Pickup at pharmacy</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      value="delivery"
                      checked={refillData.deliveryMethod === 'delivery'}
                      onChange={(e) => setRefillData({...refillData, deliveryMethod: e.target.value})}
                      className="mr-2"
                    />
                    <span className="text-sm text-gray-700">Home delivery</span>
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Urgency
                </label>
                <select
                  value={refillData.urgency}
                  onChange={(e) => setRefillData({...refillData, urgency: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="standard">Standard (3-5 days)</option>
                  <option value="urgent">Urgent (1-2 days)</option>
                  <option value="emergency">Emergency (same day)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Additional Notes (optional)
                </label>
                <textarea
                  value={refillData.notes}
                  onChange={(e) => setRefillData({...refillData, notes: e.target.value})}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Any special instructions or notes..."
                />
              </div>

              <div className="flex space-x-4 pt-6">
                <button
                  type="button"
                  onClick={() => setShowRefillModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center"
                >
                  <Send className="w-4 h-4 mr-2" />
                  Submit Request
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const uniqueDoctors = [...new Set(medications.map(med => med.prescriber))];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Prescriptions</h1>
        <p className="text-gray-600">Manage your medications and refill requests</p>
      </div>

      {/* Quick Actions */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 border border-blue-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Need a Refill?</h3>
            <p className="text-gray-600">Request refills for your current medications quickly and easily</p>
          </div>
          <div className="flex space-x-3">
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              Request Refills
            </button>
            <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors">
              Find Pharmacy
            </button>
          </div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
          <div className="flex space-x-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search medications..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <select
              value={filterDoctor}
              onChange={(e) => setFilterDoctor(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Doctors</option>
              {uniqueDoctors.map((doctor, index) => (
                <option key={index} value={doctor}>{doctor}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'current', label: 'All Current', count: medications.filter(m => m.status === 'active' || m.status === 'refill_needed').length },
              { id: 'active', label: 'Active', count: medications.filter(m => m.status === 'active').length },
              { id: 'refill_needed', label: 'Refill Needed', count: medications.filter(m => m.status === 'refill_needed').length },
              { id: 'controlled', label: 'Controlled', count: medications.filter(m => m.isControlled).length },
              { id: 'expired', label: 'Expired', count: medications.filter(m => m.status === 'expired').length }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label} ({tab.count})
              </button>
            ))}
          </nav>
        </div>

        {/* Medications List */}
        <div className="p-6">
          {filteredMedications.length === 0 ? (
            <div className="text-center py-12">
              <Pill className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No medications found</h3>
              <p className="mt-1 text-sm text-gray-500">
                No medications match your current filters.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredMedications.map(medication => (
                <MedicationCard key={medication.id} medication={medication} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Refill Modal */}
      <RefillModal />

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">Error loading medications: {error}</p>
        </div>
      )}
    </div>
  );
};

export default Prescriptions;