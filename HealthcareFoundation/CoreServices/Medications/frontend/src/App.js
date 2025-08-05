import React, { useState, useEffect } from 'react';
import { Search, Plus, Edit, Trash2, Pill, FileText, Calendar, User, AlertCircle } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8000';

const MedicationApp = () => {
  const [activeTab, setActiveTab] = useState('medications');
  const [medications, setMedications] = useState([]);
  const [medicationRequests, setMedicationRequests] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [formType, setFormType] = useState('medication');
  const [searchTerm, setSearchTerm] = useState('');

  const [medicationForm, setMedicationForm] = useState({
    fhir_id: '',
    code: { text: '', coding: [] },
    status: 'active',
    form: { text: '', coding: [] },
    ingredients: [{ item_codeable_concept: { text: '' }, is_active: true }],
    batch: { lot_number: '', expiration_date: '' }
  });

  const [medicationRequestForm, setMedicationRequestForm] = useState({
    fhir_id: '',
    status: 'active',
    intent: 'order',
    priority: 'routine',
    subject_patient_id: '',
    medication_id: '',
    medication_codeable_concept: { text: '', coding: [] },
    authored_on: new Date().toISOString().split('T')[0],
    dosage_instructions: [{ text: '', timing: { repeat: { frequency: 1, period: 1, periodUnit: 'day' } } }],
    dispense_request: { quantity: { value: 30, unit: 'tablet' }, expected_supply_duration: { value: 30, unit: 'day' } }
  });

  useEffect(() => {
    if (activeTab === 'medications') {
      fetchMedications();
    } else {
      fetchMedicationRequests();
    }
  }, [activeTab]);

  const fetchMedications = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/medications`);
      if (response.ok) {
        const data = await response.json();
        setMedications(data);
      }
    } catch (error) {
      console.error('Error fetching medications:', error);
      alert('Error fetching medications');
    } finally {
      setLoading(false);
    }
  };

  const fetchMedicationRequests = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/medication-requests`);
      if (response.ok) {
        const data = await response.json();
        setMedicationRequests(data);
      }
    } catch (error) {
      console.error('Error fetching medication requests:', error);
      alert('Error fetching medication requests');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const isRequest = formType === 'medicationRequest';
      const formData = isRequest ? medicationRequestForm : medicationForm;
      const endpoint = isRequest ? 'medication-requests' : 'medications';
      
      const method = selectedItem ? 'PUT' : 'POST';
      const url = selectedItem 
        ? `${API_BASE_URL}/${endpoint}/${selectedItem.id}` 
        : `${API_BASE_URL}/${endpoint}`;

      const payload = { ...formData };
      if (!isRequest) {
        payload.ingredients = payload.ingredients.filter(ing => ing.item_codeable_concept?.text?.trim());
        if (payload.code?.text === '') payload.code = null;
        if (payload.form?.text === '') payload.form = null;
        if (payload.batch?.lot_number === '' && payload.batch?.expiration_date === '') payload.batch = null;
      } else {
        payload.dosage_instructions = payload.dosage_instructions.filter(dose => dose.text?.trim());
        if (payload.medication_codeable_concept?.text === '') payload.medication_codeable_concept = null;
        if (!payload.medication_id) payload.medication_id = null;
        if (!payload.subject_patient_id) {
          alert('Patient ID is required');
          setLoading(false);
          return;
        }
      }

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        if (activeTab === 'medications') {
          await fetchMedications();
        } else {
          await fetchMedicationRequests();
        }
        resetForm();
        alert(selectedItem ? 'Item updated successfully!' : 'Item created successfully!');
      } else {
        try {
          const error = await response.json();
          alert(`Error: ${error.detail || JSON.stringify(error)}`);
        } catch (parseError) {
          alert(`Error: HTTP ${response.status} - ${response.statusText}`);
        }
      }
    } catch (error) {
      console.error('Error saving item:', error);
      alert('Error saving item');
    } finally {
      setLoading(false);
    }
  };

  const deleteItem = async (id, type) => {
    if (!window.confirm('Are you sure you want to delete this item?')) {
      return;
    }

    setLoading(true);
    try {
      const endpoint = type === 'medication' ? 'medications' : 'medication-requests';
      const response = await fetch(`${API_BASE_URL}/${endpoint}/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        if (type === 'medication') {
          await fetchMedications();
        } else {
          await fetchMedicationRequests();
        }
        alert('Item deleted successfully!');
      } else {
        alert('Error deleting item');
      }
    } catch (error) {
      console.error('Error deleting item:', error);
      alert('Error deleting item');
    } finally {
      setLoading(false);
    }
  };

  const editItem = (item, type) => {
    setSelectedItem(item);
    setFormType(type);
    
    if (type === 'medication') {
      setMedicationForm({
        fhir_id: item.fhir_id || '',
        code: item.code || { text: '', coding: [] },
        status: item.status || 'active',
        form: item.form || { text: '', coding: [] },
        ingredients: item.ingredients?.length > 0 
          ? item.ingredients 
          : [{ item_codeable_concept: { text: '' }, is_active: true }],
        batch: item.batch || { lot_number: '', expiration_date: '' }
      });
    } else {
      setMedicationRequestForm({
        fhir_id: item.fhir_id || '',
        status: item.status || 'active',
        intent: item.intent || 'order',
        priority: item.priority || 'routine',
        subject_patient_id: item.subject_patient_id || '',
        medication_id: item.medication_id || '',
        medication_codeable_concept: item.medication_codeable_concept || { text: '', coding: [] },
        authored_on: item.authored_on ? item.authored_on.split('T')[0] : new Date().toISOString().split('T')[0],
        dosage_instructions: item.dosage_instructions?.length > 0 
          ? item.dosage_instructions 
          : [{ text: '', timing: { repeat: { frequency: 1, period: 1, periodUnit: 'day' } } }],
        dispense_request: item.dispense_request || { quantity: { value: 30, unit: 'tablet' }, expected_supply_duration: { value: 30, unit: 'day' } }
      });
    }
    setShowForm(true);
  };

  const resetForm = () => {
    setSelectedItem(null);
    setShowForm(false);
    setMedicationForm({
      fhir_id: '',
      code: { text: '', coding: [] },
      status: 'active',
      form: { text: '', coding: [] },
      ingredients: [{ item_codeable_concept: { text: '' }, is_active: true }],
      batch: { lot_number: '', expiration_date: '' }
    });
    setMedicationRequestForm({
      fhir_id: '',
      status: 'active',
      intent: 'order',
      priority: 'routine',
      subject_patient_id: '',
      medication_id: '',
      medication_codeable_concept: { text: '', coding: [] },
      authored_on: new Date().toISOString().split('T')[0],
      dosage_instructions: [{ text: '', timing: { repeat: { frequency: 1, period: 1, periodUnit: 'day' } } }],
      dispense_request: { quantity: { value: 30, unit: 'tablet' }, expected_supply_duration: { value: 30, unit: 'day' } }
    });
  };

  const openForm = (type) => {
    setFormType(type);
    resetForm();
    setShowForm(true);
  };

  const formatDate = (dateString) => {
    return dateString ? new Date(dateString).toLocaleDateString() : 'N/A';
  };

  const getStatusBadge = (status) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      inactive: 'bg-gray-100 text-gray-800',
      'entered-in-error': 'bg-red-100 text-red-800',
      'on-hold': 'bg-yellow-100 text-yellow-800',
      cancelled: 'bg-red-100 text-red-800',
      completed: 'bg-blue-100 text-blue-800',
      stopped: 'bg-orange-100 text-orange-800',
      draft: 'bg-purple-100 text-purple-800',
      unknown: 'bg-gray-100 text-gray-800'
    };
    
    return (
      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${colors[status] || colors.unknown}`}>
        {status}
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Pill className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-3xl font-bold text-gray-900">Medication Management</h1>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => openForm('medication')}
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg flex items-center"
              >
                <Plus className="h-5 w-5 mr-2" />
                Add Medication
              </button>
              <button
                onClick={() => openForm('medicationRequest')}
                className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg flex items-center"
              >
                <Plus className="h-5 w-5 mr-2" />
                Add Request
              </button>
            </div>
          </div>

          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('medications')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'medications'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Pill className="h-5 w-5 inline-block mr-2" />
                Medications
              </button>
              <button
                onClick={() => setActiveTab('medicationRequests')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'medicationRequests'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <FileText className="h-5 w-5 inline-block mr-2" />
                Medication Requests
              </button>
            </nav>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder={`Search ${activeTab === 'medications' ? 'medications' : 'medication requests'}...`}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : activeTab === 'medications' ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {medications
              .filter(med => 
                !searchTerm || 
                med.fhir_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                med.code?.text?.toLowerCase().includes(searchTerm.toLowerCase())
              )
              .map((medication) => (
                <div key={medication.id} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center">
                      <Pill className="h-8 w-8 text-blue-400 mr-3" />
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          {medication.code?.text || 'Unnamed Medication'}
                        </h3>
                        <p className="text-sm text-gray-500">ID: {medication.fhir_id}</p>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => editItem(medication, 'medication')}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => deleteItem(medication.id, 'medication')}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  <div className="space-y-2 text-sm text-gray-600">
                    {medication.form?.text && (
                      <div>
                        <span className="font-medium">Form:</span> {medication.form.text}
                      </div>
                    )}
                    
                    {medication.ingredients && medication.ingredients.length > 0 && (
                      <div>
                        <span className="font-medium">Ingredients:</span>
                        <ul className="ml-4 mt-1">
                          {medication.ingredients.slice(0, 3).map((ing, idx) => (
                            <li key={idx} className="text-xs">
                              • {ing.item_codeable_concept?.text || 'Unknown ingredient'}
                            </li>
                          ))}
                          {medication.ingredients.length > 3 && (
                            <li className="text-xs text-gray-400">
                              ... and {medication.ingredients.length - 3} more
                            </li>
                          )}
                        </ul>
                      </div>
                    )}

                    {medication.batch?.lot_number && (
                      <div>
                        <span className="font-medium">Lot:</span> {medication.batch.lot_number}
                      </div>
                    )}
                  </div>

                  <div className="mt-4 pt-4 border-t">
                    {getStatusBadge(medication.status)}
                  </div>
                </div>
              ))}
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
            {medicationRequests
              .filter(req => 
                !searchTerm || 
                req.fhir_id?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                req.medication_codeable_concept?.text?.toLowerCase().includes(searchTerm.toLowerCase())
              )
              .map((request) => (
                <div key={request.id} className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center">
                      <FileText className="h-8 w-8 text-green-400 mr-3" />
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">
                          {request.medication_codeable_concept?.text || `Request ${request.fhir_id}`}
                        </h3>
                        <p className="text-sm text-gray-500">ID: {request.fhir_id}</p>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => editItem(request, 'medicationRequest')}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        <Edit className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => deleteItem(request.id, 'medicationRequest')}
                        className="text-red-600 hover:text-red-800"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  <div className="space-y-2 text-sm text-gray-600">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2" />
                      <span>Authored: {formatDate(request.authored_on)}</span>
                    </div>
                    
                    <div className="flex items-center">
                      <User className="h-4 w-4 mr-2" />
                      <span>Patient: {request.subject_patient_id}</span>
                    </div>

                    <div className="flex items-center">
                      <AlertCircle className="h-4 w-4 mr-2" />
                      <span>Intent: {request.intent}</span>
                    </div>

                    {request.priority && (
                      <div>
                        <span className="font-medium">Priority:</span> {request.priority}
                      </div>
                    )}

                    {request.dosage_instructions && request.dosage_instructions.length > 0 && (
                      <div>
                        <span className="font-medium">Dosage:</span>
                        <div className="ml-4 mt-1 text-xs">
                          {request.dosage_instructions[0].text || 'See detailed instructions'}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="mt-4 pt-4 border-t flex justify-between items-center">
                    {getStatusBadge(request.status)}
                    {request.dispense_request?.quantity && (
                      <span className="text-xs text-gray-500">
                        Qty: {request.dispense_request.quantity.value} {request.dispense_request.quantity.unit}
                      </span>
                    )}
                  </div>
                </div>
              ))}
          </div>
        )}

        {((activeTab === 'medications' && medications.length === 0) || 
          (activeTab === 'medicationRequests' && medicationRequests.length === 0)) && 
          !loading && (
          <div className="text-center py-12">
            {activeTab === 'medications' ? (
              <Pill className="mx-auto h-12 w-12 text-gray-400" />
            ) : (
              <FileText className="mx-auto h-12 w-12 text-gray-400" />
            )}
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              No {activeTab === 'medications' ? 'medications' : 'medication requests'} found
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by adding a new {activeTab === 'medications' ? 'medication' : 'medication request'}.
            </p>
          </div>
        )}
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-screen overflow-y-auto">
            <div className="px-6 py-4 border-b">
              <h2 className="text-xl font-semibold text-gray-900">
                {selectedItem ? 'Edit' : 'Add New'} {formType === 'medication' ? 'Medication' : 'Medication Request'}
              </h2>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-6">
              {formType === 'medication' ? (
                <div className="space-y-6">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        FHIR ID *
                      </label>
                      <input
                        type="text"
                        required
                        value={medicationForm.fhir_id}
                        onChange={(e) => setMedicationForm(prev => ({ ...prev, fhir_id: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Status
                      </label>
                      <select
                        value={medicationForm.status}
                        onChange={(e) => setMedicationForm(prev => ({ ...prev, status: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                        <option value="entered-in-error">Entered in Error</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Medication Name
                      </label>
                      <input
                        type="text"
                        value={medicationForm.code.text}
                        onChange={(e) => setMedicationForm(prev => ({ 
                          ...prev, 
                          code: { ...prev.code, text: e.target.value }
                        }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="e.g., Lisinopril 10mg"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Form
                      </label>
                      <input
                        type="text"
                        value={medicationForm.form.text}
                        onChange={(e) => setMedicationForm(prev => ({ 
                          ...prev, 
                          form: { ...prev.form, text: e.target.value }
                        }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="e.g., Tablet, Capsule, Liquid"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Ingredients
                    </label>
                    {medicationForm.ingredients.map((ingredient, index) => (
                      <div key={index} className="flex gap-2 mb-2">
                        <input
                          type="text"
                          value={ingredient.item_codeable_concept?.text || ''}
                          onChange={(e) => {
                            const newIngredients = [...medicationForm.ingredients];
                            newIngredients[index] = {
                              ...newIngredients[index],
                              item_codeable_concept: { text: e.target.value }
                            };
                            setMedicationForm(prev => ({ ...prev, ingredients: newIngredients }));
                          }}
                          placeholder="Ingredient name"
                          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                        <label className="flex items-center">
                          <input
                            type="checkbox"
                            checked={ingredient.is_active !== false}
                            onChange={(e) => {
                              const newIngredients = [...medicationForm.ingredients];
                              newIngredients[index] = {
                                ...newIngredients[index],
                                is_active: e.target.checked
                              };
                              setMedicationForm(prev => ({ ...prev, ingredients: newIngredients }));
                            }}
                            className="mr-1"
                          />
                          Active
                        </label>
                        {medicationForm.ingredients.length > 1 && (
                          <button
                            type="button"
                            onClick={() => {
                              const newIngredients = medicationForm.ingredients.filter((_, i) => i !== index);
                              setMedicationForm(prev => ({ ...prev, ingredients: newIngredients }));
                            }}
                            className="px-3 py-2 text-red-600 hover:text-red-800"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        )}
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={() => setMedicationForm(prev => ({
                        ...prev,
                        ingredients: [...prev.ingredients, { item_codeable_concept: { text: '' }, is_active: true }]
                      }))}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      + Add Ingredient
                    </button>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Lot Number
                      </label>
                      <input
                        type="text"
                        value={medicationForm.batch.lot_number}
                        onChange={(e) => setMedicationForm(prev => ({ 
                          ...prev, 
                          batch: { ...prev.batch, lot_number: e.target.value }
                        }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Expiration Date
                      </label>
                      <input
                        type="date"
                        value={medicationForm.batch.expiration_date}
                        onChange={(e) => setMedicationForm(prev => ({ 
                          ...prev, 
                          batch: { ...prev.batch, expiration_date: e.target.value }
                        }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        FHIR ID *
                      </label>
                      <input
                        type="text"
                        required
                        value={medicationRequestForm.fhir_id}
                        onChange={(e) => setMedicationRequestForm(prev => ({ ...prev, fhir_id: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Patient ID *
                      </label>
                      <input
                        type="text"
                        required
                        value={medicationRequestForm.subject_patient_id}
                        onChange={(e) => setMedicationRequestForm(prev => ({ ...prev, subject_patient_id: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="patient123 (will be converted to UUID format)"
                      />
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-3">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Status
                      </label>
                      <select
                        value={medicationRequestForm.status}
                        onChange={(e) => setMedicationRequestForm(prev => ({ ...prev, status: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="active">Active</option>
                        <option value="on-hold">On Hold</option>
                        <option value="cancelled">Cancelled</option>
                        <option value="completed">Completed</option>
                        <option value="entered-in-error">Entered in Error</option>
                        <option value="stopped">Stopped</option>
                        <option value="draft">Draft</option>
                        <option value="unknown">Unknown</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Intent
                      </label>
                      <select
                        value={medicationRequestForm.intent}
                        onChange={(e) => setMedicationRequestForm(prev => ({ ...prev, intent: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="proposal">Proposal</option>
                        <option value="plan">Plan</option>
                        <option value="order">Order</option>
                        <option value="original-order">Original Order</option>
                        <option value="reflex-order">Reflex Order</option>
                        <option value="filler-order">Filler Order</option>
                        <option value="instance-order">Instance Order</option>
                        <option value="option">Option</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Priority
                      </label>
                      <select
                        value={medicationRequestForm.priority}
                        onChange={(e) => setMedicationRequestForm(prev => ({ ...prev, priority: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="routine">Routine</option>
                        <option value="urgent">Urgent</option>
                        <option value="asap">ASAP</option>
                        <option value="stat">STAT</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Medication Name
                      </label>
                      <input
                        type="text"
                        value={medicationRequestForm.medication_codeable_concept.text}
                        onChange={(e) => setMedicationRequestForm(prev => ({ 
                          ...prev, 
                          medication_codeable_concept: { ...prev.medication_codeable_concept, text: e.target.value }
                        }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="e.g., Lisinopril 10mg"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Authored Date
                      </label>
                      <input
                        type="date"
                        value={medicationRequestForm.authored_on}
                        onChange={(e) => setMedicationRequestForm(prev => ({ ...prev, authored_on: e.target.value }))}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Dosage Instructions
                    </label>
                    {medicationRequestForm.dosage_instructions.map((dosage, index) => (
                      <div key={index} className="border border-gray-200 rounded-md p-4 mb-4">
                        <div className="flex justify-between items-center mb-3">
                          <span className="font-medium">Dosage {index + 1}</span>
                          {medicationRequestForm.dosage_instructions.length > 1 && (
                            <button
                              type="button"
                              onClick={() => {
                                const newDosages = medicationRequestForm.dosage_instructions.filter((_, i) => i !== index);
                                setMedicationRequestForm(prev => ({ ...prev, dosage_instructions: newDosages }));
                              }}
                              className="text-red-600 hover:text-red-800"
                            >
                              <Trash2 className="h-4 w-4" />
                            </button>
                          )}
                        </div>
                        
                        <textarea
                          value={dosage.text || ''}
                          onChange={(e) => {
                            const newDosages = [...medicationRequestForm.dosage_instructions];
                            newDosages[index] = { ...newDosages[index], text: e.target.value };
                            setMedicationRequestForm(prev => ({ ...prev, dosage_instructions: newDosages }));
                          }}
                          placeholder="e.g., Take 1 tablet by mouth once daily"
                          rows={2}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    ))}
                    <button
                      type="button"
                      onClick={() => setMedicationRequestForm(prev => ({
                        ...prev,
                        dosage_instructions: [...prev.dosage_instructions, { text: '', timing: { repeat: { frequency: 1, period: 1, periodUnit: 'day' } } }]
                      }))}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      + Add Dosage Instruction
                    </button>
                  </div>

                  <div className="border border-gray-200 rounded-md p-4">
                    <h4 className="font-medium text-gray-900 mb-3">Dispense Request</h4>
                    <div className="grid gap-4 md:grid-cols-2">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Quantity
                        </label>
                        <div className="flex gap-2">
                          <input
                            type="number"
                            value={medicationRequestForm.dispense_request.quantity?.value || ''}
                            onChange={(e) => setMedicationRequestForm(prev => ({ 
                              ...prev, 
                              dispense_request: { 
                                ...prev.dispense_request, 
                                quantity: { ...prev.dispense_request.quantity, value: parseInt(e.target.value) || 0 }
                              }
                            }))}
                            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="30"
                          />
                          <input
                            type="text"
                            value={medicationRequestForm.dispense_request.quantity?.unit || ''}
                            onChange={(e) => setMedicationRequestForm(prev => ({ 
                              ...prev, 
                              dispense_request: { 
                                ...prev.dispense_request, 
                                quantity: { ...prev.dispense_request.quantity, unit: e.target.value }
                              }
                            }))}
                            className="w-24 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="tablets"
                          />
                        </div>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Expected Supply Duration
                        </label>
                        <div className="flex gap-2">
                          <input
                            type="number"
                            value={medicationRequestForm.dispense_request.expected_supply_duration?.value || ''}
                            onChange={(e) => setMedicationRequestForm(prev => ({ 
                              ...prev, 
                              dispense_request: { 
                                ...prev.dispense_request, 
                                expected_supply_duration: { ...prev.dispense_request.expected_supply_duration, value: parseInt(e.target.value) || 0 }
                              }
                            }))}
                            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="30"
                          />
                          <input
                            type="text"
                            value={medicationRequestForm.dispense_request.expected_supply_duration?.unit || ''}
                            onChange={(e) => setMedicationRequestForm(prev => ({ 
                              ...prev, 
                              dispense_request: { 
                                ...prev.dispense_request, 
                                expected_supply_duration: { ...prev.dispense_request.expected_supply_duration, unit: e.target.value }
                              }
                            }))}
                            className="w-24 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            placeholder="days"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

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
                  {loading ? 'Saving...' : selectedItem ? `Update ${formType === 'medication' ? 'Medication' : 'Request'}` : `Create ${formType === 'medication' ? 'Medication' : 'Request'}`}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default MedicationApp;
