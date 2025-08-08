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

export const calendarService = {
  // Get appointments for calendar view
  getAppointments: async (params = {}) => {
    try {
      const response = await apiClient.get('/appointments/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching appointments:', error);
      throw error;
    }
  },

  // Get patients for calendar integration
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

  // Get all practitioners
  getPractitioners: async () => {
    try {
      const response = await apiClient.get('/practitioners/');
      return response.data;
    } catch (error) {
      console.error('Error fetching practitioners:', error);
      throw error;
    }
  },

  // Get appointment types
  getAppointmentTypes: async () => {
    try {
      const response = await apiClient.get('/appointment-types/');
      return response.data;
    } catch (error) {
      console.error('Error fetching appointment types:', error);
      throw error;
    }
  },

  // Get available slots for a practitioner
  getAvailableSlots: async (practitionerId, date, appointmentTypeId = null) => {
    try {
      const params = { appointment_date: date };
      if (appointmentTypeId) {
        params.appointment_type_id = appointmentTypeId;
      }
      console.log('Calling available slots API:', {
        url: `/practitioner-availability/${practitionerId}/available-slots`,
        params
      });
      const response = await apiClient.get(`/practitioner-availability/${practitionerId}/available-slots`, { params });
      console.log('Available slots response:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error fetching available slots:', error);
      throw error;
    }
  },

  // Create new appointment
  createAppointment: async (appointmentData) => {
    try {
      const response = await apiClient.post('/appointments/', appointmentData);
      return response.data;
    } catch (error) {
      console.error('Error creating appointment:', error);
      throw error;
    }
  },

  // Update appointment
  updateAppointment: async (appointmentId, appointmentData) => {
    try {
      const response = await apiClient.put(`/appointments/${appointmentId}`, appointmentData);
      return response.data;
    } catch (error) {
      console.error('Error updating appointment:', error);
      throw error;
    }
  },

  // Delete appointment
  deleteAppointment: async (appointmentId) => {
    try {
      const response = await apiClient.delete(`/appointments/${appointmentId}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting appointment:', error);
      throw error;
    }
  }
};

export default calendarService; 