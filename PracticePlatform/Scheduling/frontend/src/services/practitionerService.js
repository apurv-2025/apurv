import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const practitionerService = {
  // Get all practitioners with pagination
  getPractitioners: async (params = {}) => {
    try {
      const response = await apiClient.get('/practitioners/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching practitioners:', error);
      throw error;
    }
  },

  // Get practitioner by ID
  getPractitionerById: async (practitionerId) => {
    try {
      const response = await apiClient.get(`/practitioners/${practitionerId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching practitioner:', error);
      throw error;
    }
  },

  // Get practitioner by FHIR ID
  getPractitionerByFhirId: async (fhirId) => {
    try {
      const response = await apiClient.get(`/practitioners/fhir/${fhirId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching practitioner by FHIR ID:', error);
      throw error;
    }
  },

  // Create new practitioner
  createPractitioner: async (practitionerData) => {
    try {
      const response = await apiClient.post('/practitioners/', practitionerData);
      return response.data;
    } catch (error) {
      console.error('Error creating practitioner:', error);
      throw error;
    }
  },

  // Update practitioner
  updatePractitioner: async (practitionerId, practitionerData) => {
    try {
      const response = await apiClient.put(`/practitioners/${practitionerId}`, practitionerData);
      return response.data;
    } catch (error) {
      console.error('Error updating practitioner:', error);
      throw error;
    }
  },

  // Delete practitioner
  deletePractitioner: async (practitionerId) => {
    try {
      const response = await apiClient.delete(`/practitioners/${practitionerId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting practitioner:', error);
      throw error;
    }
  },

  // Search practitioners by name
  searchPractitionersByName: async (searchParams) => {
    try {
      const response = await apiClient.get('/practitioners/search/name', { params: searchParams });
      return response.data;
    } catch (error) {
      console.error('Error searching practitioners:', error);
      throw error;
    }
  },

  // Search practitioners by identifier
  searchPractitionersByIdentifier: async (searchParams) => {
    try {
      const response = await apiClient.get('/practitioners/search/identifier', { params: searchParams });
      return response.data;
    } catch (error) {
      console.error('Error searching practitioners by identifier:', error);
      throw error;
    }
  },

  // Search practitioners (POST method)
  searchPractitioners: async (searchData) => {
    try {
      const response = await apiClient.post('/practitioners/search', searchData);
      return response.data;
    } catch (error) {
      console.error('Error searching practitioners:', error);
      throw error;
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/practitioners/health/check');
      return response.data;
    } catch (error) {
      console.error('Error checking practitioner service health:', error);
      throw error;
    }
  }
};

export default practitionerService; 