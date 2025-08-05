// Mock API Service with complete mock responses
class MockApiService {
  constructor() {
    this.baseUrl = 'http://localhost:8000';
    this.token = localStorage.getItem('token');
    
    // Mock data storage
    this.mockData = {
      users: [
        {
          id: 1,
          email: 'admin@springfielddental.com',
          full_name: 'Dr. Nancy Smith',
          practice_name: 'Springfield Dental Practice',
          role: 'admin',
          is_active: true
        },
        {
          id: 2,
          email: 'billing@test.com',
          full_name: 'Jane Smith',
          practice_name: 'Springfield Practice',
          role: 'billing',
          is_active: true
        },
        {
          id: 3,
          email: 'frontdesk@test.com',
          full_name: 'Mike Johnson',
          practice_name: 'Springfield Practice',
          role: 'front_desk',
          is_active: true
        }
      ],
      agents: [
        {
          id: 1,
          name: 'Billing Assistant',
          description: 'Helps with billing and insurance questions',
          role: 'billing',
          persona: 'Professional and helpful billing expert',
          instructions: 'Assist patients with billing inquiries and insurance questions',
          is_active: true,
          created_at: '2024-01-15T10:00:00Z'
        },
        {
          id: 2,
          name: 'Front Desk Assistant',
          description: 'Assists with appointment scheduling and general inquiries',
          role: 'front_desk',
          persona: 'Friendly and welcoming receptionist',
          instructions: 'Help patients schedule appointments and answer general questions',
          is_active: true,
          created_at: '2024-01-16T09:00:00Z'
        },
        {
          id: 3,
          name: 'General Assistant',
          description: 'Provides general practice information and assistance',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 4,
          name: 'Eligibility Assistant',
          description: 'Provides Insurance Eligibility Support',
          role: 'billing',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 5,
          name: 'PreAuthorization Assistant',
          description: 'Provides Insurance PreAuthorization Services',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 6,
          name: 'Coding and Notes Assistant',
          description: 'Provides review for insurance coding and notes preview',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 7,
          name: 'Claims Processing Assistant',
          description: 'Provides Claims Processing Support',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 8,
          name: 'Denials Management Assistant',
          description: 'Provides Denial Management Support',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 9,
          name: 'Payment Posting Assistant',
          description: 'Provides Payment Posting',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 10,
          name: 'RCM Analytics Assistant',
          description: 'Provides RCM Analytics Support',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 11,
          name: 'AP and AR  Assistant',
          description: 'Provides AP and AR Support',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 12,
          name: 'Patient Records Assistant',
          description: 'Provides Patient Records Managment Support',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 13,
          name: 'Patient Medication Assistant',
          description: 'Provides Patient Medication Management Support',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 14,
          name: 'Patient Wellness Assistant',
          description: 'Provides Overall health Support',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 15,
          name: 'Practionier Notes Assistant ',
          description: 'Provides support for Practioniers to manage notes',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        },
        {
          id: 16,
          name: 'Pateint Intake Assistant ',
          description: 'Provides patient intake support',
          role: 'general',
          persona: 'Knowledgeable and patient healthcare assistant',
          instructions: 'Provide general information about the practice and healthcare services',
          is_active: false,
          created_at: '2024-01-14T14:00:00Z'
        }
      ],
      knowledge: {
        1: [
          {
            id: 1,
            title: 'Insurance Policies Guide',
            content: 'Complete guide to understanding insurance policies and billing procedures...',
            source_type: 'document',
            agent_id: 1
          },
          {
            id: 2,
            title: 'Payment Processing Manual',
            content: 'Step-by-step instructions for processing patient payments...',
            source_type: 'document',
            agent_id: 1
          }
        ],
        2: [
          {
            id: 3,
            title: 'Appointment Scheduling Guide',
            content: 'Guidelines for scheduling patient appointments and managing calendar...',
            source_type: 'document',
            agent_id: 2
          }
        ],
        3: []
      }
    };
  }

  // Helper method to simulate API delay
  async mockDelay(ms = 500) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Helper method to get current user from token
  getCurrentUserFromToken() {
    if (!this.token) return null;
    
    // Extract user ID from mock token
    if (this.token.includes('billing')) {
      return this.mockData.users.find(u => u.role === 'billing');
    } else if (this.token.includes('frontdesk')) {
      return this.mockData.users.find(u => u.role === 'front_desk');
    } else {
      return this.mockData.users.find(u => u.role === 'admin');
    }
  }

  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    await this.mockDelay(1000);

    // Mock different scenarios based on email/password
    if (email === 'admin@test.com' && password === 'password123') {
      const token = 'mock_jwt_token_admin_' + Date.now();
      this.token = token;
      localStorage.setItem('token', token);
      return {
        access_token: token,
        token_type: 'bearer',
        expires_in: 3600
      };
    } else if (email === 'billing@test.com' && password === 'billing123') {
      const token = 'mock_jwt_token_billing_' + Date.now();
      this.token = token;
      localStorage.setItem('token', token);
      return {
        access_token: token,
        token_type: 'bearer',
        expires_in: 3600
      };
    } else if (email === 'frontdesk@test.com' && password === 'front123') {
      const token = 'mock_jwt_token_frontdesk_' + Date.now();
      this.token = token;
      localStorage.setItem('token', token);
      return {
        access_token: token,
        token_type: 'bearer',
        expires_in: 3600
      };
    } else {
      throw new Error('Login failed');
    }
  }

  async register(userData) {
    await this.mockDelay();
    
    // Check if email already exists
    if (this.mockData.users.some(u => u.email === userData.email)) {
      throw new Error('Email already registered');
    }

    const newUser = {
      id: this.mockData.users.length + 1,
      ...userData,
      is_active: true
    };
    
    this.mockData.users.push(newUser);
    return { message: 'User registered successfully' };
  }

  async getCurrentUser() {
    await this.mockDelay();
    
    if (!this.token) {
      throw new Error('No token provided');
    }

    const user = this.getCurrentUserFromToken();
    if (!user) {
      throw new Error('Invalid token');
    }

    return user;
  }

  async getAgents() {
    await this.mockDelay();
    
    if (!this.token) {
      throw new Error('Authentication required');
    }

    return [...this.mockData.agents];
  }

  async createAgent(agentData) {
    await this.mockDelay();
    
    if (!this.token) {
      throw new Error('Authentication required');
    }

    const newAgent = {
      id: this.mockData.agents.length + 1,
      ...agentData,
      is_active: true,
      created_at: new Date().toISOString()
    };

    this.mockData.agents.push(newAgent);
    this.mockData.knowledge[newAgent.id] = [];
    
    return newAgent;
  }

  async updateAgent(agentId, agentData) {
    await this.mockDelay();
    
    if (!this.token) {
      throw new Error('Authentication required');
    }

    const agentIndex = this.mockData.agents.findIndex(a => a.id === agentId);
    if (agentIndex === -1) {
      throw new Error('Agent not found');
    }

    this.mockData.agents[agentIndex] = {
      ...this.mockData.agents[agentIndex],
      ...agentData
    };

    return this.mockData.agents[agentIndex];
  }

  async deleteAgent(agentId) {
    await this.mockDelay();
    
    if (!this.token) {
      throw new Error('Authentication required');
    }

    const agentIndex = this.mockData.agents.findIndex(a => a.id === agentId);
    if (agentIndex === -1) {
      throw new Error('Agent not found');
    }

    this.mockData.agents.splice(agentIndex, 1);
    delete this.mockData.knowledge[agentId];
    
    return { message: 'Agent deleted successfully' };
  }

  async chatWithAgent(agentId, message) {
    await this.mockDelay(1500); // Longer delay for chat responses
    
    if (!this.token) {
      throw new Error('Authentication required');
    }

    const agent = this.mockData.agents.find(a => a.id === agentId);
    if (!agent) {
      throw new Error('Agent not found');
    }

    // Mock responses based on agent role and message content
    let response = '';
    let confidence = 0.85;

    if (agent.role === 'billing') {
      if (message.toLowerCase().includes('insurance')) {
        response = "I can help you with insurance questions. Our practice accepts most major insurance plans including Blue Cross Blue Shield, Aetna, and United Healthcare. Would you like me to check your specific coverage?";
        confidence = 0.92;
      } else if (message.toLowerCase().includes('payment') || message.toLowerCase().includes('bill')) {
        response = "For payment inquiries, I can help you understand your statement or set up a payment plan. We accept cash, credit cards, and offer monthly payment options for larger balances.";
        confidence = 0.89;
      } else {
        response = "I'm here to help with billing and insurance questions. Is there something specific about your account or insurance coverage you'd like to know?";
        confidence = 0.75;
      }
    } else if (agent.role === 'front_desk') {
      if (message.toLowerCase().includes('appointment')) {
        response = "I'd be happy to help you schedule an appointment! Our available time slots this week are Monday 2:00 PM, Wednesday 10:00 AM, and Friday 3:30 PM. Which would work best for you?";
        confidence = 0.94;
      } else if (message.toLowerCase().includes('hours') || message.toLowerCase().includes('open')) {
        response = "Our office hours are Monday through Friday, 8:00 AM to 5:00 PM. We're closed on weekends and major holidays. Is there anything else you'd like to know?";
        confidence = 0.96;
      } else {
        response = "Welcome! I'm here to help with scheduling appointments and general practice information. How can I assist you today?";
        confidence = 0.80;
      }
    } else {
      response = "Hello! I'm a general practice assistant. I can provide information about our services, policies, and general healthcare guidance. What would you like to know?";
      confidence = 0.78;
    }

    return { response, confidence };
  }

  async getKnowledgeBase(agentId) {
    await this.mockDelay();
    
    if (!this.token) {
      throw new Error('Authentication required');
    }

    return this.mockData.knowledge[agentId] || [];
  }

  async uploadDocument(agentId, file) {
    await this.mockDelay(2000); // Longer delay for file upload
    
    if (!this.token) {
      throw new Error('Authentication required');
    }

    if (!this.mockData.knowledge[agentId]) {
      this.mockData.knowledge[agentId] = [];
    }

    const newDocument = {
      id: Date.now(),
      title: file.name,
      content: `This is the content of ${file.name}. In a real implementation, this would be the extracted text from the uploaded file...`,
      source_type: 'document',
      agent_id: agentId,
      uploaded_at: new Date().toISOString()
    };

    this.mockData.knowledge[agentId].push(newDocument);
    
    return { 
      message: 'Document uploaded successfully',
      document: newDocument 
    };
  }

  logout() {
    this.token = null;
    localStorage.removeItem('token');
  }
}

export const api = new MockApiService();
