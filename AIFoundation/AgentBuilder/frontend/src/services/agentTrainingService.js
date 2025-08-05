// Agent Training Service
class AgentTrainingService {
  constructor() {
    this.baseUrl = 'http://localhost:8000';
  }

  // Mock agents data
  getAgents() {
    return [
      {
        id: 1,
        name: "Billing Support Bot",
        template: "billing",
        status: "active",
        trainingStatus: "trained",
        accuracy: 94,
        lastTrained: "2025-01-25",
        trainingData: 15420,
        conversations: 1247
      },
      {
        id: 2,
        name: "Front Desk Assistant",
        template: "reception",
        status: "active",
        trainingStatus: "training",
        accuracy: 89,
        lastTrained: "2025-01-28",
        trainingData: 8932,
        conversations: 892
      },
      {
        id: 3,
        name: "Sales Consultant",
        template: "sales",
        status: "paused",
        trainingStatus: "needs_training",
        accuracy: 72,
        lastTrained: "2025-01-15",
        trainingData: 3421,
        conversations: 543
      }
    ];
  }

  // AI Models
  getAIModels() {
    return [
      {
        id: 'apurv-ops-1',
        name: 'Apurv-Ops-1',
        description: 'General purpose operations model'
      },
      {
        id: 'apurv-ops-2',
        name: 'Apurv-Ops-2',
        description: 'Enhanced operations model'
      },
      {
        id: 'apurv-ops-3',
        name: 'Apurv-Ops-3',
        description: 'Advanced operations model'
      }
    ];
  }

  // Data source options with EHR integrations
  getDataSourceOptions() {
    return [
      {
        category: "EHR Systems",
        sources: [
          { id: 'epic', name: 'Epic', type: 'ehr', icon: 'Database', status: 'connected' },
          { id: 'cerner', name: 'Cerner (Oracle Health)', type: 'ehr', icon: 'Database', status: 'available' },
          { id: 'allscripts', name: 'Allscripts', type: 'ehr', icon: 'Database', status: 'available' },
          { id: 'athenahealth', name: 'athenahealth', type: 'ehr', icon: 'Database', status: 'connected' },
          { id: 'eclinicalworks', name: 'eClinicalWorks', type: 'ehr', icon: 'Database', status: 'available' }
        ]
      },
      {
        category: "Practice Management",
        sources: [
          { id: 'change_healthcare', name: 'Change Healthcare', type: 'clearinghouse', icon: 'CreditCard', status: 'connected' },
          { id: 'availity', name: 'Availity', type: 'clearinghouse', icon: 'CreditCard', status: 'available' },
          { id: 'surescripts', name: 'Surescripts', type: 'prescription', icon: 'FileText', status: 'connected' }
        ]
      },
      {
        category: "Business Systems",
        sources: [
          { id: 'quickbooks', name: 'QuickBooks', type: 'accounting', icon: 'BarChart3', status: 'connected' },
          { id: 'salesforce', name: 'Salesforce CRM', type: 'crm', icon: 'Users', status: 'available' },
          { id: 'calendar', name: 'Google Calendar', type: 'scheduling', icon: 'Calendar', status: 'connected' }
        ]
      },
      {
        category: "Communication",
        sources: [
          { id: 'gmail', name: 'Gmail', type: 'email', icon: 'Mail', status: 'connected' },
          { id: 'slack', name: 'Slack', type: 'messaging', icon: 'Phone', status: 'available' },
          { id: 'zendesk', name: 'Zendesk', type: 'support', icon: 'Settings', status: 'available' }
        ]
      }
    ];
  }

  // Simulate URL scraping
  async scrapeUrl(url) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    return {
      id: Date.now(),
      url: url,
      title: `Data from ${new URL(url).hostname}`,
      pages: Math.floor(Math.random() * 50) + 10,
      dataPoints: Math.floor(Math.random() * 1000) + 500,
      status: 'completed',
      scrapedAt: new Date().toISOString(),
      content: [
        'FAQ sections',
        'Product descriptions',
        'Service information',
        'Contact details',
        'Policy documents'
      ]
    };
  }

  // Simulate training
  async startTraining(agentId, trainingConfig) {
    return new Promise((resolve) => {
      let progress = 0;
      const interval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress >= 100) {
          clearInterval(interval);
          resolve({
            success: true,
            trainingId: `train-${Date.now()}`,
            accuracy: Math.random() * 20 + 80 // 80-100% accuracy
          });
        }
      }, 500);
    });
  }

  // Get training history
  getTrainingHistory(agentId) {
    return [
      { date: '2025-01-28', type: 'Full Training', duration: '2h 34m', accuracy: 94, dataPoints: 15420 },
      { date: '2025-01-25', type: 'Incremental', duration: '45m', accuracy: 92, dataPoints: 3200 },
      { date: '2025-01-20', type: 'Full Training', duration: '3h 12m', accuracy: 89, dataPoints: 12100 },
      { date: '2025-01-15', type: 'Data Import', duration: '1h 20m', accuracy: 85, dataPoints: 8900 }
    ];
  }

  // Get training status colors
  getTrainingStatusColors() {
    return {
      'trained': 'text-green-600 bg-green-100',
      'training': 'text-blue-600 bg-blue-100',
      'needs_training': 'text-orange-600 bg-orange-100'
    };
  }

  // Get connection status colors
  getConnectionStatusColors() {
    return {
      'connected': 'text-green-600 bg-green-100',
      'available': 'text-gray-600 bg-gray-100',
      'error': 'text-red-600 bg-red-100'
    };
  }
}

export default new AgentTrainingService(); 