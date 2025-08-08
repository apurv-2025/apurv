import React, { useState, useEffect } from 'react';
import { X, Save, User } from 'lucide-react';

const PatientForm = ({ patient, onSubmit, onCancel, isOpen }) => {
  const [formData, setFormData] = useState({
    fhir_id: '',
    family_name: '',
    given_names: [''],
    prefix: '',
    suffix: '',
    gender: '',
    birth_date: '',
    active: true
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (patient) {
      setFormData({
        fhir_id: patient.fhir_id || '',
        family_name: patient.family_name || '',
        given_names: patient.given_names || [''],
        prefix: patient.prefix || '',
        suffix: patient.suffix || '',
        gender: patient.gender || '',
        birth_date: patient.birth_date ? patient.birth_date.split('T')[0] : '',
        active: patient.active !== undefined ? patient.active : true
      });
    } else {
      setFormData({
        fhir_id: '',
        family_name: '',
        given_names: [''],
        prefix: '',
        suffix: '',
        gender: '',
        birth_date: '',
        active: true
      });
    }
    setErrors({});
  }, [patient]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleGivenNameChange = (index, value) => {
    const newGivenNames = [...formData.given_names];
    newGivenNames[index] = value;
    setFormData(prev => ({ ...prev, given_names: newGivenNames }));
  };

  const addGivenName = () => {
    setFormData(prev => ({
      ...prev,
      given_names: [...prev.given_names, '']
    }));
  };

  const removeGivenName = (index) => {
    if (formData.given_names.length > 1) {
      const newGivenNames = formData.given_names.filter((_, i) => i !== index);
      setFormData(prev => ({ ...prev, given_names: newGivenNames }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.fhir_id.trim()) {
      newErrors.fhir_id = 'FHIR ID is required';
    }
    
    if (!formData.family_name.trim()) {
      newErrors.family_name = 'Family name is required';
    }
    
    if (formData.given_names.length === 0 || !formData.given_names[0].trim()) {
      newErrors.given_names = 'At least one given name is required';
    }
    
    if (!formData.gender) {
      newErrors.gender = 'Gender is required';
    }
    
    if (!formData.birth_date) {
      newErrors.birth_date = 'Birth date is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      // Filter out empty given names
      const filteredGivenNames = formData.given_names.filter(name => name.trim());
      
      const submitData = {
        ...formData,
        given_names: filteredGivenNames
      };
      
      onSubmit(submitData);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center space-x-2">
            <User className="h-5 w-5 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              {patient ? 'Edit Patient' : 'Add New Patient'}
            </h2>
          </div>
          <button
            onClick={onCancel}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* FHIR ID */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                FHIR ID *
              </label>
              <input
                type="text"
                name="fhir_id"
                value={formData.fhir_id}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.fhir_id ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Enter FHIR ID"
              />
              {errors.fhir_id && (
                <p className="mt-1 text-sm text-red-600">{errors.fhir_id}</p>
              )}
            </div>

            {/* Family Name */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Family Name *
              </label>
              <input
                type="text"
                name="family_name"
                value={formData.family_name}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.family_name ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Enter family name"
              />
              {errors.family_name && (
                <p className="mt-1 text-sm text-red-600">{errors.family_name}</p>
              )}
            </div>

            {/* Prefix */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Prefix
              </label>
              <input
                type="text"
                name="prefix"
                value={formData.prefix}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., Dr., Mr., Ms."
              />
            </div>

            {/* Suffix */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Suffix
              </label>
              <input
                type="text"
                name="suffix"
                value={formData.suffix}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="e.g., MD, PhD, Jr."
              />
            </div>

            {/* Gender */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Gender *
              </label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.gender ? 'border-red-500' : 'border-gray-300'
                }`}
              >
                <option value="">Select gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="unknown">Unknown</option>
              </select>
              {errors.gender && (
                <p className="mt-1 text-sm text-red-600">{errors.gender}</p>
              )}
            </div>

            {/* Birth Date */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Birth Date *
              </label>
              <input
                type="date"
                name="birth_date"
                value={formData.birth_date}
                onChange={handleInputChange}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  errors.birth_date ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.birth_date && (
                <p className="mt-1 text-sm text-red-600">{errors.birth_date}</p>
              )}
            </div>
          </div>

          {/* Given Names */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Given Names *
            </label>
            <div className="space-y-2">
              {formData.given_names.map((name, index) => (
                <div key={index} className="flex space-x-2">
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => handleGivenNameChange(index, e.target.value)}
                    className={`flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                      errors.given_names ? 'border-red-500' : 'border-gray-300'
                    }`}
                    placeholder={`Given name ${index + 1}`}
                  />
                  {formData.given_names.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeGivenName(index)}
                      className="px-3 py-2 text-red-600 hover:text-red-800 transition-colors"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addGivenName}
                className="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                + Add another given name
              </button>
            </div>
            {errors.given_names && (
              <p className="mt-1 text-sm text-red-600">{errors.given_names}</p>
            )}
          </div>

          {/* Active Status */}
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              name="active"
              checked={formData.active}
              onChange={handleInputChange}
              className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label className="text-sm font-medium text-gray-700">
              Active Patient
            </label>
          </div>

          {/* Form Actions */}
          <div className="flex justify-end space-x-3 pt-6 border-t">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-md transition-colors flex items-center space-x-2"
            >
              <Save className="h-4 w-4" />
              <span>{patient ? 'Update Patient' : 'Create Patient'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PatientForm; 