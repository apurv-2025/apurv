// File: src/components/eligibility/EligibilityForm.js
import React, { useState } from 'react';
import { CheckCircle } from 'lucide-react';
import Card from '../common/Card';
import Button from '../common/Button';
import { useEligibilityCheck } from '../../hooks/useEligibilityCheck';
import { useApp } from '../../contexts/AppContext';

const EligibilityForm = () => {
  const { extractedData } = useApp();
  const { submitEligibilityInquiry, submitting } = useEligibilityCheck();
  
  const [formData, setFormData] = useState({
    member_id: extractedData?.member_id || '',
    provider_npi: '',
    subscriber_first_name: extractedData?.patient_name?.split(' ')[0] || '',
    subscriber_last_name: extractedData?.patient_name?.split(' ').slice(1).join(' ') || '',
    subscriber_dob: '',
    service_type: '30'
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await submitEligibilityInquiry(formData);
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <Card title="Eligibility and Benefits Verification">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Member ID *
            </label>
            <input
              type="text"
              required
              value={formData.member_id}
              onChange={(e) => handleChange('member_id', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Provider NPI *
            </label>
            <input
              type="text"
              required
              value={formData.provider_npi}
              onChange={(e) => handleChange('provider_npi', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              First Name *
            </label>
            <input
              type="text"
              required
              value={formData.subscriber_first_name}
              onChange={(e) => handleChange('subscriber_first_name', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Last Name *
            </label>
            <input
              type="text"
              required
              value={formData.subscriber_last_name}
              onChange={(e) => handleChange('subscriber_last_name', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Date of Birth *
            </label>
            <input
              type="date"
              required
              value={formData.subscriber_dob}
              onChange={(e) => handleChange('subscriber_dob', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Service Type
            </label>
            <select
              value={formData.service_type}
              onChange={(e) => handleChange('service_type', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="30">Health Benefit Plan Coverage</option>
              <option value="1">Medical Care</option>
              <option value="88">Pharmacy</option>
              <option value="98">Professional Services</option>
            </select>
          </div>
        </div>

        <div className="flex justify-end pt-4">
          <Button
            type="submit"
            loading={submitting}
            icon={CheckCircle}
          >
            Submit Eligibility Inquiry
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default EligibilityForm;
