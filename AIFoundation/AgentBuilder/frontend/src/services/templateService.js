// Template Service - Centralized template definitions
class TemplateService {
  constructor() {
    this.baseUrl = 'http://localhost:8000';
  }

  // Centralized template definitions aligned with templates section
  getAgentTemplates() {
    return [
      {
        id: 'billing-specialist',
        name: 'Billing Specialist',
        type: 'Autonomous',
        category: 'billing',
        description: 'Handles insurance claims, payment inquiries, and billing questions',
        persona: 'Professional and detail-oriented billing specialist with expertise in medical billing and insurance processes.',
        instructions: 'Assist patients and staff with billing inquiries, insurance verification, payment processing, and claims status. Always maintain HIPAA compliance and refer complex cases to human staff.',
        tags: ['autonomous', 'billing', 'insurance', 'payments'],
        complexity: 'intermediate',
        icon: '💰',
        defaultPersona: 'Professional & Detail-oriented',
        defaultTone: 'Formal',
        features: ['Payment Processing', 'Invoice Management', 'Account Updates', 'Insurance Verification']
      },
      {
        id: 'appointment-scheduler',
        name: 'Appointment Scheduler',
        type: 'Human in the Loop',
        category: 'front_desk',
        description: 'Manages appointment scheduling, cancellations, and rescheduling',
        persona: 'Friendly and efficient front desk assistant focused on patient convenience and schedule optimization.',
        instructions: 'Help patients schedule, reschedule, or cancel appointments. Check availability, confirm patient information, and send appointment reminders. Always verify patient identity before accessing information.',
        tags: ['human in the loop', 'scheduling', 'appointments', 'calendar'],
        complexity: 'beginner',
        icon: '📅',
        defaultPersona: 'Friendly & Efficient',
        defaultTone: 'Casual',
        features: ['Appointment Scheduling', 'Visitor Management', 'Information Desk', 'Calendar Management']
      },
      {
        id: 'patient-intake',
        name: 'Patient Intake Assistant',
        type: 'Autonomous',
        category: 'front_desk',
        description: 'Guides new patients through intake process and form completion',
        persona: 'Welcoming and patient guide who helps new patients feel comfortable while ensuring complete information collection.',
        instructions: 'Assist new patients with intake forms, explain office policies, collect insurance information, and guide them through the registration process. Ensure all required information is collected while maintaining a friendly demeanor.',
        tags: ['autonomous', 'intake', 'registration', 'new patients'],
        complexity: 'intermediate',
        icon: '👋',
        defaultPersona: 'Welcoming & Patient',
        defaultTone: 'Friendly',
        features: ['Patient Registration', 'Form Completion', 'Policy Explanation', 'Information Collection']
      },
      {
        id: 'insurance-verifier',
        name: 'Insurance Verification',
        type: 'Autonomous',
        category: 'billing',
        description: 'Verifies insurance coverage and benefits for patients',
        persona: 'Thorough and knowledgeable insurance specialist who ensures accurate coverage verification.',
        instructions: 'Verify patient insurance coverage, check benefits, confirm copays and deductibles, and explain coverage limitations. Always use current insurance information and escalate complex verification issues.',
        tags: ['autonomous', 'insurance', 'verification', 'benefits'],
        complexity: 'advanced',
        icon: '🛡️',
        defaultPersona: 'Thorough & Knowledgeable',
        defaultTone: 'Professional',
        features: ['Insurance Verification', 'Benefits Checking', 'Coverage Analysis', 'Claims Processing']
      },
      {
        id: 'medication-reminder',
        name: 'Medication Reminder',
        type: 'Autonomous',
        category: 'general',
        description: 'Helps patients with medication reminders and basic information',
        persona: 'Caring and reliable assistant focused on patient medication adherence and safety.',
        instructions: 'Provide medication reminders, basic drug information (non-prescriptive), and help track medication schedules. Never provide medical advice or dosage recommendations - always refer to healthcare providers.',
        tags: ['autonomous', 'medication', 'reminders', 'adherence'],
        complexity: 'beginner',
        icon: '💊',
        defaultPersona: 'Caring & Reliable',
        defaultTone: 'Supportive',
        features: ['Medication Reminders', 'Schedule Tracking', 'Basic Information', 'Adherence Support']
      },
      {
        id: 'lab-results',
        name: 'Lab Results Assistant',
        type: 'Human in the Loop',
        category: 'general',
        description: 'Helps patients understand when lab results are available',
        persona: 'Professional and reassuring assistant who helps patients navigate lab result information.',
        instructions: 'Inform patients about lab result availability, explain the process for receiving results, and schedule follow-up appointments. Never interpret results - always direct patients to speak with their provider.',
        tags: ['human in the loop', 'lab results', 'follow-up', 'communication'],
        complexity: 'intermediate',
        icon: '🔬',
        defaultPersona: 'Professional & Reassuring',
        defaultTone: 'Informative',
        features: ['Result Notifications', 'Process Explanation', 'Follow-up Scheduling', 'Communication Management']
      }
    ];
  }

  // Get templates by category
  getTemplatesByCategory(category) {
    return this.getAgentTemplates().filter(template => template.category === category);
  }

  // Get template by ID
  getTemplateById(id) {
    return this.getAgentTemplates().find(template => template.id === id);
  }

  // Get all categories
  getCategories() {
    const categories = [
      { value: 'all', label: 'All Categories' },
      { value: 'billing', label: 'Billing & Insurance' },
      { value: 'front_desk', label: 'Front Desk' },
      { value: 'general', label: 'General Assistant' }
    ];
    return categories;
  }

  // Get agent types
  getAgentTypes() {
    return [
      { value: 'all', label: 'All Types' },
      { value: 'autonomous', label: 'Autonomous' },
      { value: 'human_in_loop', label: 'Human in the Loop' }
    ];
  }

  // Get complexity levels
  getComplexityLevels() {
    return [
      { value: 'all', label: 'All Levels' },
      { value: 'beginner', label: 'Beginner' },
      { value: 'intermediate', label: 'Intermediate' },
      { value: 'advanced', label: 'Advanced' }
    ];
  }

  // Get persona options (aligned with templates)
  getPersonaOptions() {
    return [
      'Professional & Detail-oriented',
      'Friendly & Efficient',
      'Welcoming & Patient',
      'Thorough & Knowledgeable',
      'Caring & Reliable',
      'Professional & Reassuring',
      'Energetic & Motivating',
      'Calm & Reassuring'
    ];
  }

  // Get tone options (aligned with templates)
  getToneOptions() {
    return [
      'Formal',
      'Casual',
      'Friendly',
      'Professional',
      'Supportive',
      'Informative',
      'Conversational',
      'Empathetic'
    ];
  }

  // Get integration options (same as AgentBuilding.jsx)
  getIntegrationOptions() {
    return {
      ehrIntegration: [
        { value: 'none', label: 'None' },
        { value: 'epic', label: 'Epic' },
        { value: 'cerner', label: 'Cerner (Oracle Health)' },
        { value: 'allscripts', label: 'Allscripts' },
        { value: 'athenahealth', label: 'athenahealth' },
        { value: 'eclinicalworks', label: 'eClinicalWorks' },
        { value: 'nextgen', label: 'NextGen Healthcare' },
        { value: 'practice_fusion', label: 'Practice Fusion' },
        { value: 'custom', label: 'Custom EHR' }
      ],
      clearingHouse: [
        { value: 'none', label: 'None' },
        { value: 'change_healthcare', label: 'Change Healthcare' },
        { value: 'availity', label: 'Availity' },
        { value: 'relay_health', label: 'Relay Health' },
        { value: 'waystar', label: 'Waystar' },
        { value: 'navicure', label: 'Navicure' },
        { value: 'office_ally', label: 'Office Ally' },
        { value: 'clearinghouse_custom', label: 'Custom Clearing House' }
      ],
      ePrescription: [
        { value: 'none', label: 'None' },
        { value: 'surescripts', label: 'Surescripts' },
        { value: 'newcrop', label: 'NewCrop' },
        { value: 'drfirst', label: 'DrFirst' },
        { value: 'imprivata', label: 'Imprivata' },
        { value: 'allscripts_eprescribe', label: 'Allscripts ePrescribe' },
        { value: 'epic_eprescribe', label: 'Epic E-Prescribing' },
        { value: 'custom_erx', label: 'Custom E-Rx System' }
      ],
      accountingSystem: [
        { value: 'none', label: 'None' },
        { value: 'quickbooks', label: 'QuickBooks' },
        { value: 'sage', label: 'Sage' },
        { value: 'xero', label: 'Xero' },
        { value: 'freshbooks', label: 'FreshBooks' },
        { value: 'netsuite', label: 'NetSuite' },
        { value: 'peachtree', label: 'Peachtree' },
        { value: 'wave', label: 'Wave Accounting' },
        { value: 'custom_accounting', label: 'Custom Accounting System' }
      ],
      mobileIntegration: [
        { value: 'none', label: 'None' },
        { value: 'apple_health_ios', label: 'Apple Health (iOS)' },
        { value: 'google_fit_android', label: 'Google Fit (Android)' },
        { value: 'samsung_health_android', label: 'Samsung Health (Android)' },
        { value: 'fitbit_cross', label: 'Fitbit (iOS/Android)' },
        { value: 'garmin_cross', label: 'Garmin Connect (iOS/Android)' },
        { value: 'strava_cross', label: 'Strava (iOS/Android)' },
        { value: 'myfitnesspal_cross', label: 'MyFitnessPal (iOS/Android)' },
        { value: 'withings_cross', label: 'Withings Health Mate (iOS/Android)' },
        { value: 'polar_cross', label: 'Polar Flow (iOS/Android)' },
        { value: 'suunto_cross', label: 'Suunto App (iOS/Android)' },
        { value: 'oura_cross', label: 'Oura Ring (iOS/Android)' },
        { value: 'whoop_cross', label: 'WHOOP (iOS/Android)' },
        { value: 'custom_ios', label: 'Custom iOS Health App' },
        { value: 'custom_android', label: 'Custom Android Health App' },
        { value: 'custom_cross', label: 'Custom Cross-Platform Health App' }
      ]
    };
  }

  // Filter templates based on search and category
  filterTemplates(templates, searchTerm, selectedCategory) {
    return templates.filter(template => {
      const matchesSearch = template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           template.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           template.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
      const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }
}

export default new TemplateService(); 