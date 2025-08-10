// File: src/components/upload/ExtractedDataDisplay.js
import React from 'react';
import { CheckCircle } from 'lucide-react';
import Card from '../common/Card';

const ExtractedDataDisplay = ({ data }) => {
  const fields = [
    { key: 'patient_name', label: 'Patient Name' },
    { key: 'member_id', label: 'Member ID' },
    { key: 'group_number', label: 'Group Number' },
    { key: 'plan_name', label: 'Plan Name' },
    { key: 'insurance_company', label: 'Insurance Company' },
    { key: 'effective_date', label: 'Effective Date' },
    { key: 'phone_number', label: 'Phone Number' }
  ];

  const extractedFields = fields.filter(field => data[field.key]);

  if (extractedFields.length === 0) {
    return (
      <Card title="Extraction Results">
        <p className="text-gray-500">No data could be extracted from the uploaded file.</p>
      </Card>
    );
  }

  return (
    <Card>
      <div className="flex items-center mb-4">
        <CheckCircle className="h-6 w-6 text-green-500 mr-2" />
        <h3 className="text-lg font-medium text-gray-900">
          Extracted Information
        </h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {extractedFields.map(({ key, label }) => (
          <div key={key} className="border-l-4 border-green-400 pl-4">
            <dt className="text-sm font-medium text-gray-500">
              {label}
            </dt>
            <dd className="text-sm text-gray-900 mt-1">
              {data[key]}
            </dd>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default ExtractedDataDisplay;
