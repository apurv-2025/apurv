// File: src/services/authorizationService.js - API Service
class AuthorizationService {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';
  }

  async request(endpoint, options = {}) {
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
      console.error('API request failed:', error);
      throw error;
    }
  }

  async submitPriorAuthorizationRequest(requestData) {
    return this.request('/prior-authorization/request', {
      method: 'POST',
      body: JSON.stringify(requestData),
    });
  }

  async getPriorAuthorizationResponse(requestId) {
    return this.request(`/prior-authorization/response/${requestId}`);
  }

  async createPatientInformation(patientData) {
    return this.request('/patient-information/', {
      method: 'POST',
      body: JSON.stringify(patientData),
    });
  }

  async getPatientEDI275(patientId) {
    return this.request(`/patient-information/edi-275/${patientId}`);
  }

  async getAuthorizationRequests(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/prior-authorization/requests${queryString ? '?' + queryString : ''}`);
  }

  async getPatients(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/patient-information/${queryString ? '?' + queryString : ''}`);
  }

  async healthCheck() {
    return this.request('/health/');
  }
}

export const authorizationService = new AuthorizationService()
