import React, { useState, useEffect } from 'react';
import { Search, Plus, Edit, Trash2, User, Phone, Mail, MapPin, Calendar, Heart } from 'lucide-react';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const FHIRPatientApp = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [formData, setFormData] = useState({
    fhir_id: '',
    family_name: '',
    given_names: [''], // Initialize as array of strings
    gender: '',
    birth_date: '',
    telecom: [{ system: 'phone', value: '', use: 'home' }],
    addresses: [{ use: 'home', line: [''], city: '', state: '', postal_code: '', country: '' }],
    active: true
  });

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/patients`);
      if (response.ok) {
        const data = await response.json();
        setPatients(data);
      }
    } catch (error) {
      console.error('Error fetching patients:', error);
      alert('Error fetching patients');
    } finally {
      setLoading(false);
    }
  };

  const searchPatients = async () => {
    if (!searchTerm.trim()) {
      fetchPatients();
      return;
    }
    
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/patients/search/name?family_name=${encodeURIComponent(searchTerm)}`);
      if (response.ok) {
        const data = await response.json();
        setPatients(data);
      }
    } catch (error) {
      console.error('Error searching patients:', error);
      alert('Error searching patients');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const method = selectedPatient ? 'PUT' : 'POST';
      const url = selectedPatient 
        ? `${API_BASE_URL}/patients/${selectedPatient.id}` 
        : `${API_BASE_URL}/patients`;
      
      const payload = {
        ...formData,
        given_names: formData.given_names.filter(name => name.trim()),
        telecom: formData.telecom.filter(t => t.value.trim()),
        addresses: formData.addresses.map(addr => ({
          ...addr,
          line: addr.line.filter(line => line.trim())
        })).filter(addr => addr.city.trim() || addr.line.length > 0)
      };

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        await fetchPatients();
        resetForm();
        alert(selectedPatient ? 'Patient updated successfully!' : 'Patient created successfully!');
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail || 'Failed to save patient'}`);
      }
    } catch (error) {
      console.error('Error saving patient:', error);
      alert('Error saving patient');
    } finally {
      setLoading(false);
    }
  };

  const deletePatient = async (id) => {
    if (!window.confirm('Are you sure you want to delete this patient?')) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/patients/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        await fetchPatients();
        alert('Patient deleted successfully!');
      } else {
        alert('Error deleting patient');
      }
    } catch (error) {
      console.error('Error deleting patient:', error);
      alert('Error deleting patient');
    } finally {
      setLoading(false);
    }
  };

  const editPatient = (patient) => {
    setSelectedPatient(patient);
    
    // Ensure given_names is always an array of strings
    let givenNames = [];
    if (patient.given_names) {
      if (Array.isArray(patient.given_names)) {
        givenNames = patient.given_names.filter(name => typeof name === 'string' && name.trim());
      }
    }
    if (givenNames.length === 0) {
      givenNames = [''];
    }
    
    setFormData({
      fhir_id: patient.fhir_id || '',
      family_name: patient.family_name || '',
      given_names: givenNames,
      gender: patient.gender || '',
      birth_date: patient.birth_date || '',
      telecom: patient.telecom && patient.telecom.length > 0 
        ? patient.telecom 
        : [{ system: 'phone', value: '', use: 'home' }],
      addresses: patient.addresses && patient.addresses.length > 0 
        ? patient.addresses 
        : [{ use: 'home', line: [''], city: '', state: '', postal_code: '', country: '' }],
      active: patient.active ?? true
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setSelectedPatient(null);
    setShowForm(false);
    setFormData({
      fhir_id: '',
      family_name: '',
      given_names: [''], // Make sure this is always an array of strings
      gender: '',
      birth_date: '',
      telecom: [{ system: 'phone', value: '', use: 'home' }],
      addresses: [{ use: 'home', line: [''], city: '', state: '', postal_code: '', country: '' }],
      active: true
    });
  };

  const updateFormData = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const updateGivenName = (index, value) => {
    setFormData(prev => ({
      ...prev,
      given_names: prev.given_names.map((name, i) => i === index ? value : name)
    }));
  };

  const updateArrayField = (field, index, subField, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].map((item, i) => 
        i === index ? { ...item, [subField]: value } : item
      )
    }));
  };

  const addArrayItem = (field, template) => {
    setFormData(prev => {
      if (field === 'given_names') {
        // For given_names, template should be a string
        return {
          ...prev,
          [field]: [...prev[field], template || '']
        };
      } else {
        // For other arrays (objects like telecom, addresses)
        return {
          ...prev,
          [field]: [...prev[field], template]
        };
      }
    });
  };

  const removeArrayItem = (field, index) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].filter((_, i) => i !== index)
    }));
  };

  const formatDate = (dateString) => {
    return dateString ? new Date(dateString).toLocaleDateString() : 'N/A';
  };

  const getFullName = (patient) => {
    const given = patient.given_names?.join(' ') || '';
    const family = patient.family_name || '';
    return `${given} ${family}`.trim() || 'Unknown';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Heart className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-3xl font-bold text-gray-900">Patient Management</h1>
            </div>
            <button
              onClick={() => {
                resetForm();
                setShowForm(true);
              }}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center"
            >
              <Plus className="h-5 w-5 mr-2" />
              Add Patient
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Bar */}
        <div className="mb-6">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Search by family name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={searchPatients}
              className="bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-6 rounded-lg"
            >
              Search
            </button>
            <button
              onClick={() => { setSearchTerm(''); fetchPatients(); }}
              className="bg-gray-400 hover:bg-gray-500 text-white font-medium py-2 px-6 rounded-lg"
            >
              Clear
            </button>
          </div>
        </div>

        {/* Patient List */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {patients.map((patient) => (
              <div key={patient.id} className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center">
                    <User className="h-8 w-8 text-gray-400 mr-3" />
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {getFullName(patient)}
                      </h3>
                      <p className="text-sm text-gray-500">ID: {patient.fhir_id}</p>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <button
                      onClick={() => editPatient(patient)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                    <button
                      onClick={() => deletePatient(patient.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center">
                    <Calendar className="h-4 w-4 mr-2" />
                    <span>Born: {formatDate(patient.birth_date)}</span>
                  </div>
                  
                  {patient.gender && (
                    <div className="flex items-center">
                      <User className="h-4 w-4 mr-2" />
                      <span>Gender: {patient.gender}</span>
                    </div>
                  )}

                  {patient.telecom && patient.telecom.length > 0 && (
                    <div className="flex items-center">
                      <Phone className="h-4 w-4 mr-2" />
                      <span>{patient.telecom[0].value}</span>
                    </div>
                  )}

                  {patient.addresses && patient.addresses.length > 0 && patient.addresses[0].city && (
                    <div className="flex items-center">
                      <MapPin className="h-4 w-4 mr-2" />
                      <span>{patient.addresses[0].city}, {patient.addresses[0].state}</span>
                    </div>
                  )}
                </div>

                <div className="mt-4 pt-4 border-t">
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    patient.active 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {patient.active ? 'Active' : 'Inactive'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {patients.length === 0 && !loading && (
          <div className="text-center py-12">
            <User className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No patients found</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by adding a new patient.</p>
          </div>
        )}
      </div>

      {/* Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-screen overflow-y-auto">
            <div className="px-6 py-4 border-b">
              <h2 className="text-xl font-semibold text-gray-900">
                {selectedPatient ? 'Edit Patient' : 'Add New Patient'}
              </h2>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-6">
              {/* Basic Information */}
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    FHIR ID *
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.fhir_id}
                    onChange={(e) => updateFormData('fhir_id', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Family Name
                  </label>
                  <input
                    type="text"
                    value={formData.family_name}
                    onChange={(e) => updateFormData('family_name', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Given Names */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Given Names
                </label>
                {formData.given_names.map((name, index) => (
                  <div key={index} className="flex gap-2 mb-2">
                    <input
                      type="text"
                      value={typeof name === 'string' ? name : ''}
                      onChange={(e) => updateGivenName(index, e.target.value)}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder={`Given name ${index + 1}`}
                    />
                    {formData.given_names.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeArrayItem('given_names', index)}
                        className="px-3 py-2 text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => addArrayItem('given_names', '')}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  + Add Given Name
                </button>
              </div>

              {/* Gender and Birth Date */}
              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Gender
                  </label>
                  <select
                    value={formData.gender}
                    onChange={(e) => updateFormData('gender', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                    <option value="unknown">Unknown</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Birth Date
                  </label>
                  <input
                    type="date"
                    value={formData.birth_date}
                    onChange={(e) => updateFormData('birth_date', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              {/* Contact Information */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Contact Information
                </label>
                {formData.telecom.map((contact, index) => (
                  <div key={index} className="grid gap-2 md:grid-cols-3 mb-2">
                    <select
                      value={contact.system}
                      onChange={(e) => updateArrayField('telecom', index, 'system', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="phone">Phone</option>
                      <option value="email">Email</option>
                      <option value="fax">Fax</option>
                    </select>
                    <input
                      type="text"
                      value={contact.value}
                      onChange={(e) => updateArrayField('telecom', index, 'value', e.target.value)}
                      placeholder="Contact value"
                      className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <div className="flex gap-2">
                      <select
                        value={contact.use}
                        onChange={(e) => updateArrayField('telecom', index, 'use', e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="home">Home</option>
                        <option value="work">Work</option>
                        <option value="mobile">Mobile</option>
                      </select>
                      {formData.telecom.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeArrayItem('telecom', index)}
                          className="px-3 py-2 text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => addArrayItem('telecom', { system: 'phone', value: '', use: 'home' })}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  + Add Contact
                </button>
              </div>

              {/* Addresses */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Addresses
                </label>
                {formData.addresses.map((address, index) => (
                  <div key={index} className="border border-gray-200 rounded-md p-4 mb-4">
                    <div className="flex justify-between items-center mb-3">
                      <select
                        value={address.use}
                        onChange={(e) => updateArrayField('addresses', index, 'use', e.target.value)}
                        className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="home">Home</option>
                        <option value="work">Work</option>
                        <option value="temp">Temporary</option>
                      </select>
                      {formData.addresses.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeArrayItem('addresses', index)}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                    
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={address.line[0] || ''}
                        onChange={(e) => {
                          const newLine = [...(address.line || [''])];
                          newLine[0] = e.target.value;
                          updateArrayField('addresses', index, 'line', newLine);
                        }}
                        placeholder="Street address"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      
                      <div className="grid gap-3 md:grid-cols-2">
                        <input
                          type="text"
                          value={address.city}
                          onChange={(e) => updateArrayField('addresses', index, 'city', e.target.value)}
                          placeholder="City"
                          className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <input
                          type="text"
                          value={address.state}
                          onChange={(e) => updateArrayField('addresses', index, 'state', e.target.value)}
                          placeholder="State"
                          className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                      
                      <div className="grid gap-3 md:grid-cols-2">
                        <input
                          type="text"
                          value={address.postal_code}
                          onChange={(e) => updateArrayField('addresses', index, 'postal_code', e.target.value)}
                          placeholder="Postal Code"
                          className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <input
                          type="text"
                          value={address.country}
                          onChange={(e) => updateArrayField('addresses', index, 'country', e.target.value)}
                          placeholder="Country"
                          className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    </div>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => addArrayItem('addresses', { 
                    use: 'home', 
                    line: [''], 
                    city: '', 
                    state: '', 
                    postal_code: '', 
                    country: '' 
                  })}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  + Add Address
                </button>
              </div>

              {/* Active Status */}
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="active"
                  checked={formData.active}
                  onChange={(e) => updateFormData('active', e.target.checked)}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label htmlFor="active" className="ml-2 text-sm font-medium text-gray-700">
                  Active Patient
                </label>
              </div>

              {/* Form Actions */}
              <div className="flex justify-end space-x-3 pt-6 border-t">
                <button
                  type="button"
                  onClick={resetForm}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {loading ? 'Saving...' : selectedPatient ? 'Update Patient' : 'Create Patient'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default FHIRPatientApp;
