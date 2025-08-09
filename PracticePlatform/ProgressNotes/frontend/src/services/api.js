import { API_BASE_URL } from '../utils/constants';

class APIService {
  static async request(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
      if (response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.reload();
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  }

  // Auth endpoints
  static async login(email, password) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  static async getMe() {
    return this.request('/auth/me');
  }

  // Notes endpoints
  static async getNotes(filters = {}) {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value);
      }
    });
    return this.request(`/notes/?${params.toString()}`);
  }

  static async getNote(noteId) {
    return this.request(`/notes/${noteId}`);
  }

  static async createNote(noteData) {
    return this.request('/notes/', {
      method: 'POST',
      body: JSON.stringify(noteData),
    });
  }

  static async updateNote(noteId, noteData) {
    return this.request(`/notes/${noteId}`, {
      method: 'PUT',
      body: JSON.stringify(noteData),
    });
  }

  static async saveDraft(noteId, content) {
    return this.request(`/notes/${noteId}/draft`, {
      method: 'POST',
      body: JSON.stringify({ content }),
    });
  }

  static async signNote(noteId, digitalSignature = null) {
    return this.request(`/notes/${noteId}/sign`, {
      method: 'POST',
      body: JSON.stringify({ digital_signature: digitalSignature }),
    });
  }

  static async unlockNote(noteId, unlockReason) {
    return this.request(`/notes/${noteId}/unlock`, {
      method: 'POST',
      body: JSON.stringify({ unlock_reason: unlockReason }),
    });
  }

  // Patient endpoints
  static async getPatients() {
    return this.request('/patients/');
  }

  static async getPatient(patientId) {
    return this.request(`/patients/${patientId}`);
  }

  static async createPatient(patientData) {
    return this.request('/patients/', {
      method: 'POST',
      body: JSON.stringify(patientData),
    });
  }

  static async updatePatient(patientId, patientData) {
    return this.request(`/patients/${patientId}`, {
      method: 'PUT',
      body: JSON.stringify(patientData),
    });
  }

  // Template endpoints
  static async getTemplates(templateType = null) {
    const params = templateType ? `?template_type=${templateType}` : '';
    return this.request(`/templates/${params}`);
  }

  static async getDashboardStats() {
    return this.request('/notes/dashboard');
  }
}

export default APIService;
