// Enhanced Agent Service with Agentic Core Integration
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[Agentic] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[Agentic] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('[Agentic] Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

class AgenticService {
  constructor(config = {}) {
    this.config = {
      apiUrl: API_BASE_URL,
      userId: config.userId || 'default_user',
      model: config.model || 'gpt-4',
      ...config
    };
  }

  // Enhanced Chat Methods
  async chat(message, userId = this.config.userId, context = {}) {
    try {
      const response = await apiClient.post('/api/agent/chat', {
        message,
        user_id: userId,
        context
      });
      return response.data;
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  }

  async chatWithClaimsContext(message, userId = this.config.userId, claimContext = {}) {
    try {
      const context = {
        ...claimContext,
        claims_processing: true,
        timestamp: new Date().toISOString()
      };

      const response = await apiClient.post('/api/agent/chat', {
        message,
        user_id: userId,
        context
      });
      return response.data;
    } catch (error) {
      console.error('Claims chat error:', error);
      throw error;
    }
  }

  // Enhanced Task Processing
  async processTask(taskType, taskDescription, userId = this.config.userId, context = {}) {
    try {
      const response = await apiClient.post('/api/agent/tasks', {
        task_type: taskType,
        user_id: userId,
        task_description: taskDescription,
        context
      });
      return response.data;
    } catch (error) {
      console.error('Task processing error:', error);
      throw error;
    }
  }

  // Claims-Specific Methods
  async analyzeClaim(claimId, userId = this.config.userId) {
    try {
      const response = await apiClient.post(`/api/agent/tasks/analyze-claim/${claimId}`, {
        user_id: userId
      });
      return response.data;
    } catch (error) {
      console.error('Claim analysis error:', error);
      throw error;
    }
  }

  async processRejection(claimId, userId = this.config.userId) {
    try {
      const response = await apiClient.post(`/api/agent/tasks/process-rejection/${claimId}`, {
        user_id: userId
      });
      return response.data;
    } catch (error) {
      console.error('Rejection processing error:', error);
      throw error;
    }
  }

  async generateReport(reportType, userId = this.config.userId, context = {}) {
    try {
      const response = await apiClient.post('/api/agent/tasks/generate-report', {
        report_type: reportType,
        user_id: userId,
        context
      });
      return response.data;
    } catch (error) {
      console.error('Report generation error:', error);
      throw error;
    }
  }

  async searchClaims(searchCriteria, userId = this.config.userId) {
    try {
      const response = await apiClient.post('/api/agent/tasks', {
        task_type: 'search_claims',
        user_id: userId,
        task_description: 'Search claims with specified criteria',
        context: { filters: searchCriteria }
      });
      return response.data;
    } catch (error) {
      console.error('Claims search error:', error);
      throw error;
    }
  }

  // Batch Processing
  async processBatchTasks(tasks, userId = this.config.userId, maxConcurrent = 3) {
    try {
      const response = await apiClient.post('/api/agent/batch-tasks', {
        tasks,
        user_id: userId,
        max_concurrent: maxConcurrent
      });
      return response.data;
    } catch (error) {
      console.error('Batch processing error:', error);
      throw error;
    }
  }

  // Task Management
  async getTaskStatus(taskId) {
    try {
      const response = await apiClient.get(`/api/agent/tasks/${taskId}/status`);
      return response.data;
    } catch (error) {
      console.error('Get task status error:', error);
      throw error;
    }
  }

  async getActiveTasks() {
    try {
      const response = await apiClient.get('/api/agent/tasks/active');
      return response.data;
    } catch (error) {
      console.error('Get active tasks error:', error);
      throw error;
    }
  }

  async cleanupOldTasks(maxAgeHours = 24) {
    try {
      const response = await apiClient.post('/api/agent/tasks/cleanup', {
        max_age_hours: maxAgeHours
      });
      return response.data;
    } catch (error) {
      console.error('Cleanup tasks error:', error);
      throw error;
    }
  }

  // Tools and Capabilities
  async getAvailableTools() {
    try {
      const response = await apiClient.get('/api/agent/tools');
      return response.data;
    } catch (error) {
      console.error('Get tools error:', error);
      throw error;
    }
  }

  // Health and Monitoring
  async getAgentHealth() {
    try {
      const response = await apiClient.get('/api/agent/health');
      return response.data;
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }

  async getPerformanceMetrics(hoursBack = 24) {
    try {
      const response = await apiClient.get(`/api/agent/metrics/performance?hours_back=${hoursBack}`);
      return response.data;
    } catch (error) {
      console.error('Performance metrics error:', error);
      throw error;
    }
  }

  async getRealtimeMetrics() {
    try {
      const response = await apiClient.get('/api/agent/metrics/realtime');
      return response.data;
    } catch (error) {
      console.error('Realtime metrics error:', error);
      throw error;
    }
  }

  async getToolUsageMetrics() {
    try {
      const response = await apiClient.get('/api/agent/metrics/tools');
      return response.data;
    } catch (error) {
      console.error('Tool usage metrics error:', error);
      throw error;
    }
  }

  // Conversation Management
  async getConversationHistory(userId = this.config.userId, limit = 50, offset = 0) {
    try {
      const response = await apiClient.get(`/api/agent/conversations/${userId}?limit=${limit}&offset=${offset}`);
      return response.data;
    } catch (error) {
      console.error('Get conversation history error:', error);
      throw error;
    }
  }

  async clearConversationHistory(userId = this.config.userId) {
    try {
      const response = await apiClient.delete(`/api/agent/conversations/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Clear conversation history error:', error);
      throw error;
    }
  }

  // Claims Processing Specific Methods
  async getClaimsData(userId = this.config.userId) {
    try {
      const response = await apiClient.get('/api/claims', {
        params: { user_id: userId }
      });
      return response.data;
    } catch (error) {
      console.error('Get claims data error:', error);
      throw error;
    }
  }

  async getClaimById(claimId) {
    try {
      const response = await apiClient.get(`/api/claims/${claimId}`);
      return response.data;
    } catch (error) {
      console.error('Get claim by ID error:', error);
      throw error;
    }
  }

  async createClaim(claimData) {
    try {
      const response = await apiClient.post('/api/claims', claimData);
      return response.data;
    } catch (error) {
      console.error('Create claim error:', error);
      throw error;
    }
  }

  async updateClaim(claimId, claimData) {
    try {
      const response = await apiClient.put(`/api/claims/${claimId}`, claimData);
      return response.data;
    } catch (error) {
      console.error('Update claim error:', error);
      throw error;
    }
  }

  async deleteClaim(claimId) {
    try {
      const response = await apiClient.delete(`/api/claims/${claimId}`);
      return response.data;
    } catch (error) {
      console.error('Delete claim error:', error);
      throw error;
    }
  }

  async getRejections(userId = this.config.userId) {
    try {
      const response = await apiClient.get('/api/rejections', {
        params: { user_id: userId }
      });
      return response.data;
    } catch (error) {
      console.error('Get rejections error:', error);
      throw error;
    }
  }

  async getRejectionById(rejectionId) {
    try {
      const response = await apiClient.get(`/api/rejections/${rejectionId}`);
      return response.data;
    } catch (error) {
      console.error('Get rejection by ID error:', error);
      throw error;
    }
  }

  async getReports(userId = this.config.userId) {
    try {
      const response = await apiClient.get('/api/reports', {
        params: { user_id: userId }
      });
      return response.data;
    } catch (error) {
      console.error('Get reports error:', error);
      throw error;
    }
  }

  async getReportById(reportId) {
    try {
      const response = await apiClient.get(`/api/reports/${reportId}`);
      return response.data;
    } catch (error) {
      console.error('Get report by ID error:', error);
      throw error;
    }
  }

  // Utility Methods
  async testConnection() {
    try {
      const response = await apiClient.get('/api/agent/health');
      return response.status === 200;
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }

  // Configuration
  updateConfig(newConfig) {
    this.config = { ...this.config, ...newConfig };
  }

  getConfig() {
    return { ...this.config };
  }
}

// Legacy compatibility functions
export const agentService = {
  // Chat methods
  chat: (message, userId, context) => {
    const service = new AgenticService({ userId });
    return service.chat(message, userId, context);
  },

  // Task methods
  createTask: (taskType, description, userId, context) => {
    const service = new AgenticService({ userId });
    return service.processTask(taskType, description, userId, context);
  },

  analyzeClaim: (claimId, userId) => {
    const service = new AgenticService({ userId });
    return service.analyzeClaim(claimId, userId);
  },

  processRejection: (claimId, userId) => {
    const service = new AgenticService({ userId });
    return service.processRejection(claimId, userId);
  },

  generateReport: (reportType, userId, context) => {
    const service = new AgenticService({ userId });
    return service.generateReport(reportType, userId, context);
  },

  // Claims data methods
  getClaimsData: (userId) => {
    const service = new AgenticService({ userId });
    return service.getClaimsData(userId);
  },

  getClaimById: (claimId) => {
    const service = new AgenticService();
    return service.getClaimById(claimId);
  },

  createClaim: (claimData) => {
    const service = new AgenticService();
    return service.createClaim(claimData);
  },

  updateClaim: (claimId, claimData) => {
    const service = new AgenticService();
    return service.updateClaim(claimId, claimData);
  },

  deleteClaim: (claimId) => {
    const service = new AgenticService();
    return service.deleteClaim(claimId);
  },

  // Utility methods
  getAvailableTools: () => {
    const service = new AgenticService();
    return service.getAvailableTools();
  },

  getAgentHealth: () => {
    const service = new AgenticService();
    return service.getAgentHealth();
  },

  getPerformanceMetrics: (hoursBack) => {
    const service = new AgenticService();
    return service.getPerformanceMetrics(hoursBack);
  },

  getRealtimeMetrics: () => {
    const service = new AgenticService();
    return service.getRealtimeMetrics();
  },

  getToolUsageMetrics: () => {
    const service = new AgenticService();
    return service.getToolUsageMetrics();
  },

  getTaskStatus: (taskId) => {
    const service = new AgenticService();
    return service.getTaskStatus(taskId);
  },

  getActiveTasks: () => {
    const service = new AgenticService();
    return service.getActiveTasks();
  },

  // Mock responses for development (when API is not available)
  getMockResponse: (type) => {
    const mockResponses = {
      chat: {
        task_id: 'mock_chat_001',
        task_type: 'chat',
        status: 'completed',
        response: 'This is a mock response from the AI agent. The system is working correctly.',
        result: {
          confidence: 0.95,
          processing_time: 1.2
        },
        created_at: new Date().toISOString(),
        completed_at: new Date().toISOString()
      },
      claim_analysis: {
        task_id: 'mock_analysis_001',
        task_type: 'analyze_claim',
        status: 'completed',
        response: 'Claim analysis completed successfully',
        result: {
          claim_id: '12345',
          analysis: {
            issues_found: 2,
            recommendations: [
              'Verify patient eligibility',
              'Check diagnosis codes'
            ],
            confidence_score: 0.88
          }
        },
        created_at: new Date().toISOString(),
        completed_at: new Date().toISOString()
      },
      rejection_analysis: {
        task_id: 'mock_rejection_001',
        task_type: 'analyze_rejection',
        status: 'completed',
        response: 'Rejection analysis completed',
        result: {
          claim_id: '12345',
          rejection_reason: 'Invalid diagnosis code',
          suggested_fixes: [
            'Update diagnosis code to valid ICD-10 code',
            'Add supporting documentation'
          ],
          resubmission_ready: true,
          confidence_score: 0.92
        },
        created_at: new Date().toISOString(),
        completed_at: new Date().toISOString()
      }
    };

    return mockResponses[type] || mockResponses.chat;
  }
};

// Export the main service class
export { AgenticService };

// Export default instance
export default new AgenticService(); 