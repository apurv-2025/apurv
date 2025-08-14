# api_client.py - Frontend API integration utilities
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth tokens
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Charge API functions
export const chargeAPI = {
  // Create a new charge
  createCharge: async (chargeData) => {
    const response = await apiClient.post('/charges', chargeData);
    return response.data;
  },

  // Get charge by ID
  getCharge: async (chargeId) => {
    const response = await apiClient.get(`/charges/${chargeId}`);
    return response.data;
  },

  // Update charge
  updateCharge: async (chargeId, updateData) => {
    const response = await apiClient.put(`/charges/${chargeId}`, updateData);
    return response.data;
  },

  // Search charges
  searchCharges: async (params) => {
    const response = await apiClient.get('/charges', { params });
    return response.data;
  },

  // Validate charge
  validateCharge: async (chargeData) => {
    const response = await apiClient.post('/charges/validate', chargeData);
    return response.data;
  },

  // Create batch charges
  createBatchCharges: async (chargesData) => {
    const response = await apiClient.post('/charges/batch', chargesData);
    return response.data;
  },

  // Submit charge to billing
  submitCharge: async (chargeId) => {
    const response = await apiClient.post(`/charges/${chargeId}/submit`);
    return response.data;
  },
};

// Template API functions
export const templateAPI = {
  // Get templates
  getTemplates: async (params) => {
    const response = await apiClient.get('/templates', { params });
    return response.data;
  },

  // Create template
  createTemplate: async (templateData) => {
    const response = await apiClient.post('/templates', templateData);
    return response.data;
  },

  // Update template
  updateTemplate: async (templateId, updateData) => {
    const response = await apiClient.put(`/templates/${templateId}`, updateData);
    return response.data;
  },
};

// Medical codes API functions
export const codeAPI = {
  // Search CPT codes
  searchCPTCodes: async (query, specialty, limit = 10) => {
    const response = await apiClient.get('/codes/cpt/search', {
      params: { query, specialty, limit }
    });
    return response.data;
  },

  // Search ICD codes
  searchICDCodes: async (query, limit = 10) => {
    const response = await apiClient.get('/codes/icd/search', {
      params: { query, limit }
    });
    return response.data;
  },

  // Get provider favorites
  getProviderFavorites: async (providerId) => {
    const response = await apiClient.get(`/codes/favorites/${providerId}`);
    return response.data;
  },
};

// Reporting API functions
export const reportingAPI = {
  // Get charge metrics
  getChargeMetrics: async (dateFrom, dateTo, specialty) => {
    const response = await apiClient.get('/reports/charge-metrics', {
      params: { date_from: dateFrom, date_to: dateTo, specialty }
    });
    return response.data;
  },

  // Get provider metrics
  getProviderMetrics: async (dateFrom, dateTo, providerId) => {
    const response = await apiClient.get('/reports/provider-metrics', {
      params: { date_from: dateFrom, date_to: dateTo, provider_id: providerId }
    });
    return response.data;
  },

  // Get missed charges
  getMissedCharges: async (dateFrom, dateTo, specialty) => {
    const response = await apiClient.get('/encounters/without-charges', {
      params: { date_from: dateFrom, date_to: dateTo, specialty }
    });
    return response.data;
  },
};

export default apiClient;
