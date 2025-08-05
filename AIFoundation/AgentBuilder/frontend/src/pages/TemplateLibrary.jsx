import React, { useState } from 'react';
import { Search } from 'lucide-react';
import TemplateCard from '../components/templates/TemplateCard';
import SearchAndFilter from '../components/ui/SearchAndFilter';

const TemplateLibrary = ({ onSelectTemplate }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const templates = [
    {
      id: 'billing-specialist',
      name: 'Billing Specialist',
      type: 'Autonomous',
      category: 'billing',
      description: 'Handles insurance claims, payment inquiries, and billing questions',
      persona: 'Professional and detail-oriented billing specialist with expertise in medical billing and insurance processes.',
      instructions: 'Assist patients and staff with billing inquiries, insurance verification, payment processing, and claims status. Always maintain HIPAA compliance and refer complex cases to human staff.',
      tags: ['autonomous','billing', 'insurance', 'payments'],
      complexity: 'intermediate',
      icon: '💰'
    },
    {
      id: 'appointment-scheduler',
      name: 'Appointment Scheduler',
      type: 'Human in the Loop',
      category: 'front_desk',
      description: 'Manages appointment scheduling, cancellations, and rescheduling',
      persona: 'Friendly and efficient front desk assistant focused on patient convenience and schedule optimization.',
      instructions: 'Help patients schedule, reschedule, or cancel appointments. Check availability, confirm patient information, and send appointment reminders. Always verify patient identity before accessing information.',
      tags: ['human in the loop','scheduling', 'appointments', 'calendar'],
      complexity: 'beginner',
      icon: '📅'
    },
    {
      id: 'patient-intake',
      name: 'Patient Intake Assistant',
      type: 'Autonomus',
      category: 'Human in the Loop',
      description: 'Guides new patients through intake process and form completion',
      persona: 'Welcoming and patient guide who helps new patients feel comfortable while ensuring complete information collection.',
      instructions: 'Assist new patients with intake forms, explain office policies, collect insurance information, and guide them through the registration process. Ensure all required information is collected while maintaining a friendly demeanor.',
      tags: ['autonomus','intake', 'registration', 'new patients'],
      complexity: 'intermediate',
      icon: '👋'
    },
    {
      id: 'insurance-verifier',
      name: 'Insurance Verification',
      type: 'Autonomous',
      category: 'billing',
      description: 'Verifies insurance coverage and benefits for patients',
      persona: 'Thorough and knowledgeable insurance specialist who ensures accurate coverage verification.',
      instructions: 'Verify patient insurance coverage, check benefits, confirm copays and deductibles, and explain coverage limitations. Always use current insurance information and escalate complex verification issues.',
      tags: ['autonomus','insurance', 'verification', 'benefits'],
      complexity: 'advanced',
      icon: '🛡️'
    },
    {
      id: 'medication-reminder',
      name: 'Medication Reminder',
      type: 'Autonomous',
      category: 'general',
      description: 'Helps patients with medication reminders and basic information',
      persona: 'Caring and reliable assistant focused on patient medication adherence and safety.',
      instructions: 'Provide medication reminders, basic drug information (non-prescriptive), and help track medication schedules. Never provide medical advice or dosage recommendations - always refer to healthcare providers.',
      tags: ['autonomus','medication', 'reminders', 'adherence'],
      complexity: 'beginner',
      icon: '💊'
    },
    {
      id: 'lab-results',
      name: 'Lab Results Assistant',
      type: 'Human in the Loop',
      category: 'general',
      description: 'Helps patients understand when lab results are available',
      persona: 'Professional and reassuring assistant who helps patients navigate lab result information.',
      instructions: 'Inform patients about lab result availability, explain the process for receiving results, and schedule follow-up appointments. Never interpret results - always direct patients to speak with their provider.',
      tags: ['human in the loop','lab results', 'follow-up', 'communication'],
      complexity: 'intermediate',
      icon: '🔬'
    }
  ];

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
  

  const categories = [
    { value: 'all', label: 'All Categories' },
    { value: 'billing', label: 'Billing & Insurance' },
    { value: 'front_desk', label: 'Front Desk' },
    { value: 'general', label: 'General Assistant' }
  ];

  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

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
