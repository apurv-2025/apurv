import React from 'react';

const SOAPNoteTemplate = ({ content, onChange, isReadOnly }) => {
  const handleFieldChange = (field, value) => {
    onChange({ ...content, [field]: value });
  };

  const fields = [
    {
      name: 'subjective',
      label: 'Subjective',
      placeholder: "Patient's subjective report, symptoms, concerns..."
    },
    {
      name: 'objective',
      label: 'Objective',
      placeholder: "Observable data, mental status exam, behavioral observations..."
    },
    {
      name: 'assessment',
      label: 'Assessment',
      placeholder: "Clinical impressions, diagnosis, progress evaluation..."
    },
    {
      name: 'plan',
      label: 'Plan',
      placeholder: "Treatment plan, interventions, next steps, homework..."
    }
  ];

  return (
    <div className="space-y-6">
      {fields.map(({ name, label, placeholder }) => (
        <div key={name}>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {label}
          </label>
          <textarea
            value={content[name] || ''}
            onChange={(e) => handleFieldChange(name, e.target.value)}
            disabled={isReadOnly}
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            placeholder={placeholder}
          />
        </div>
      ))}
    </div>
  );
};

export default SOAPNoteTemplate;
