import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add loading state if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health Check
  getHealth: () => apiClient.get('/health'),

  // Model Information
  getModelInfo: () => apiClient.get('/api/v1/model/info'),

  // Example Data
  getExample: () => apiClient.get('/api/v1/example'),

  // Single Claim Scoring
  scoreClaim: (claimData) => apiClient.post('/api/v1/score', claimData),

  // Batch Claim Scoring
  scoreBatch: (claimsData) => apiClient.post('/api/v1/score/batch', { claims: claimsData }),

  // Data Pipeline Management
  generateData: (config) => apiClient.post('/api/v1/data/generate', config),
  
  getDataStats: () => apiClient.get('/api/v1/data/stats'),

  // Model Training
  trainModel: (config) => apiClient.post('/api/v1/model/train', config),
  
  getTrainingStatus: () => apiClient.get('/api/v1/model/training-status'),
  
  getTrainingHistory: () => apiClient.get('/api/v1/model/training-history'),

  // Model Management
  getModels: () => apiClient.get('/api/v1/models'),
  
  getModel: (modelId) => apiClient.get(`/api/v1/models/${modelId}`),
  
  deleteModel: (modelId) => apiClient.delete(`/api/v1/models/${modelId}`),
  
  activateModel: (modelId) => apiClient.post(`/api/v1/models/${modelId}/activate`),

  // API Service Management
  getApiConfig: () => apiClient.get('/api/v1/service/config'),
  
  updateApiConfig: (config) => apiClient.put('/api/v1/service/config', config),
  
  restartApi: () => apiClient.post('/api/v1/service/restart'),
  
  getApiStats: () => apiClient.get('/api/v1/service/stats'),

  // Monitoring
  getSystemHealth: () => apiClient.get('/api/v1/monitoring/health'),
  
  getPerformanceMetrics: () => apiClient.get('/api/v1/monitoring/performance'),
  
  getApiRequests: (params) => apiClient.get('/api/v1/monitoring/requests', { params }),

  // Settings
  getSettings: () => apiClient.get('/api/v1/settings'),
  
  updateSettings: (settings) => apiClient.put('/api/v1/settings', settings),

  // File Upload
  uploadFile: (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiClient.post('/api/v1/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    });
  },

  // WebSocket connection for real-time updates
  createWebSocket: () => {
    const wsUrl = API_BASE_URL.replace('http', 'ws') + '/ws';
    return new WebSocket(wsUrl);
  },
};

// Helper functions
export const formatApiError = (error) => {
  if (error.response) {
    return {
      message: error.response.data?.detail || error.response.data?.message || 'An error occurred',
      status: error.response.status,
    };
  } else if (error.request) {
    return {
      message: 'Unable to connect to the server',
      status: 0,
    };
  } else {
    return {
      message: error.message || 'An unexpected error occurred',
      status: 0,
    };
  }
};

export const validateClaimData = (claimData) => {
  const required = [
    'claim_id', 'submission_date', 'provider_id', 'provider_specialty',
    'patient_age', 'patient_gender', 'cpt_code', 'icd_code',
    'units_of_service', 'billed_amount', 'paid_amount',
    'place_of_service', 'prior_authorization'
  ];

  const missing = required.filter(field => !claimData[field]);
  
  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(', ')}`);
  }

  // Validate data types
  if (typeof claimData.patient_age !== 'number' || claimData.patient_age < 0 || claimData.patient_age > 120) {
    throw new Error('Patient age must be a number between 0 and 120');
  }

  if (!['M', 'F'].includes(claimData.patient_gender)) {
    throw new Error('Patient gender must be M or F');
  }

  if (typeof claimData.billed_amount !== 'number' || claimData.billed_amount <= 0) {
    throw new Error('Billed amount must be a positive number');
  }

  if (typeof claimData.paid_amount !== 'number' || claimData.paid_amount < 0) {
    throw new Error('Paid amount must be a non-negative number');
  }

  if (!['Y', 'N'].includes(claimData.prior_authorization)) {
    throw new Error('Prior authorization must be Y or N');
  }

  return true;
};

export default apiService; 