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

export const patientService = {
  // Get all patients with pagination
  getPatients: async (params = {}) => {
    try {
      const response = await apiClient.get('/patients/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching patients:', error);
      throw error;
    }
  },

  // Get patient by ID
  getPatientById: async (patientId) => {
    try {
      const response = await apiClient.get(`/patients/${patientId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching patient:', error);
      throw error;
    }
  },

  // Get patient by FHIR ID
  getPatientByFhirId: async (fhirId) => {
    try {
      const response = await apiClient.get(`/patients/fhir/${fhirId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching patient by FHIR ID:', error);
      throw error;
    }
  },

  // Create new patient
  createPatient: async (patientData) => {
    try {
      const response = await apiClient.post('/patients/', patientData);
      return response.data;
    } catch (error) {
      console.error('Error creating patient:', error);
      throw error;
    }
  },

  // Update patient
  updatePatient: async (patientId, patientData) => {
    try {
      const response = await apiClient.put(`/patients/${patientId}`, patientData);
      return response.data;
    } catch (error) {
      console.error('Error updating patient:', error);
      throw error;
    }
  },

  // Delete patient
  deletePatient: async (patientId) => {
    try {
      const response = await apiClient.delete(`/patients/${patientId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting patient:', error);
      throw error;
    }
  },

  // Search patients by name
  searchPatientsByName: async (searchParams) => {
    try {
      const response = await apiClient.get('/patients/search/name', { params: searchParams });
      return response.data;
    } catch (error) {
      console.error('Error searching patients:', error);
      throw error;
    }
  },

  // Search patients (POST method)
  searchPatients: async (searchData) => {
    try {
      const response = await apiClient.post('/patients/search', searchData);
      return response.data;
    } catch (error) {
      console.error('Error searching patients:', error);
      throw error;
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await apiClient.get('/patients/health/check');
      return response.data;
    } catch (error) {
      console.error('Error checking patient service health:', error);
      throw error;
    }
  }
};

export default patientService; 