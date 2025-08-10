// File: src/components/forms/PriorAuthorizationForm.js - Prior Authorization Form
import React, { useState } from 'react';
import { CheckCircle } from 'lucide-react';
import Card from '../common/Card';
import Button from '../common/Button';
import FormField from '../common/FormField';
import { usePriorAuthorization } from '../../hooks/usePriorAuthorization';

const PriorAuthorizationForm = () => {
  const { submitRequest, validationErrors } = usePriorAuthorization();
  const [loading, setLoading] = useState(false);
  
  const [formData, setFormData] = useState({
    patient_first_name: '',
    patient_last_name: '',
    patient_dob: '',
    patient_gender: 'M',
    member_id: '',
    requesting_provider_npi: '',
    requesting_provider_name: '',
    service_date_from: '',
    service_date_to: '',
    medical_necessity: '',
    clinical_information: '',
    priority: 'normal'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    const result = await submitRequest(formData);
    
    if (result) {
      // Reset form on success
      setFormData({
        patient_first_name: '',
        patient_last_name: '',
        patient_dob: '',
        patient_gender: 'M',
        member_id: '',
        requesting_provider_npi: '',
        requesting_provider_name: '',
        service_date_from: '',
        service_date_to: '',
        medical_necessity: '',
        clinical_information: '',
        priority: 'normal'
      });
    }
    
    setLoading(false);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const genderOptions = [
    { value: 'M', label: 'Male' },
    { value: 'F', label: 'Female' },
    { value: 'U', label: 'Unknown' }
  ];

  const priorityOptions = [
    { value: 'normal', label: 'Normal' },
    { value: 'urgent', label: 'Urgent' },
    { value: 'emergency', label: 'Emergency' }
  ];

  return (
    <Card title="EDI 278 Prior Authorization Request">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Patient Information */}
        <div className="border-b border-gray-200 pb-6">
          <h3 className="text-md font-medium text-gray-800 mb-4">Patient Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              label="First Name"
              value={formData.patient_first_name}
              onChange={(e) => handleChange('patient_first_name', e.target.value)}
              required
              error={validationErrors.patient_first_name}
            />
            <FormField
              label="Last Name"
              value={formData.patient_last_name}
              onChange={(e) => handleChange('patient_last_name', e.target.value)}
              required
              error={validationErrors.patient_last_name}
            />
            <FormField
              label="Date of Birth"
              type="date"
              value={formData.patient_dob}
              onChange={(e) => handleChange('patient_dob', e.target.value)}
              required
              error={validationErrors.patient_dob}
            />
            <FormField
              label="Gender"
              type="select"
              value={formData.patient_gender}
              onChange={(e) => handleChange('patient_gender', e.target.value)}
              options={genderOptions}
            />
            <FormField
              label="Member ID"
              value={formData.member_id}
              onChange={(e) => handleChange('member_id', e.target.value)}
              required
              error={validationErrors.member_id}
            />
          </div>
        </div>

        {/* Provider Information */}
        <div className="border-b border-gray-200 pb-6">
          <h3 className="text-md font-medium text-gray-800 mb-4">Provider Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              label="Provider NPI"
              value={formData.requesting_provider_npi}
              onChange={(e) => handleChange('requesting_provider_npi', e.target.value)}
              placeholder="10-digit NPI"
              required
              error={validationErrors.requesting_provider_npi}
            />
            <FormField
              label="Provider Name"
              value={formData.requesting_provider_name}
              onChange={(e) => handleChange('requesting_provider_name', e.target.value)}
            />
          </div>
        </div>

        {/* Service Information */}
        <div className="border-b border-gray-200 pb-6">
          <h3 className="text-md font-medium text-gray-800 mb-4">Service Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              label="Service Date From"
              type="date"
              value={formData.service_date_from}
              onChange={(e) => handleChange('service_date_from', e.target.value)}
              required
              error={validationErrors.service_date_from}
            />
            <FormField
              label="Service Date To"
              type="date"
              value={formData.service_date_to}
              onChange={(e) => handleChange('service_date_to', e.target.value)}
            />
            <FormField
              label="Priority"
              type="select"
              value={formData.priority}
              onChange={(e) => handleChange('priority', e.target.value)}
              options={priorityOptions}
            />
          </div>
        </div>

        {/* Clinical Information */}
        <div>
          <h3 className="text-md font-medium text-gray-800 mb-4">Clinical Information</h3>
          <div className="space-y-4">
            <FormField
              label="Medical Necessity"
              type="textarea"
              value={formData.medical_necessity}
              onChange={(e) => handleChange('medical_necessity', e.target.value)}
              placeholder="Explain the medical necessity for the requested services..."
              required
              error={validationErrors.medical_necessity}
            />
            <FormField
              label="Additional Clinical Information"
              type="textarea"
              value={formData.clinical_information}
              onChange={(e) => handleChange('clinical_information', e.target.value)}
              placeholder="Additional clinical details, lab results, etc..."
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end pt-6">
          <Button
            type="submit"
            loading={loading}
            icon={CheckCircle}
            size="large"
          >
            Submit Authorization Request
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default PriorAuthorizationForm;
