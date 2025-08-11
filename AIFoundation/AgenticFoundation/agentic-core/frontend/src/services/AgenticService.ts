import axios, { AxiosInstance, AxiosResponse } from 'axios';

export interface AgenticConfig {
  apiUrl: string;
  userId: string;
  model: string;
  theme: 'light' | 'dark';
  position?: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  showQuickActions?: boolean;
  enableHistory?: boolean;
  enableMetrics?: boolean;
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'agent';
  content: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
}

export interface Task {
  id: string;
  type: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  data: Record<string, any>;
  result?: Record<string, any>;
  createdAt: Date;
  completedAt?: Date;
}

export interface AgentResponse {
  taskId: string;
  taskType: string;
  status: string;
  response: string;
  result?: Record<string, any>;
  createdAt: Date;
  completedAt?: Date;
}

export class AgenticService {
  private config: AgenticConfig;
  private apiClient: AxiosInstance;

  constructor(config: Partial<AgenticConfig> = {}) {
    this.config = {
      apiUrl: 'http://localhost:8000',
      userId: 'default_user',
      model: 'gpt-4',
      theme: 'light',
      position: 'bottom-right',
      showQuickActions: true,
      enableHistory: true,
      enableMetrics: true,
      ...config
    };

    this.apiClient = axios.create({
      baseURL: this.config.apiUrl,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor for logging
    this.apiClient.interceptors.request.use(
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
    this.apiClient.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        console.error('[Agentic] Response error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Chat Methods
  async chat(message: string, userId?: string, context?: Record<string, any>): Promise<AgentResponse> {
    try {
      const response = await this.apiClient.post('/api/agent/chat', {
        message,
        user_id: userId || this.config.userId,
        context: context || {}
      });
      return response.data;
    } catch (error) {
      console.error('Chat error:', error);
      throw error;
    }
  }

  async chatWithClaimsContext(message: string, userId?: string, claimContext?: Record<string, any>): Promise<AgentResponse> {
    try {
      const context = {
        ...claimContext,
        claims_processing: true,
        timestamp: new Date().toISOString()
      };

      const response = await this.apiClient.post('/api/agent/chat', {
        message,
        user_id: userId || this.config.userId,
        context
      });
      return response.data;
    } catch (error) {
      console.error('Claims chat error:', error);
      throw error;
    }
  }

  // Task Processing
  async processTask(taskType: string, taskDescription: string, userId?: string, context?: Record<string, any>): Promise<AgentResponse> {
    try {
      const response = await this.apiClient.post('/api/agent/tasks', {
        task_type: taskType,
        user_id: userId || this.config.userId,
        task_description: taskDescription,
        context: context || {}
      });
      return response.data;
    } catch (error) {
      console.error('Task processing error:', error);
      throw error;
    }
  }

  // Claims-Specific Methods
  async analyzeClaim(claimId: string, userId?: string): Promise<AgentResponse> {
    try {
      const response = await this.apiClient.post(`/api/agent/tasks/analyze-claim/${claimId}`, {
        user_id: userId || this.config.userId
      });
      return response.data;
    } catch (error) {
      console.error('Claim analysis error:', error);
      throw error;
    }
  }

  async processRejection(claimId: string, userId?: string): Promise<AgentResponse> {
    try {
      const response = await this.apiClient.post(`/api/agent/tasks/process-rejection/${claimId}`, {
        user_id: userId || this.config.userId
      });
      return response.data;
    } catch (error) {
      console.error('Rejection processing error:', error);
      throw error;
    }
  }

  async generateReport(reportType: string, userId?: string, context?: Record<string, any>): Promise<AgentResponse> {
    try {
      const response = await this.apiClient.post('/api/agent/tasks/generate-report', {
        report_type: reportType,
        user_id: userId || this.config.userId,
        context: context || {}
      });
      return response.data;
    } catch (error) {
      console.error('Report generation error:', error);
      throw error;
    }
  }

  async searchClaims(searchCriteria: Record<string, any>, userId?: string): Promise<AgentResponse> {
    try {
      const response = await this.apiClient.post('/api/agent/tasks', {
        task_type: 'search_claims',
        user_id: userId || this.config.userId,
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
  async processBatchTasks(tasks: Array<{ type: string; description: string; context?: Record<string, any> }>, userId?: string, maxConcurrent: number = 3): Promise<AgentResponse[]> {
    try {
      const response = await this.apiClient.post('/api/agent/batch-tasks', {
        tasks,
        user_id: userId || this.config.userId,
        max_concurrent: maxConcurrent
      });
      return response.data;
    } catch (error) {
      console.error('Batch processing error:', error);
      throw error;
    }
  }

  // Task Management
  async getTaskStatus(taskId: string): Promise<AgentResponse> {
    try {
      const response = await this.apiClient.get(`/api/agent/tasks/${taskId}/status`);
      return response.data;
    } catch (error) {
      console.error('Get task status error:', error);
      throw error;
    }
  }

  async getActiveTasks(): Promise<Task[]> {
    try {
      const response = await this.apiClient.get('/api/agent/tasks/active');
      return response.data;
    } catch (error) {
      console.error('Get active tasks error:', error);
      throw error;
    }
  }

  async cleanupOldTasks(maxAgeHours: number = 24): Promise<{ deleted: number }> {
    try {
      const response = await this.apiClient.post('/api/agent/tasks/cleanup', {
        max_age_hours: maxAgeHours
      });
      return response.data;
    } catch (error) {
      console.error('Cleanup tasks error:', error);
      throw error;
    }
  }

  // Tools and Capabilities
  async getAvailableTools(): Promise<Array<{ name: string; description: string; type: string; parameters?: Record<string, any> }>> {
    try {
      const response = await this.apiClient.get('/api/agent/tools');
      return response.data;
    } catch (error) {
      console.error('Get tools error:', error);
      throw error;
    }
  }

  // Health and Monitoring
  async getAgentHealth(): Promise<{ status: string; timestamp: string; version: string; [key: string]: any }> {
    try {
      const response = await this.apiClient.get('/api/agent/health');
      return response.data;
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }

  async getPerformanceMetrics(hoursBack: number = 24): Promise<{ total_requests: number; average_response_time: number; success_rate: number; [key: string]: any }> {
    try {
      const response = await this.apiClient.get(`/api/agent/metrics/performance?hours_back=${hoursBack}`);
      return response.data;
    } catch (error) {
      console.error('Performance metrics error:', error);
      throw error;
    }
  }

  async getRealtimeMetrics(): Promise<{ active_tasks: number; completed_tasks: number; error_rate: number; [key: string]: any }> {
    try {
      const response = await this.apiClient.get('/api/agent/metrics/realtime');
      return response.data;
    } catch (error) {
      console.error('Realtime metrics error:', error);
      throw error;
    }
  }

  async getToolUsageMetrics(): Promise<Record<string, { total_executions: number; successful_executions: number; failed_executions: number; [key: string]: any }>> {
    try {
      const response = await this.apiClient.get('/api/agent/metrics/tools');
      return response.data;
    } catch (error) {
      console.error('Tool usage metrics error:', error);
      throw error;
    }
  }

  // Conversation Management
  async getConversationHistory(userId?: string, limit: number = 50, offset: number = 0): Promise<Conversation[]> {
    try {
      const response = await this.apiClient.get(`/api/agent/conversations/${userId || this.config.userId}?limit=${limit}&offset=${offset}`);
      return response.data;
    } catch (error) {
      console.error('Get conversation history error:', error);
      throw error;
    }
  }

  async clearConversationHistory(userId?: string): Promise<{ deleted: number }> {
    try {
      const response = await this.apiClient.delete(`/api/agent/conversations/${userId || this.config.userId}`);
      return response.data;
    } catch (error) {
      console.error('Clear conversation history error:', error);
      throw error;
    }
  }

  // Utility Methods
  async testConnection(): Promise<boolean> {
    try {
      const response = await this.apiClient.get('/api/agent/health');
      return response.status === 200;
    } catch (error) {
      console.error('Connection test failed:', error);
      return false;
    }
  }

  // Configuration
  updateConfig(newConfig: Partial<AgenticConfig>): void {
    this.config = { ...this.config, ...newConfig };
  }

  getConfig(): AgenticConfig {
    return { ...this.config };
  }

  // Mock responses for development (when API is not available)
  getMockResponse(type: string): AgentResponse {
    const mockResponses: Record<string, AgentResponse> = {
      chat: {
        taskId: 'mock_chat_001',
        taskType: 'chat',
        status: 'completed',
        response: 'This is a mock response from the AI agent. The system is working correctly.',
        result: {
          confidence: 0.95,
          processing_time: 1.2
        },
        createdAt: new Date(),
        completedAt: new Date()
      },
      claim_analysis: {
        taskId: 'mock_analysis_001',
        taskType: 'analyze_claim',
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
        createdAt: new Date(),
        completedAt: new Date()
      },
      rejection_analysis: {
        taskId: 'mock_rejection_001',
        taskType: 'analyze_rejection',
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
        createdAt: new Date(),
        completedAt: new Date()
      }
    };

    return mockResponses[type] || mockResponses.chat;
  }
} 