// =============================================================================
// FILE: frontend/src/services/agentService.js
// =============================================================================
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance for agent API
const agentApi = axios.create({
  baseURL: `${API_BASE_URL}/agent`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
agentApi.interceptors.request.use(
  (config) => {
    console.log('Agent API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('Agent API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging
agentApi.interceptors.response.use(
  (response) => {
    console.log('Agent API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('Agent API Response Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

export const agentService = {
  // Chat with the agent
  async chat(message, userId = 'default_user') {
    try {
      const response = await agentApi.post('/chat', {
        task_description: message,
        user_id: userId,
        task_type: 'general_query'
      });
      return response.data;
    } catch (error) {
      console.error('Error chatting with agent:', error);
      throw error;
    }
  },

  // Get task status
  async getTaskStatus(taskId) {
    try {
      const response = await agentApi.get(`/tasks/${taskId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting task status:', error);
      throw error;
    }
  },

  // Cancel a task
  async cancelTask(taskId) {
    try {
      const response = await agentApi.delete(`/tasks/${taskId}`);
      return response.data;
    } catch (error) {
      console.error('Error cancelling task:', error);
      throw error;
    }
  },

  // Get active tasks
  async getActiveTasks() {
    try {
      const response = await agentApi.get('/tasks');
      return response.data;
    } catch (error) {
      console.error('Error getting active tasks:', error);
      throw error;
    }
  },

  // Get task history
  async getTaskHistory(limit = 50) {
    try {
      const response = await agentApi.get(`/history?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error getting task history:', error);
      throw error;
    }
  },

  // Get agent status
  async getAgentStatus() {
    try {
      const response = await agentApi.get('/status');
      return response.data;
    } catch (error) {
      console.error('Error getting agent status:', error);
      throw error;
    }
  },

  // Get task statistics
  async getTaskStatistics() {
    try {
      const response = await agentApi.get('/statistics');
      return response.data;
    } catch (error) {
      console.error('Error getting task statistics:', error);
      throw error;
    }
  },

  // Get agent health
  async getAgentHealth() {
    try {
      const response = await agentApi.get('/monitoring/health');
      return response.data;
    } catch (error) {
      console.error('Error getting agent health:', error);
      throw error;
    }
  },

  // Get performance metrics
  async getPerformanceMetrics(windowMinutes = 60) {
    try {
      const response = await agentApi.get(`/monitoring/performance?window_minutes=${windowMinutes}`);
      return response.data;
    } catch (error) {
      console.error('Error getting performance metrics:', error);
      throw error;
    }
  },

  // Get error summary
  async getErrorSummary(hours = 24) {
    try {
      const response = await agentApi.get(`/monitoring/errors?hours=${hours}`);
      return response.data;
    } catch (error) {
      console.error('Error getting error summary:', error);
      throw error;
    }
  },

  // Get agent uptime
  async getAgentUptime() {
    try {
      const response = await agentApi.get('/monitoring/uptime');
      return response.data;
    } catch (error) {
      console.error('Error getting agent uptime:', error);
      throw error;
    }
  },

  // Execute a specific tool
  async executeTool(toolName, args = {}) {
    try {
      const response = await agentApi.post('/tools/execute', {
        tool_name: toolName,
        args: args
      });
      return response.data;
    } catch (error) {
      console.error('Error executing tool:', error);
      throw error;
    }
  },

  // List available tools
  async listAvailableTools() {
    try {
      const response = await agentApi.get('/tools');
      return response.data;
    } catch (error) {
      console.error('Error listing tools:', error);
      throw error;
    }
  },

  // Clear task history
  async clearTaskHistory(olderThanDays = 30) {
    try {
      const response = await agentApi.delete(`/history?older_than_days=${olderThanDays}`);
      return response.data;
    } catch (error) {
      console.error('Error clearing task history:', error);
      throw error;
    }
  },

  // Export task history
  async exportTaskHistory(format = 'json') {
    try {
      const response = await agentApi.get(`/export/history?format=${format}`);
      return response.data;
    } catch (error) {
      console.error('Error exporting task history:', error);
      throw error;
    }
  },

  // Export monitoring metrics
  async exportMonitoringMetrics(format = 'json') {
    try {
      const response = await agentApi.get(`/export/metrics?format=${format}`);
      return response.data;
    } catch (error) {
      console.error('Error exporting monitoring metrics:', error);
      throw error;
    }
  },

  // Reset agent metrics
  async resetAgentMetrics() {
    try {
      const response = await agentApi.post('/reset');
      return response.data;
    } catch (error) {
      console.error('Error resetting agent metrics:', error);
      throw error;
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await agentApi.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking agent health:', error);
      throw error;
    }
  },

  // Schedule appointment via agent
  async scheduleAppointment(appointmentData) {
    try {
      const response = await agentApi.post('/chat', {
        task_description: `Schedule an appointment for ${appointmentData.patient_name} with ${appointmentData.practitioner_name} on ${appointmentData.date} at ${appointmentData.time}`,
        user_id: appointmentData.user_id || 'default_user',
        task_type: 'schedule_appointment',
        context: {
          patient_id: appointmentData.patient_id,
          practitioner_id: appointmentData.practitioner_id,
          start_time: appointmentData.start_time,
          end_time: appointmentData.end_time,
          appointment_type: appointmentData.appointment_type,
          location: appointmentData.location,
          notes: appointmentData.notes
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error scheduling appointment via agent:', error);
      throw error;
    }
  },

  // Find availability via agent
  async findAvailability(practitionerId, date, durationMinutes = 60) {
    try {
      const response = await agentApi.post('/chat', {
        task_description: `Find available time slots for practitioner ${practitionerId} on ${date} for ${durationMinutes} minutes`,
        user_id: 'default_user',
        task_type: 'find_availability',
        context: {
          practitioner_id: practitionerId,
          date: date,
          duration_minutes: durationMinutes
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error finding availability via agent:', error);
      throw error;
    }
  },

  // Analyze schedule via agent
  async analyzeSchedule(practitionerId = null, days = 7) {
    try {
      const response = await agentApi.post('/chat', {
        task_description: `Analyze schedule patterns for the last ${days} days`,
        user_id: 'default_user',
        task_type: 'analyze_schedule',
        context: {
          practitioner_id: practitionerId,
          days: days
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error analyzing schedule via agent:', error);
      throw error;
    }
  },

  // Optimize schedule via agent
  async optimizeSchedule(practitionerId = null, optimizationType = 'general') {
    try {
      const response = await agentApi.post('/chat', {
        task_description: `Optimize schedule with ${optimizationType} optimization`,
        user_id: 'default_user',
        task_type: 'optimize_schedule',
        context: {
          practitioner_id: practitionerId,
          optimization_type: optimizationType
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error optimizing schedule via agent:', error);
      throw error;
    }
  },

  // Generate report via agent
  async generateReport(reportType = 'daily', date = null) {
    try {
      const response = await agentApi.post('/chat', {
        task_description: `Generate ${reportType} report`,
        user_id: 'default_user',
        task_type: 'generate_report',
        context: {
          report_type: reportType,
          date: date || new Date().toISOString().split('T')[0]
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error generating report via agent:', error);
      throw error;
    }
  }
};

export default agentService; 