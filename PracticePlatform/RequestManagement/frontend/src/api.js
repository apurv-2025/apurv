const API_BASE = 'http://localhost:8000';

// API functions
const api = {
  async getPractitioners() {
    const response = await fetch(`${API_BASE}/practitioners`);
    return response.json();
  },
  
  async getClients() {
    const response = await fetch(`${API_BASE}/clients`);
    return response.json();
  },
  
  async getAppointmentRequests() {
    const response = await fetch(`${API_BASE}/appointment-requests`);
    return response.json();
  },
  
  async createAppointmentRequest(request) {
    const response = await fetch(`${API_BASE}/appointment-requests`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });
    return response.json();
  },
  
  async updateAppointmentRequest(requestId, status) {
    const response = await fetch(`${API_BASE}/appointment-requests/${requestId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    return response.json();
  }
};

export default api;
