import React from 'react';

const TemplateCard = ({ template, onSelect }) => {
  const complexityColors = {
    'beginner': 'bg-green-100 text-green-800',
    'intermediate': 'bg-yellow-100 text-yellow-800',
    'advanced': 'bg-red-100 text-red-800'
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <div className="text-2xl">{template.icon}</div>
        <span className={`px-2 py-1 text-xs rounded-full ${complexityColors[template.complexity]}`}>
          {template.complexity}
        </span>
      </div>

      <h3 className="text-lg font-semibold text-gray-900 mb-2">{template.name}</h3>
      <p className="text-sm text-gray-600 mb-4">{template.description}</p>

      <div className="flex flex-wrap gap-2 mb-4">
        {template.tags.map(tag => (
          <span key={tag} className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">
            {tag}
          </span>
        ))}
      </div>

      <button
        onClick={() => onSelect(template)}
        className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-200"
      >
        Use Template
      </button>
    </div>
  );
};

export default TemplateCard;
