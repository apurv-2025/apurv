import React, { useState, useEffect } from 'react';
import { Search, Plus, Edit, Trash2, UserCheck, Phone, Mail, MapPin, Calendar, Award, Languages } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

const PractitionerApp = () => {
  const [practitioners, setPractitioners] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [selectedPractitioner, setSelectedPractitioner] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchType, setSearchType] = useState('name');

  const [formData, setFormData] = useState({
    fhir_id: '',
    family_name: '',
    given_names: [''],
    prefix: '',
    suffix: '',
    gender: '',
    birth_date: '',
    telecom: [{ system: 'phone', value: '', use: 'work' }],
    addresses: [{ use: 'work', line: [''], city: '', state: '', postal_code: '', country: '' }],
    identifiers: [{ system: 'NPI', value: '', use: 'official' }],
    qualifications: [{ code: { text: '' }, issuer: { display: '' }, period: { start: '', end: '' } }],
    communication: [{ language: { text: '' }, preferred: true }],
    active: true
  });

  useEffect(() => {
    fetchPractitioners();
  }, []);

  const fetchPractitioners = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/practitioners`);
      if (response.ok) {
        const data = await response.json();
        setPractitioners(data);
      }
    } catch (error) {
      console.error('Error fetching practitioners:', error);
      alert('Error fetching practitioners');
    } finally {
      setLoading(false);
    }
  };

  const searchPractitioners = async () => {
    if (!searchTerm.trim()) {
      fetchPractitioners();
      return;
    }
    
    setLoading(true);
    try {
      let url;
      if (searchType === 'name') {
        url = `${API_BASE_URL}/practitioners/search/name?family_name=${encodeURIComponent(searchTerm)}`;
      } else {
        url = `${API_BASE_URL}/practitioners/search/identifier?identifier_value=${encodeURIComponent(searchTerm)}`;
      }
      
      const response = await fetch(url);
      if (response.ok) {
        const data = await response.json();
        setPractitioners(data);
      }
    } catch (error) {
      console.error('Error searching practitioners:', error);
      alert('Error searching practitioners');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const method = selectedPractitioner ? 'PUT' : 'POST';
      const url = selectedPractitioner 
        ? `${API_BASE_URL}/practitioners/${selectedPractitioner.id}` 
        : `${API_BASE_URL}/practitioners`;
      
      // Clean up form data
      const payload = {
        ...formData,
        given_names: formData.given_names.filter(name => name.trim()),
        telecom: formData.telecom.filter(t => t.value.trim()),
        addresses: formData.addresses.map(addr => ({
          ...addr,
          line: addr.line.filter(line => line.trim())
        })).filter(addr => addr.city.trim() || addr.line.length > 0),
        identifiers: formData.identifiers.filter(id => id.value.trim()),
        qualifications: formData.qualifications.filter(qual => qual.code?.text?.trim()),
        communication: formData.communication.filter(comm => comm.language?.text?.trim())
      };

      console.log('Sending payload:', JSON.stringify(payload, null, 2));

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        await fetchPractitioners();
        resetForm();
        alert(selectedPractitioner ? 'Practitioner updated successfully!' : 'Practitioner created successfully!');
      } else {
        const responseText = await response.text();
        console.log('Error response:', responseText);
        
        try {
          const error = JSON.parse(responseText);
          if (error.detail && Array.isArray(error.detail)) {
            const errorMessages = error.detail.map(err => {
              if (typeof err === 'object' && err.msg) {
                return `${err.loc ? err.loc.join('.') + ': ' : ''}${err.msg}`;
              }
              return JSON.stringify(err);
            }).join('\n');
            alert(`Validation Errors:\n${errorMessages}`);
          } else if (error.detail) {
            alert(`Error: ${error.detail}`);
          } else {
            alert(`Error: ${JSON.stringify(error)}`);
          }
        } catch (parseError) {
          alert(`Error: HTTP ${response.status}\n${responseText}`);
        }
      }
    } catch (error) {
      console.error('Error saving practitioner:', error);
      alert(`Network Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const deletePractitioner = async (id) => {
    if (!window.confirm('Are you sure you want to delete this practitioner?')) {
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/practitioners/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        await fetchPractitioners();
        alert('Practitioner deleted successfully!');
      } else {
        alert('Error deleting practitioner');
      }
    } catch (error) {
      console.error('Error deleting practitioner:', error);
      alert('Error deleting practitioner');
    } finally {
      setLoading(false);
    }
  };

  const editPractitioner = (practitioner) => {
    setSelectedPractitioner(practitioner);
    setFormData({
      fhir_id: practitioner.fhir_id || '',
      family_name: practitioner.family_name || '',
      given_names: practitioner.given_names || [''],
      prefix: practitioner.prefix || '',
      suffix: practitioner.suffix || '',
      gender: practitioner.gender || '',
      birth_date: practitioner.birth_date || '',
      telecom: practitioner.telecom?.length > 0 
        ? practitioner.telecom 
        : [{ system: 'phone', value: '', use: 'work' }],
      addresses: practitioner.addresses?.length > 0 
        ? practitioner.addresses 
        : [{ use: 'work', line: [''], city: '', state: '', postal_code: '', country: '' }],
      identifiers: practitioner.identifiers?.length > 0 
        ? practitioner.identifiers 
        : [{ system: 'NPI', value: '', use: 'official' }],
      qualifications: practitioner.qualifications?.length > 0 
        ? practitioner.qualifications 
        : [{ code: { text: '' }, issuer: { display: '' }, period: { start: '', end: '' } }],
      communication: practitioner.communication?.length > 0 
        ? practitioner.communication 
        : [{ language: { text: '' }, preferred: true }],
      active: practitioner.active ?? true
    });
    setShowForm(true);
  };

  const resetForm = () => {
    setSelectedPractitioner(null);
    setShowForm(false);
    setFormData({
      fhir_id: '',
      family_name: '',
      given_names: [''],
      prefix: '',
      suffix: '',
      gender: '',
      birth_date: '',
      telecom: [{ system: 'phone', value: '', use: 'work' }],
      addresses: [{ use: 'work', line: [''], city: '', state: '', postal_code: '', country: '' }],
      identifiers: [{ system: 'NPI', value: '', use: 'official' }],
      qualifications: [{ code: { text: '' }, issuer: { display: '' }, period: { start: '', end: '' } }],
      communication: [{ language: { text: '' }, preferred: true }],
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

  const updateNestedField = (field, index, subField, nestedField, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].map((item, i) => 
        i === index ? { 
          ...item, 
          [subField]: { ...item[subField], [nestedField]: value }
        } : item
      )
    }));
  };

  const addArrayItem = (field, template) => {
    setFormData(prev => ({
      ...prev,
      [field]: [...prev[field], template]
    }));
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

  const getFullName = (practitioner) => {
    const prefix = practitioner.prefix ? `${practitioner.prefix} ` : '';
    const given = practitioner.given_names?.join(' ') || '';
    const family = practitioner.family_name || '';
    const suffix = practitioner.suffix ? ` ${practitioner.suffix}` : '';
    return `${prefix}${given} ${family}${suffix}`.trim() || 'Unknown';
  };

  const getStatusBadge = (active) => {
    return (
      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
        active 
          ? 'bg-green-100 text-green-800' 
          : 'bg-red-100 text-red-800'
      }`}>
        {active ? 'Active' : 'Inactive'}
      </span>
    );
  };

  const getPrimaryIdentifier = (identifiers) => {
    if (!identifiers || identifiers.length === 0) return 'N/A';
    const npi = identifiers.find(id => id.system === 'NPI' || id.system?.includes('npi'));
    return npi?.value || identifiers[0]?.value || 'N/A';
  };

  const getPrimaryQualification = (qualifications) => {
    if (!qualifications || qualifications.length === 0) return 'N/A';
    return qualifications[0]?.code?.text || 'N/A';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <UserCheck className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-3xl font-bold text-gray-900">Practitioner Management</h1>
            </div>
            <button
              onClick={() => setShowForm(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center"
            >
              <Plus className="h-5 w-5 mr-2" />
              Add Practitioner
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
                placeholder={`Search by ${searchType === 'name' ? 'name' : 'identifier (NPI, License)'}...`}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <select
              value={searchType}
              onChange={(e) => setSearchType(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="name">Name</option>
              <option value="identifier">Identifier</option>
            </select>
            <button
              onClick={searchPractitioners}
              className="bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-6 rounded-lg"
            >
              Search
            </button>
            <button
              onClick={() => { setSearchTerm(''); fetchPractitioners(); }}
              className="bg-gray-400 hover:bg-gray-500 text-white font-medium py-2 px-6 rounded-lg"
            >
              Clear
            </button>
          </div>
        </div>

        {/* Practitioners List */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {practitioners
              .filter(practitioner => 
                !searchTerm || 
                practitioner.fhir_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                practitioner.family_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                practitioner.given_names?.some(name => name.toLowerCase().includes(searchTerm.toLowerCase()))
              )
              .map((practitioner) => (
                <div key={practitioner.id} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center">
                      <UserCheck className="h-8 w-8 text-blue-400 mr-3" />
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          {getFullName(practitioner)}
                        </h3>
                        <p className="text-sm text-gray-500">ID: {practitioner.fhir_id}</p>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => editPractitioner(practitioner)}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => deletePractitioner(practitioner.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex items-center">
                      <Award className="h-4 w-4 mr-2" />
                      <span>NPI: {getPrimaryIdentifier(practitioner.identifiers)}</span>
                    </div>
                    
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2" />
                      <span>Born: {formatDate(practitioner.birth_date)}</span>
                    </div>
                    
                    {practitioner.gender && (
                      <div className="flex items-center">
                        <UserCheck className="h-4 w-4 mr-2" />
                        <span>Gender: {practitioner.gender}</span>
                      </div>
                    )}

                    {practitioner.telecom && practitioner.telecom.length > 0 && (
                      <div className="flex items-center">
                        <Phone className="h-4 w-4 mr-2" />
                        <span>{practitioner.telecom[0].value}</span>
                      </div>
                    )}

                    {practitioner.addresses && practitioner.addresses.length > 0 && practitioner.addresses[0].city && (
                      <div className="flex items-center">
                        <MapPin className="h-4 w-4 mr-2" />
                        <span>{practitioner.addresses[0].city}, {practitioner.addresses[0].state}</span>
                      </div>
                    )}

                    <div className="flex items-center">
                      <Award className="h-4 w-4 mr-2" />
                      <span>Qualification: {getPrimaryQualification(practitioner.qualifications)}</span>
                    </div>
                  </div>

                  <div className="mt-4 pt-4 border-t">
                    {getStatusBadge(practitioner.active)}
                  </div>
                </div>
              ))}
          </div>
        )}

        {practitioners.length === 0 && !loading && (
          <div className="text-center py-12">
            <UserCheck className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No practitioners found</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by adding a new practitioner.</p>
          </div>
        )}
      </div>

      {/* Form Modal */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-screen overflow-y-auto">
            <div className="px-6 py-4 border-b">
              <h2 className="text-xl font-semibold text-gray-900">
                {selectedPractitioner ? 'Edit Practitioner' : 'Add New Practitioner'}
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
              </div>

              {/* Name Fields */}
              <div className="grid gap-4 md:grid-cols-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Prefix
                  </label>
                  <input
                    type="text"
                    value={formData.prefix}
                    onChange={(e) => updateFormData('prefix', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Dr., Prof., etc."
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

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Suffix
                  </label>
                  <input
                    type="text"
                    value={formData.suffix}
                    onChange={(e) => updateFormData('suffix', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="MD, PhD, etc."
                  />
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

              {/* Given Names */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Given Names
                </label>
                {formData.given_names.map((name, index) => (
                  <div key={index} className="flex gap-2 mb-2">
                    <input
                      type="text"
                      value={name}
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

              {/* Identifiers */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Professional Identifiers
                </label>
                {formData.identifiers.map((identifier, index) => (
                  <div key={index} className="grid gap-2 md:grid-cols-3 mb-2">
                    <select
                      value={identifier.system}
                      onChange={(e) => updateArrayField('identifiers', index, 'system', e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="NPI">NPI</option>
                      <option value="DEA">DEA</option>
                      <option value="LICENSE">Medical License</option>
                      <option value="TAX">Tax ID</option>
                    </select>
                    <input
                      type="text"
                      value={identifier.value}
                      onChange={(e) => updateArrayField('identifiers', index, 'value', e.target.value)}
                      placeholder="Identifier value"
                      className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <div className="flex gap-2">
                      <select
                        value={identifier.use}
                        onChange={(e) => updateArrayField('identifiers', index, 'use', e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="official">Official</option>
                        <option value="secondary">Secondary</option>
                      </select>
                      {formData.identifiers.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeArrayItem('identifiers', index)}
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
                  onClick={() => addArrayItem('identifiers', { system: 'NPI', value: '', use: 'official' })}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  + Add Identifier
                </button>
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
                        <option value="work">Work</option>
                        <option value="home">Home</option>
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
                  onClick={() => addArrayItem('telecom', { system: 'phone', value: '', use: 'work' })}
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
                        <option value="work">Work</option>
                        <option value="home">Home</option>
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
                    use: 'work', 
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

              {/* Qualifications */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Professional Qualifications
                </label>
                {formData.qualifications.map((qualification, index) => (
                  <div key={index} className="border border-gray-200 rounded-md p-4 mb-4">
                    <div className="flex justify-between items-center mb-3">
                      <span className="font-medium">Qualification {index + 1}</span>
                      {formData.qualifications.length > 1 && (
                        <button
                          type="button"
                          onClick={() => removeArrayItem('qualifications', index)}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="h-4 w-4" />
                        </button>
                      )}
                    </div>
                    
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={qualification.code?.text || ''}
                        onChange={(e) => updateNestedField('qualifications', index, 'code', 'text', e.target.value)}
                        placeholder="Degree/Certification (e.g., MD, RN, PhD)"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      
                      <input
                        type="text"
                        value={qualification.issuer?.display || ''}
                        onChange={(e) => updateNestedField('qualifications', index, 'issuer', 'display', e.target.value)}
                        placeholder="Issuing Institution"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      
                      <div className="grid gap-3 md:grid-cols-2">
                        <input
                          type="date"
                          value={qualification.period?.start || ''}
                          onChange={(e) => updateNestedField('qualifications', index, 'period', 'start', e.target.value)}
                          placeholder="Start Date"
                          className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <input
                          type="date"
                          value={qualification.period?.end || ''}
                          onChange={(e) => updateNestedField('qualifications', index, 'period', 'end', e.target.value)}
                          placeholder="End Date (if applicable)"
                          className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    </div>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => addArrayItem('qualifications', { 
                    code: { text: '' }, 
                    issuer: { display: '' }, 
                    period: { start: '', end: '' }
                  })}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  + Add Qualification
                </button>
              </div>

              {/* Communication Languages */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Languages Spoken
                </label>
                {formData.communication.map((comm, index) => (
                  <div key={index} className="flex gap-2 mb-2">
                    <input
                      type="text"
                      value={comm.language?.text || ''}
                      onChange={(e) => updateNestedField('communication', index, 'language', 'text', e.target.value)}
                      placeholder="Language (e.g., English, Spanish, French)"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <label className="flex items-center">
                      <input
                        type="checkbox"
                        checked={comm.preferred}
                        onChange={(e) => updateArrayField('communication', index, 'preferred', e.target.checked)}
                        className="mr-1"
                      />
                      Preferred
                    </label>
                    {formData.communication.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeArrayItem('communication', index)}
                        className="px-3 py-2 text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => addArrayItem('communication', { language: { text: '' }, preferred: false })}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  + Add Language
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
                  Active Practitioner
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
                  {loading ? 'Saving...' : selectedPractitioner ? 'Update Practitioner' : 'Create Practitioner'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default PractitionerApp;
