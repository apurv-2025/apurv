// File: src/components/forms/PatientInformationForm.js - Patient Information Form
import React, { useState } from 'react';
import { User } from 'lucide-react';
import Card from '../common/Card';
import Button from '../common/Button';
import FormField from '../common/FormField';
import { usePatientInformation } from '../../hooks/usePatientInformation';

const PatientInformationForm = () => {
  const { createPatient, validationErrors } = usePatientInformation();
  const [loading, setLoading] = useState(false);
  
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    middle_name: '',
    date_of_birth: '',
    gender: 'M',
    member_id_primary: '',
    member_id_secondary: '',
    address_line1: '',
    address_line2: '',
    city: '',
    state: '',
    zip_code: '',
    phone_home: '',
    phone_work: '',
    phone_mobile: '',
    email: '',
    primary_care_provider: '',
    hipaa_authorization: false
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    const result = await createPatient(formData);
    
    if (result) {
      // Reset form on success
      setFormData({
        first_name: '',
        last_name: '',
        middle_name: '',
        date_of_birth: '',
        gender: 'M',
        member_id_primary: '',
        member_id_secondary: '',
        address_line1: '',
        address_line2: '',
        city: '',
        state: '',
        zip_code: '',
        phone_home: '',
        phone_work: '',
        phone_mobile: '',
        email: '',
        primary_care_provider: '',
        hipaa_authorization: false
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

  return (
    <Card title="EDI 275 Patient Information">
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Demographics */}
        <div className="border-b border-gray-200 pb-6">
          <h3 className="text-md font-medium text-gray-800 mb-4">Demographics</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormField
              label="First Name"
              value={formData.first_name}
              onChange={(e) => handleChange('first_name', e.target.value)}
              required
              error={validationErrors.first_name}
            />
            <FormField
              label="Last Name"
              value={formData.last_name}
              onChange={(e) => handleChange('last_name', e.target.value)}
              required
              error={validationErrors.last_name}
            />
            <FormField
              label="Middle Name"
              value={formData.middle_name}
              onChange={(e) => handleChange('middle_name', e.target.value)}
            />
            <FormField
              label="Date of Birth"
              type="date"
              value={formData.date_of_birth}
              onChange={(e) => handleChange('date_of_birth', e.target.value)}
              required
              error={validationErrors.date_of_birth}
            />
            <FormField
              label="Gender"
              type="select"
              value={formData.gender}
              onChange={(e) => handleChange('gender', e.target.value)}
              options={genderOptions}
            />
            <FormField
              label="Primary Member ID"
              value={formData.member_id_primary}
              onChange={(e) => handleChange('member_id_primary', e.target.value)}
              required
              error={validationErrors.member_id_primary}
            />
          </div>
        </div>

        {/* Contact Information */}
        <div className="border-b border-gray-200 pb-6">
          <h3 className="text-md font-medium text-gray-800 mb-4">Contact Information</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              label="Address Line 1"
              value={formData.address_line1}
              onChange={(e) => handleChange('address_line1', e.target.value)}
            />
            <FormField
              label="Address Line 2"
              value={formData.address_line2}
              onChange={(e) => handleChange('address_line2', e.target.value)}
            />
            <FormField
              label="City"
              value={formData.city}
              onChange={(e) => handleChange('city', e.target.value)}
            />
            <FormField
              label="State"
              value={formData.state}
              onChange={(e) => handleChange('state', e.target.value)}
            />
            <FormField
              label="ZIP Code"
              value={formData.zip_code}
              onChange={(e) => handleChange('zip_code', e.target.value)}
            />
            <FormField
              label="Primary Care Provider"
              value={formData.primary_care_provider}
              onChange={(e) => handleChange('primary_care_provider', e.target.value)}
            />
            <FormField
              label="Phone (Home)"
              type="tel"
              value={formData.phone_home}
              onChange={(e) => handleChange('phone_home', e.target.value)}
              error={validationErrors.phone_home}
            />
            <FormField
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => handleChange('email', e.target.value)}
              error={validationErrors.email}
            />
          </div>
        </div>

        {/* HIPAA Authorization */}
        <div className="border-b border-gray-200 pb-6">
          <div className="flex items-center">
            <input
              type="checkbox"
              checked={formData.hipaa_authorization}
              onChange={(e) => handleChange('hipaa_authorization', e.target.checked)}
              className="mr-3 h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
            />
            <label className="text-sm font-medium text-gray-700">
              HIPAA Authorization - I authorize the use and disclosure of my health information
            </label>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end pt-6">
          <Button
            type="submit"
            loading={loading}
            icon={User}
            size="large"
            variant="success"
          >
            Create Patient Record
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default PatientInformationForm;
