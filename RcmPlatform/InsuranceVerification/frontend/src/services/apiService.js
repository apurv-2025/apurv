// File: src/services/apiService.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
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

  async uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/v1/upload/insurance-card`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.status}`);
    }

    return await response.json();
  }

  async submitEligibilityInquiry(data) {
    return this.request('/api/v1/eligibility/inquiry', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getEligibilityResponse(requestId) {
    return this.request(`/api/v1/eligibility/response/${requestId}`);
  }

  async getInsuranceCards() {
    return this.request('/api/v1/insurance-cards');
  }

  async healthCheck() {
    return this.request('/');
  }
}

export const apiService = new ApiService();
