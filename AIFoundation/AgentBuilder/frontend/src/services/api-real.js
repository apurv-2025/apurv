// API Service
class ApiService {
  constructor() {
    this.baseUrl = 'http://localhost:8000';
    this.token = localStorage.getItem('token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`${this.baseUrl}/auth/token`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    this.token = data.access_token;
    localStorage.setItem('token', this.token);
    return data;
  }

  async register(userData) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getCurrentUser() {
    return this.request('/auth/me');
  }

  async getAgents() {
    return this.request('/agents/');
  }

  async createAgent(agentData) {
    return this.request('/agents/', {
      method: 'POST',
      body: JSON.stringify(agentData),
    });
  }

  async updateAgent(agentId, agentData) {
    return this.request(`/agents/${agentId}`, {
      method: 'PUT',
      body: JSON.stringify(agentData),
    });
  }

  async deleteAgent(agentId) {
    return this.request(`/agents/${agentId}`, {
      method: 'DELETE',
    });
  }

  async chatWithAgent(agentId, message) {
    return this.request('/agents/chat', {
      method: 'POST',
      body: JSON.stringify({ agent_id: agentId, message }),
    });
  }

  async getKnowledgeBase(agentId) {
    return this.request(`/knowledge/${agentId}`);
  }

  async uploadDocument(agentId, file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/knowledge/upload/${agentId}`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }

    return response.json();
  }

  logout() {
    this.token = null;
    localStorage.removeItem('token');
  }
}

export const api = new ApiService();
