import { API_BASE_URL } from '../utils/constants';


class AuditAPI {
  static async getAuditLogs(resourceId, resourceType, filters = {}) {
    const searchParams = new URLSearchParams();
    
    searchParams.append('resource_id', resourceId);
    searchParams.append('resource_type', resourceType);
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        searchParams.append(key, value);
      }
    });

    const response = await fetch(`${API_BASE_URL}/audit-logs?${searchParams}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  static async createAuditLog(auditData) {
    const response = await fetch(`${API_BASE_URL}/audit-logs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
      body: JSON.stringify(auditData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  static async getAuditSummary(resourceId, resourceType) {
    const response = await fetch(`${API_BASE_URL}/audit-logs/summary?resource_id=${resourceId}&resource_type=${resourceType}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}

export default AuditAPI;
