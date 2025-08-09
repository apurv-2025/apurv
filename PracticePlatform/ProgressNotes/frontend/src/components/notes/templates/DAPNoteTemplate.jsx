import React from 'react';

const DAPNoteTemplate = ({ content, onChange, isReadOnly }) => {
  const handleFieldChange = (field, value) => {
    onChange({ ...content, [field]: value });
  };

  const fields = [
    {
      name: 'data',
      label: 'Data',
      rows: 5,
      placeholder: "Factual information about the session, what was observed and discussed..."
    },
    {
      name: 'assessment',
      label: 'Assessment',
      rows: 4,
      placeholder: "Professional interpretation of the data, progress analysis..."
    },
    {
      name: 'plan',
      label: 'Plan',
      rows: 4,
      placeholder: "Next steps, interventions, goals for future sessions..."
    }
  ];

  return (
    <div className="space-y-6">
      {fields.map(({ name, label, rows, placeholder }) => (
        <div key={name}>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {label}
          </label>
          <textarea
            value={content[name] || ''}
            onChange={(e) => handleFieldChange(name, e.target.value)}
            disabled={isReadOnly}
            rows={rows}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            placeholder={placeholder}
          />
        </div>
      ))}
    </div>
  );
};

export default DAPNoteTemplate;
