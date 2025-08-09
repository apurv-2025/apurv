// src/components/patients/PatientForm.jsx
import React, { useState } from 'react';
import { Save } from 'lucide-react';
import ErrorMessage from '../common/ErrorMessage';

const PatientForm = ({ patient, onSave, onCancel, mode = 'create' }) => {
  const [formData, setFormData] = useState({
    first_name: patient?.first_name || '',
    last_name: patient?.last_name || '',
    date_of_birth: patient?.date_of_birth ? patient.date_of_birth.split('T')[0] : '',
    medical_record_number: patient?.medical_record_number || '',
    phone: patient?.phone || '',
    email: patient?.email || '',
    address: patient?.address || '',
    emergency_contact_name: patient?.emergency_contact_name || '',
    emergency_contact_phone: patient?.emergency_contact_phone || '',
  });

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.first_name || !formData.last_name || !formData.date_of_birth) {
      setError('Please fill in all required fields');
      return;
    }

    setSaving(true);
    setError('');

    try {
      await onSave(formData);
    } catch (err) {
      setError('Failed to save patient. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const formFields = [
    { name: 'first_name', label: 'First Name', type: 'text', required: true },
    { name: 'last_name', label: 'Last Name', type: 'text', required: true },
    { name: 'date_of_birth', label: 'Date of Birth', type: 'date', required: true },
    { name: 'medical_record_number', label: 'Medical Record Number', type: 'text', required: true },
    { name: 'phone', label: 'Phone Number', type: 'tel' },
    { name: 'email', label: 'Email Address', type: 'email' },
    { name: 'address', label: 'Address', type: 'textarea' },
    { name: 'emergency_contact_name', label: 'Emergency Contact Name', type: 'text' },
    { name: 'emergency_contact_phone', label: 'Emergency Contact Phone', type: 'tel' },
  ];

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h1 className="text-xl font-bold mb-6">
          {mode === 'create' ? 'Add New Patient' : 'Edit Patient'}
        </h1>
        
        <form onSubmit={handleSubmit}>
          {error && <ErrorMessage error={error} />}
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            {formFields.map(({ name, label, type, required }) => (
              <div key={name} className={type === 'textarea' ? 'md:col-span-2' : ''}>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {label} {required && '*'}
                </label>
                {type === 'textarea' ? (
                  <textarea
                    value={formData[name]}
                    onChange={(e) => handleChange(name, e.target.value)}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required={required}
                  />
                ) : (
                  <input
                    type={type}
                    value={formData[name]}
                    onChange={(e) => handleChange(name, e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required={required}
                  />
                )}
              </div>
            ))}
          </div>

          <div className="flex justify-between">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center"
            >
              <Save className="h-4 w-4 mr-2" />
              {saving ? 'Saving...' : mode === 'create' ? 'Create Patient' : 'Update Patient'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PatientForm;
