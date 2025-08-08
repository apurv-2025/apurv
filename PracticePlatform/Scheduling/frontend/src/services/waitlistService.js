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

export const waitlistService = {
  // Get all waitlist entries with pagination and filtering
  getWaitlistEntries: async (params = {}) => {
    try {
      const response = await apiClient.get('/waitlist/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching waitlist entries:', error);
      throw error;
    }
  },

  // Get waitlist entry by ID
  getWaitlistEntryById: async (entryId) => {
    try {
      const response = await apiClient.get(`/waitlist/${entryId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching waitlist entry:', error);
      throw error;
    }
  },

  // Create new waitlist entry
  createWaitlistEntry: async (entryData) => {
    try {
      const response = await apiClient.post('/waitlist/', entryData);
      return response.data;
    } catch (error) {
      console.error('Error creating waitlist entry:', error);
      throw error;
    }
  },

  // Update waitlist entry
  updateWaitlistEntry: async (entryId, entryData) => {
    try {
      const response = await apiClient.put(`/waitlist/${entryId}`, entryData);
      return response.data;
    } catch (error) {
      console.error('Error updating waitlist entry:', error);
      throw error;
    }
  },

  // Delete waitlist entry
  deleteWaitlistEntry: async (entryId) => {
    try {
      const response = await apiClient.delete(`/waitlist/${entryId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting waitlist entry:', error);
      throw error;
    }
  },

  // Search waitlist entries by patient ID
  searchWaitlistByPatient: async (patientId) => {
    try {
      const response = await apiClient.get(`/waitlist/search/patient/${patientId}`);
      return response.data;
    } catch (error) {
      console.error('Error searching waitlist by patient:', error);
      throw error;
    }
  },

  // Search waitlist entries by practitioner ID
  searchWaitlistByPractitioner: async (practitionerId) => {
    try {
      const response = await apiClient.get(`/waitlist/search/practitioner/${practitionerId}`);
      return response.data;
    } catch (error) {
      console.error('Error searching waitlist by practitioner:', error);
      throw error;
    }
  },

  // Schedule from waitlist
  scheduleFromWaitlist: async (entryId) => {
    try {
      const response = await apiClient.post(`/waitlist/${entryId}/schedule`);
      return response.data;
    } catch (error) {
      console.error('Error scheduling from waitlist:', error);
      throw error;
    }
  },

  // Get waitlist statistics
  getWaitlistStats: async () => {
    try {
      const response = await apiClient.get('/waitlist/stats/summary');
      return response.data;
    } catch (error) {
      console.error('Error fetching waitlist stats:', error);
      throw error;
    }
  }
};

export default waitlistService; 