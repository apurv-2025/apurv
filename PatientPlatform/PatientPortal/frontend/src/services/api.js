// frontend/src/services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
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

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },
  
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/users/me');
    return response.data;
  }
};

// User API
export const userAPI = {
  updateProfile: async (userData) => {
    const response = await api.put('/users/me', userData);
    return response.data;
  }
};

// Appointments API
export const appointmentsAPI = {
  getAppointments: async () => {
    const response = await api.get('/appointments');
    return response.data;
  },
  
  createAppointment: async (appointmentData) => {
    const response = await api.post('/appointments', appointmentData);
    return response.data;
  },
  
  updateAppointment: async (id, appointmentData) => {
    const response = await api.put(`/appointments/${id}`, appointmentData);
    return response.data;
  }
};

// Medications API
export const medicationsAPI = {
  getMedications: async () => {
    const response = await api.get('/medications');
    return response.data;
  },
  
  requestRefill: async (medicationId) => {
    const response = await api.post(`/medications/${medicationId}/refill`);
    return response.data;
  }
};

// Lab Results API
export const labResultsAPI = {
  getLabResults: async () => {
    const response = await api.get('/lab-results');
    return response.data;
  }
};

// Messages API
export const messagesAPI = {
  getMessages: async () => {
    const response = await api.get('/messages');
    return response.data;
  },
  
  markAsRead: async (messageId) => {
    const response = await api.put(`/messages/${messageId}/read`);
    return response.data;
  }
};

export default api;
