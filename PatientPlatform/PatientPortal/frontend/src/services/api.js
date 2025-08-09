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

// Fitness API
export const fitnessAPI = {
  getFitnessData: async (period = 'week') => {
    const response = await api.get(`/fitness/data?period=${period}`);
    return response.data;
  },
  
  getDevices: async () => {
    const response = await api.get('/fitness/devices');
    return response.data;
  },
  
  syncDevice: async (deviceId) => {
    const response = await api.post(`/fitness/devices/${deviceId}/sync`);
    return response.data;
  },
  
  updateGoals: async (goals) => {
    const response = await api.put('/fitness/goals', goals);
    return response.data;
  }
};

// Wellness API
export const wellnessAPI = {
  getWellnessData: async () => {
    const response = await api.get('/wellness/data');
    return response.data;
  },
  
  getHabits: async () => {
    const response = await api.get('/wellness/habits');
    return response.data;
  },
  
  updateHabit: async (habitId, data) => {
    const response = await api.put(`/wellness/habits/${habitId}`, data);
    return response.data;
  },
  
  getConnectedApps: async () => {
    const response = await api.get('/wellness/apps');
    return response.data;
  },
  
  connectApp: async (appData) => {
    const response = await api.post('/wellness/apps/connect', appData);
    return response.data;
  }
};

// Settings/Integration API
export const settingsAPI = {
  getIntegrations: async () => {
    const response = await api.get('/settings/integrations');
    return response.data;
  },
  
  updateIntegration: async (integrationId, data) => {
    const response = await api.put(`/settings/integrations/${integrationId}`, data);
    return response.data;
  },
  
  connectEHR: async (ehrData) => {
    const response = await api.post('/settings/integrations/ehr', ehrData);
    return response.data;
  },
  
  disconnectIntegration: async (integrationId) => {
    const response = await api.delete(`/settings/integrations/${integrationId}`);
    return response.data;
  },
  
  generateAPIKey: async () => {
    const response = await api.post('/settings/api-key/generate');
    return response.data;
  },
  
  getNotificationSettings: async () => {
    const response = await api.get('/settings/notifications');
    return response.data;
  },
  
  updateNotificationSettings: async (settings) => {
    const response = await api.put('/settings/notifications', settings);
    return response.data;
  }
};

// Records API
export const recordsAPI = {
  getRecords: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/records${queryString ? `?${queryString}` : ''}`);
    return response.data;
  },
  
  getRecordDetail: async (recordId) => {
    const response = await api.get(`/records/${recordId}`);
    return response.data;
  },
  
  getVisitSummaries: async () => {
    const response = await api.get('/records/visits');
    return response.data;
  },
  
  getImmunizations: async () => {
    const response = await api.get('/records/immunizations');
    return response.data;
  },
  
  getAllergies: async () => {
    const response = await api.get('/records/allergies');
    return response.data;
  },
  
  getMedicalConditions: async () => {
    const response = await api.get('/records/conditions');
    return response.data;
  },
  
  getRecordsSummary: async () => {
    const response = await api.get('/records/summary');
    return response.data;
  },
  
  downloadRecord: async (recordId) => {
    const response = await api.get(`/records/download/${recordId}`);
    return response.data;
  },
  
  downloadAllRecords: async () => {
    const response = await api.get('/records/download/all');
    return response.data;
  },
  
  getProviders: async () => {
    const response = await api.get('/records/providers');
    return response.data;
  },
  
  getRecordTypes: async () => {
    const response = await api.get('/records/types');
    return response.data;
  }
};

// Billing API
export const billingAPI = {
  getOverview: async () => {
    const response = await api.get('/billing/overview');
    return response.data;
  },
  
  getInvoices: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/billing/invoices${queryString ? `?${queryString}` : ''}`);
    return response.data;
  },
  
  getInvoiceDetail: async (invoiceId) => {
    const response = await api.get(`/billing/invoices/${invoiceId}`);
    return response.data;
  },
  
  getInsuranceCards: async () => {
    const response = await api.get('/billing/insurance-cards');
    return response.data;
  },
  
  addInsuranceCard: async (cardData) => {
    const response = await api.post('/billing/insurance-cards', cardData);
    return response.data;
  },
  
  updateInsuranceCard: async (cardId, cardData) => {
    const response = await api.put(`/billing/insurance-cards/${cardId}`, cardData);
    return response.data;
  },
  
  deleteInsuranceCard: async (cardId) => {
    const response = await api.delete(`/billing/insurance-cards/${cardId}`);
    return response.data;
  },
  
  uploadInsuranceCardImage: async (cardId, side, file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post(`/billing/insurance-cards/${cardId}/upload-image?side=${side}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },
  
  getCoverageDetails: async () => {
    const response = await api.get('/billing/coverage');
    return response.data;
  },
  
  getPaymentHistory: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/billing/payments${queryString ? `?${queryString}` : ''}`);
    return response.data;
  },
  
  processPayment: async (paymentData) => {
    const response = await api.post('/billing/payments', paymentData);
    return response.data;
  },
  
  getStatements: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/billing/statements${queryString ? `?${queryString}` : ''}`);
    return response.data;
  },
  
  getBillingSummary: async () => {
    const response = await api.get('/billing/summary');
    return response.data;
  },
  
  downloadInvoice: async (invoiceId) => {
    const response = await api.get(`/billing/download/invoice/${invoiceId}`);
    return response.data;
  },
  
  downloadStatement: async (statementId) => {
    const response = await api.get(`/billing/download/statement/${statementId}`);
    return response.data;
  }
};

// Forms API
export const formsAPI = {
  getAvailableForms: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/forms/available${queryString ? `?${queryString}` : ''}`);
    return response.data;
  },
  
  getCompletedForms: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/forms/completed${queryString ? `?${queryString}` : ''}`);
    return response.data;
  },
  
  getPendingForms: async () => {
    const response = await api.get('/forms/pending');
    return response.data;
  },
  
  getFormTemplate: async (formId) => {
    const response = await api.get(`/forms/templates/${formId}`);
    return response.data;
  },
  
  submitForm: async (formData) => {
    const response = await api.post('/forms/submit', formData);
    return response.data;
  },
  
  saveDraft: async (formData) => {
    const response = await api.post('/forms/save-draft', formData);
    return response.data;
  },
  
  getDocuments: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/forms/documents${queryString ? `?${queryString}` : ''}`);
    return response.data;
  },
  
  uploadDocument: async (file, metadata = {}) => {
    const formData = new FormData();
    formData.append('file', file);
    Object.keys(metadata).forEach(key => {
      if (metadata[key]) formData.append(key, metadata[key]);
    });
    const response = await api.post('/forms/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  },
  
  deleteDocument: async (documentId) => {
    const response = await api.delete(`/forms/documents/${documentId}`);
    return response.data;
  },
  
  downloadDocument: async (documentId) => {
    const response = await api.get(`/forms/documents/${documentId}/download`);
    return response.data;
  },
  
  getFormsSummary: async () => {
    const response = await api.get('/forms/summary');
    return response.data;
  },
  
  getFormCategories: async () => {
    const response = await api.get('/forms/categories');
    return response.data;
  },
  
  getDocumentCategories: async () => {
    const response = await api.get('/forms/document-categories');
    return response.data;
  }
};

// Telehealth API
export const telehealthAPI = {
  getUpcomingAppointments: async () => {
    const response = await api.get('/telehealth/appointments/upcoming');
    return response.data;
  },
  
  getCompletedSessions: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/telehealth/appointments/completed${queryString ? `?${queryString}` : ''}`);
    return response.data;
  },
  
  getAppointmentDetails: async (appointmentId) => {
    const response = await api.get(`/telehealth/appointments/${appointmentId}`);
    return response.data;
  },
  
  joinAppointment: async (appointmentId) => {
    const response = await api.post(`/telehealth/appointments/${appointmentId}/join`);
    return response.data;
  },
  
  getSystemStatus: async () => {
    const response = await api.get('/telehealth/system/status');
    return response.data;
  },
  
  runDeviceCheck: async () => {
    const response = await api.post('/telehealth/system/device-check');
    return response.data;
  },
  
  getSupportResources: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const response = await api.get(`/telehealth/support/resources${queryString ? `?${queryString}` : ''}`);
    return response.data;
  },
  
  getSupportResource: async (resourceId) => {
    const response = await api.get(`/telehealth/support/resource/${resourceId}`);
    return response.data;
  },
  
  contactSupport: async (supportData) => {
    const response = await api.post('/telehealth/support/contact', supportData);
    return response.data;
  },
  
  completeTechCheck: async (appointmentId) => {
    const response = await api.post(`/telehealth/appointments/${appointmentId}/tech-check`);
    return response.data;
  },
  
  getTelehealthSummary: async () => {
    const response = await api.get('/telehealth/summary');
    return response.data;
  }
};

export default api;
