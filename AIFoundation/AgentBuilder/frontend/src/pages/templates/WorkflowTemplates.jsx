import React, { useState } from 'react';
import { Search } from 'lucide-react';
import TemplateCard from '../../components/templates/TemplateCard';
import SearchAndFilter from '../../components/ui/SearchAndFilter';
import templateService from '../../services/templateService';

const TemplateLibrary = ({ onSelectTemplate }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Get templates from centralized service
  const templates = templateService.getAgentTemplates();

  const agenttypes = [
    { value: 'all', label: 'All Types' },
    { value: 'autonomous', label: 'Autonomus' },
    { value: 'assistant', label: 'Human in the Loop' }
  ];

  const subtypes = [
    { value: 'all', label: 'All Subtypes' },
    { value: 'standalone', label: 'Billing & Insurance' },
    { value: 'multi-agent', label: 'Front Desk' }
  ];
  

  // Get categories from centralized service
  const categories = templateService.getCategories();

  // Use centralized filtering
  const filteredTemplates = templateService.filterTemplates(templates, searchTerm, selectedCategory);

  const handleSelectTemplate = (template) => {
    if (onSelectTemplate) {
      onSelectTemplate(template);
    } else {
      // Default behavior - could navigate to agent creation with template
      console.log('Selected template:', template);
      alert(`Selected template: ${template.name}. This would navigate to agent creation.`);
    }
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Agent Template Library</h1>
        <p className="text-gray-600">Choose from pre-built templates to quickly create specialized agents</p>
      </div>

      {/* Search and Filter - Category */}
      <SearchAndFilter
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        selectedCategory={selectedCategory}
        onCategoryChange={setSelectedCategory}
        categories={categories}
        searchPlaceholder="Search templates by category..."
        className="mb-8"
      />

      {/* Template Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredTemplates.map(template => (
          <TemplateCard
            key={template.id}
            template={template}
            onSelect={handleSelectTemplate}
          />
        ))}
      </div>

      {/* No Results */}
      {filteredTemplates.length === 0 && (
        <div className="text-center py-12">
          <Search className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No templates found</h3>
          <p className="text-gray-500">Try adjusting your search or filter criteria</p>
        </div>
      )}
    </div>
  );
};

export default TemplateLibrary;
