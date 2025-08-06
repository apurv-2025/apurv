/**
 * Agent Service for PatientPortal
 * Handles all AI agent API interactions
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class AgentService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/agent`;
  }

  // Generic API call helper
  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Agent API request failed:', error);
      throw error;
    }
  }

  // Chat with AI agent
  async chat(message, userId, context = {}) {
    return this.makeRequest('/chat', {
      method: 'POST',
      body: JSON.stringify({
        message,
        user_id: userId,
        context: {
          ...context,
          patient_portal: true
        }
      })
    });
  }

  // Schedule appointment using AI
  async scheduleAppointment(patientId, appointmentType, preferredDate = null) {
    return this.makeRequest('/schedule-appointment', {
      method: 'POST',
      body: JSON.stringify({
        patient_id: patientId,
        appointment_type: appointmentType,
        preferred_date: preferredDate
      })
    });
  }

  // Check medications using AI
  async checkMedications(patientId) {
    return this.makeRequest('/check-medications', {
      method: 'POST',
      body: JSON.stringify({
        patient_id: patientId
      })
    });
  }

  // Analyze lab results using AI
  async analyzeLabResults(patientId, labResultId = null) {
    return this.makeRequest('/analyze-lab-results', {
      method: 'POST',
      body: JSON.stringify({
        patient_id: patientId,
        lab_result_id: labResultId
      })
    });
  }

  // Generate health summary using AI
  async generateHealthSummary(patientId, reportType = 'comprehensive') {
    return this.makeRequest('/generate-health-summary', {
      method: 'POST',
      body: JSON.stringify({
        patient_id: patientId,
        report_type: reportType
      })
    });
  }

  // Set up medication reminder using AI
  async setupMedicationReminder(patientId, medicationId, reminderTime) {
    return this.makeRequest('/setup-medication-reminder', {
      method: 'POST',
      body: JSON.stringify({
        patient_id: patientId,
        medication_id: medicationId,
        reminder_time: reminderTime
      })
    });
  }

  // Find doctors using AI
  async findDoctors(specialty, location = null) {
    return this.makeRequest('/find-doctors', {
      method: 'POST',
      body: JSON.stringify({
        specialty,
        location
      })
    });
  }

  // Get conversation history
  async getConversationHistory(userId, limit = 50, offset = 0) {
    return this.makeRequest(`/conversation-history/${userId}?limit=${limit}&offset=${offset}`, {
      method: 'GET'
    });
  }

  // Get available tools
  async getAvailableTools() {
    return this.makeRequest('/tools', {
      method: 'GET'
    });
  }

  // Get tool information
  async getToolInfo(toolName) {
    return this.makeRequest(`/tools/${toolName}/info`, {
      method: 'GET'
    });
  }

  // Get agent health status
  async getHealthStatus() {
    return this.makeRequest('/health', {
      method: 'GET'
    });
  }

  // Get agent metrics
  async getMetrics() {
    return this.makeRequest('/metrics', {
      method: 'GET'
    });
  }

  // Create agent task
  async createTask(taskType, userId, taskDescription, context = {}) {
    return this.makeRequest('/tasks', {
      method: 'POST',
      body: JSON.stringify({
        task_type: taskType,
        user_id: userId,
        task_description: taskDescription,
        context
      })
    });
  }

  // Get task status
  async getTaskStatus(taskId) {
    return this.makeRequest(`/tasks/${taskId}/status`, {
      method: 'GET'
    });
  }

  // Get active tasks
  async getActiveTasks() {
    return this.makeRequest('/tasks/active', {
      method: 'GET'
    });
  }

  // Create batch tasks
  async createBatchTasks(tasks, userId, maxConcurrent = 3) {
    return this.makeRequest('/batch-tasks', {
      method: 'POST',
      body: JSON.stringify({
        tasks,
        user_id: userId,
        max_concurrent: maxConcurrent
      })
    });
  }

  // Clear conversation history
  async clearConversationHistory(userId) {
    return this.makeRequest(`/conversations/${userId}`, {
      method: 'DELETE'
    });
  }

  // Mock methods for development/testing
  async mockChat(message, userId, context = {}) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    
    const lowerMessage = message.toLowerCase();
    let response = "I'm here to help with your health needs!";
    
    if (lowerMessage.includes('appointment') || lowerMessage.includes('schedule')) {
      response = "I can help you schedule an appointment! What type of visit do you need? I can assist with annual physicals, specialist consultations, or urgent care visits.";
    } else if (lowerMessage.includes('medication') || lowerMessage.includes('meds')) {
      response = "I can help you check your medications, refill status, and set up reminders. Would you like me to review your current medication list?";
    } else if (lowerMessage.includes('lab') || lowerMessage.includes('test')) {
      response = "I can help you understand your lab results! I can explain what each test means and provide personalized insights. Which lab results would you like me to review?";
    } else if (lowerMessage.includes('doctor') || lowerMessage.includes('physician')) {
      response = "I can help you find and book appointments with doctors. What specialty are you looking for? I can search based on location, availability, and your insurance.";
    } else if (lowerMessage.includes('health') || lowerMessage.includes('summary')) {
      response = "I can generate a comprehensive health summary for you, including your recent appointments, medications, lab results, and personalized recommendations.";
    }
    
    return {
      response,
      conversation_id: `conv_${Date.now()}`,
      message_id: `msg_${Date.now()}`,
      timestamp: new Date().toISOString()
    };
  }

  async mockScheduleAppointment(patientId, appointmentType, preferredDate = null) {
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    return {
      task_id: `task_${Date.now()}`,
      task_type: 'schedule_appointment',
      status: 'completed',
      response: 'Appointment scheduled successfully',
      result: {
        appointment_id: `apt_${Date.now()}`,
        patient_id: patientId,
        appointment_type: appointmentType,
        scheduled_date: preferredDate || '2024-02-15T10:00:00Z',
        doctor_name: 'Dr. Smith',
        location: 'Main Medical Center',
        status: 'scheduled',
        ai_suggestions: [
          'Bring your insurance card',
          'Arrive 15 minutes early',
          'Prepare questions for your doctor'
        ]
      },
      created_at: new Date().toISOString(),
      completed_at: new Date().toISOString()
    };
  }

  async mockCheckMedications(patientId) {
    await new Promise(resolve => setTimeout(resolve, 1200));
    
    return {
      task_id: `task_${Date.now()}`,
      task_type: 'check_medications',
      status: 'completed',
      response: 'Medication check completed successfully',
      result: {
        medications: [
          {
            id: 'med_001',
            name: 'Lisinopril',
            dosage: '10mg',
            frequency: 'Once daily',
            refills_remaining: 2,
            next_refill_date: '2024-02-20',
            pharmacy: 'CVS Pharmacy'
          },
          {
            id: 'med_002',
            name: 'Metformin',
            dosage: '500mg',
            frequency: 'Twice daily',
            refills_remaining: 0,
            next_refill_date: '2024-02-10',
            pharmacy: 'Walgreens'
          }
        ],
        total_medications: 2,
        needs_refill: 1,
        status: 'completed'
      },
      created_at: new Date().toISOString(),
      completed_at: new Date().toISOString()
    };
  }

  async mockAnalyzeLabResults(patientId, labResultId = null) {
    await new Promise(resolve => setTimeout(resolve, 1800));
    
    return {
      task_id: `task_${Date.now()}`,
      task_type: 'view_lab_results',
      status: 'completed',
      response: 'Lab results analysis completed successfully',
      result: {
        lab_results: [
          {
            id: 'lab_001',
            test_name: 'Complete Blood Count',
            date: '2024-01-15',
            results: {
              hemoglobin: { value: '14.2', unit: 'g/dL', normal_range: '12.0-15.5', status: 'normal' },
              white_blood_cells: { value: '7.5', unit: 'K/μL', normal_range: '4.5-11.0', status: 'normal' },
              platelets: { value: '250', unit: 'K/μL', normal_range: '150-450', status: 'normal' }
            },
            ai_interpretation: 'All values are within normal ranges. Your blood count looks healthy.',
            recommendations: ['Continue current diet and exercise routine', 'Schedule follow-up in 6 months']
          }
        ],
        total_results: 1,
        status: 'completed'
      },
      created_at: new Date().toISOString(),
      completed_at: new Date().toISOString()
    };
  }

  async mockGenerateHealthSummary(patientId, reportType = 'comprehensive') {
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return {
      task_id: `task_${Date.now()}`,
      task_type: 'generate_health_summary',
      status: 'completed',
      response: 'Health summary generated successfully',
      result: {
        health_summary: {
          patient_id: patientId,
          report_type: reportType,
          generated_date: new Date().toISOString(),
          summary: {
            overall_health: 'Good',
            active_conditions: ['Hypertension', 'Type 2 Diabetes'],
            current_medications: 2,
            recent_appointments: 3,
            upcoming_appointments: 1,
            lab_results_status: 'All normal',
            recommendations: [
              'Continue blood pressure monitoring',
              'Maintain diabetes management plan',
              'Schedule annual physical'
            ]
          },
          ai_insights: 'Your health metrics show good control of chronic conditions. Continue with current treatment plan.'
        },
        status: 'completed'
      },
      created_at: new Date().toISOString(),
      completed_at: new Date().toISOString()
    };
  }

  async mockFindDoctors(specialty, location = null) {
    await new Promise(resolve => setTimeout(resolve, 1600));
    
    return {
      task_id: `task_${Date.now()}`,
      task_type: 'find_doctor',
      status: 'completed',
      response: 'Doctor search completed successfully',
      result: {
        doctors: [
          {
            id: 'doc_001',
            name: 'Dr. Sarah Johnson',
            specialty: specialty,
            location: 'Main Medical Center',
            rating: 4.8,
            available_slots: [
              '2024-02-15T10:00:00Z',
              '2024-02-16T14:00:00Z',
              '2024-02-17T09:00:00Z'
            ],
            accepts_insurance: true
          },
          {
            id: 'doc_002',
            name: 'Dr. Michael Chen',
            specialty: specialty,
            location: 'Downtown Clinic',
            rating: 4.6,
            available_slots: [
              '2024-02-15T15:00:00Z',
              '2024-02-18T11:00:00Z'
            ],
            accepts_insurance: true
          }
        ],
        total_doctors: 2,
        status: 'completed'
      },
      created_at: new Date().toISOString(),
      completed_at: new Date().toISOString()
    };
  }

  async mockGetAvailableTools() {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return {
      tools: [
        { name: 'schedule_appointment', description: 'Schedule a new appointment' },
        { name: 'check_medications', description: 'Check medication information and refills' },
        { name: 'view_lab_results', description: 'View and explain lab results' },
        { name: 'health_summary', description: 'Generate health summary report' },
        { name: 'medication_reminder', description: 'Set up medication reminders' },
        { name: 'find_doctor', description: 'Find and book appointments with doctors' }
      ]
    };
  }

  async mockGetHealthStatus() {
    await new Promise(resolve => setTimeout(resolve, 300));
    
    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: '1.0.0',
      uptime: '2 days, 5 hours',
      active_tasks: 0,
      model_connected: true,
      database_connected: true,
      tools_count: 6,
      patient_portal: {
        patients_count: 1250,
        appointments_count: 85,
        database_connected: true
      }
    };
  }

  async mockGetMetrics() {
    await new Promise(resolve => setTimeout(resolve, 400));
    
    return {
      total_conversations: 156,
      total_tasks: 89,
      average_response_time: 1.2,
      success_rate: 95.2,
      patient_portal: {
        total_patients: 1250,
        active_patients: 980,
        appointments_today: 15,
        engagement_rate: 78.5
      }
    };
  }
}

// Create singleton instance
const agentService = new AgentService();

export default agentService; 